#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const options = parseArguments(process.argv.slice(2));
const manifest = readJson(options.manifest);
const testCases = options.caseIds.map((caseId) =>
  (manifest.cases ?? []).find((entry) => entry.id === caseId),
);
const missingCaseIds = options.caseIds.filter(
  (_caseId, index) => !testCases[index],
);

if (missingCaseIds.length > 0) {
  fail(`Cases not found in ${options.manifest}: ${missingCaseIds.join(", ")}`);
}

const events = readJsonLines(options.log);
const finalMessage = findFinalAssistantMessage(events);
const finalText = finalMessage ? collectText(finalMessage.message.content) : "";
const answerObject = extractLastJsonObject(finalText);
const caseResults = testCases.map((testCase) => {
  const actual = answerObject?.[testCase.id] ?? null;
  return {
    case_id: testCase.id,
    expected: testCase.answer,
    actual,
    answer_correct: actual === testCase.answer,
    valid_choice_label:
      typeof actual === "string" && Object.hasOwn(testCase.choices, actual),
    missing_required_reads: [],
    required_reads_passed: true,
  };
});
const expectedCaseIds = testCases.map((testCase) => testCase.id).sort();
const answerKeys = answerObject ? Object.keys(answerObject).sort() : [];
const schemaExact =
  answerObject !== null &&
  JSON.stringify(answerKeys) === JSON.stringify(expectedCaseIds) &&
  caseResults.every((result) => result.valid_choice_label);
const strictJsonOnly =
  answerObject !== null &&
  !finalText.includes("\n") &&
  parseWholeJsonObject(finalText) !== null;

const userTexts = collectMessageTexts(events, "user");
const expandedMarker = `<skill name="${options.skillName}"`;
const skillExpanded =
  options.skillName !== "" &&
  userTexts.some((text) => text.includes(expandedMarker));
const expectedSkillPath = normalizeSkillPath(options.skillPath);
const expectedLocationMarker =
  options.skillName && expectedSkillPath
    ? `<skill name="${options.skillName}" location="${expectedSkillPath}">`
    : "";
const skillLocationMatched =
  expectedLocationMarker !== "" &&
  userTexts.some((text) => text.includes(expectedLocationMarker));
const anySkillExpanded = userTexts.some((text) =>
  /<skill name="[^"]+"/.test(text),
);

const readPaths = collectReadPaths(events);
const normalizedSkillPath = normalizeSuffix(expectedSkillPath);
const skillRead =
  normalizedSkillPath !== "" &&
  readPaths.some((readPath) =>
    normalizeSuffix(readPath).endsWith(normalizedSkillPath),
  );
const anySkillRead = readPaths.some(
  (readPath) => path.basename(normalizeSuffix(readPath)) === "SKILL.md",
);

for (const [index, testCase] of testCases.entries()) {
  const requiredReads = Array.isArray(testCase.required_reads)
    ? testCase.required_reads
    : [];
  caseResults[index].missing_required_reads = requiredReads.filter(
    (requiredPath) => {
      const suffix = normalizeSuffix(requiredPath);
      return !readPaths.some((readPath) =>
        normalizeSuffix(readPath).endsWith(suffix),
      );
    },
  );
  caseResults[index].required_reads_passed =
    caseResults[index].missing_required_reads.length === 0;
}

const requiredReadsApplicable = options.activation !== "baseline";
const requiredReadsPassed =
  !requiredReadsApplicable ||
  caseResults.every((result) => result.required_reads_passed);
const missingRequiredReads = [
  ...new Set(
    caseResults.flatMap((result) => result.missing_required_reads),
  ),
].sort();

const toolNames = collectToolNames(events);
const toolPolicyChecked = options.allowedTools !== null;
const allowedTools = parseToolList(options.allowedTools);
const unauthorizedTools = toolPolicyChecked
  ? toolNames.filter((toolName) => !allowedTools.includes(toolName))
  : [];
const toolPolicyPassed = !toolPolicyChecked || unauthorizedTools.length === 0;

const runtimeStatus =
  options.runExitCode !== null && options.runExitCode !== 0
    ? `pi_exit_${options.runExitCode}`
    : finalMessage
      ? "ok"
      : "missing_final_assistant";

const activationPassed = evaluateActivation({
  activation: options.activation,
  anySkillExpanded,
  anySkillRead,
  skillLocationMatched,
  skillRead,
});
const answerCorrect = caseResults.every((result) => result.answer_correct);

const passed =
  answerCorrect &&
  schemaExact &&
  activationPassed &&
  requiredReadsPassed &&
  toolPolicyPassed &&
  runtimeStatus === "ok" &&
  (!options.requireStrict || strictJsonOnly);

const result = {
  case_id: testCases.length === 1 ? testCases[0].id : null,
  case_ids: testCases.map((testCase) => testCase.id),
  split:
    new Set(testCases.map((testCase) => testCase.split)).size === 1
      ? testCases[0].split
      : "mixed",
  thinking: options.thinking || null,
  activation_mode: options.activation,
  expected: testCases.length === 1 ? testCases[0].answer : null,
  actual: testCases.length === 1 ? caseResults[0].actual : null,
  answer_correct: answerCorrect,
  case_results: caseResults,
  schema_exact: schemaExact,
  strict_json_only: strictJsonOnly,
  activation_passed: activationPassed,
  skill_expanded: skillExpanded,
  skill_location_matched: skillLocationMatched,
  skill_read: skillRead,
  any_skill_expanded: anySkillExpanded,
  any_skill_read: anySkillRead,
  required_reads_applicable: requiredReadsApplicable,
  required_reads_passed: requiredReadsPassed,
  missing_required_reads: missingRequiredReads,
  read_paths: readPaths,
  tool_policy_checked: toolPolicyChecked,
  allowed_tools: allowedTools,
  observed_tools: toolNames,
  unauthorized_tools: unauthorizedTools,
  tool_policy_passed: toolPolicyPassed,
  run_exit_code: options.runExitCode,
  runtime_status: runtimeStatus,
  passed,
};

process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
process.exit(passed ? 0 : 1);

function parseArguments(args) {
  const parsed = {
    manifest: "",
    caseIds: [],
    log: "",
    skillName: "",
    skillPath: "",
    activation: "",
    requireStrict: false,
    thinking: "",
    allowedTools: null,
    runExitCode: null,
  };

  for (let index = 0; index < args.length; index += 1) {
    const argument = args[index];
    if (argument === "--require-strict") {
      parsed.requireStrict = true;
      continue;
    }

    const value = args[index + 1];
    if (!value) {
      fail(`${argument} requires a value`);
    }

    switch (argument) {
      case "--manifest":
        parsed.manifest = value;
        break;
      case "--case":
        parsed.caseIds = value
          .split(",")
          .map((caseId) => caseId.trim())
          .filter(Boolean);
        break;
      case "--log":
        parsed.log = value;
        break;
      case "--skill-name":
        parsed.skillName = value;
        break;
      case "--skill-path":
        parsed.skillPath = value;
        break;
      case "--activation":
        parsed.activation = value;
        break;
      case "--thinking":
        parsed.thinking = value;
        break;
      case "--allowed-tools":
        parsed.allowedTools = value;
        break;
      case "--run-exit-code":
        if (!/^\d+$/.test(value)) {
          fail("--run-exit-code must be a non-negative integer");
        }
        parsed.runExitCode = Number(value);
        break;
      default:
        fail(`Unknown argument: ${argument}`);
    }
    index += 1;
  }

  for (const [field, flag] of [
    ["manifest", "--manifest"],
    ["log", "--log"],
    ["activation", "--activation"],
  ]) {
    if (!parsed[field]) {
      fail(`${flag} is required`);
    }
  }

  if (!["baseline", "forced", "natural"].includes(parsed.activation)) {
    fail("--activation must be baseline, forced, or natural");
  }
  if (parsed.caseIds.length === 0) {
    fail("--case is required");
  }
  if (new Set(parsed.caseIds).size !== parsed.caseIds.length) {
    fail("--case must not contain duplicate ids");
  }
  if (
    parsed.activation !== "baseline" &&
    (!parsed.skillName || !parsed.skillPath)
  ) {
    fail("--skill-name and --skill-path are required for forced and natural activation");
  }

  return parsed;
}

function readJson(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch (error) {
    fail(`Could not read JSON from ${filePath}: ${error.message}`);
  }
}

function readJsonLines(filePath) {
  let contents;
  try {
    contents = fs.readFileSync(filePath, "utf8");
  } catch (error) {
    fail(`Could not read JSONL from ${filePath}: ${error.message}`);
  }

  return contents
    .split(/\r?\n/)
    .filter((line) => line.trim() !== "")
    .map((line, index) => {
      try {
        return JSON.parse(line);
      } catch (error) {
        fail(`Invalid JSON on ${filePath} line ${index + 1}: ${error.message}`);
      }
    });
}

function findFinalAssistantMessage(events) {
  const messages = events.filter(
    (event) =>
      event.type === "message_end" && event.message?.role === "assistant",
  );
  return messages[messages.length - 1] ?? null;
}

function collectText(content) {
  return (content ?? [])
    .filter((item) => item.type === "text")
    .map((item) => item.text ?? "")
    .join("")
    .trim();
}

function collectMessageTexts(events, role) {
  return events
    .filter(
      (event) => event.type === "message_end" && event.message?.role === role,
    )
    .map((event) =>
      (event.message.content ?? [])
        .filter((item) => item.type === "text")
        .map((item) => item.text ?? "")
        .join(""),
    );
}

function collectReadPaths(events) {
  const paths = events
    .filter(
      (event) =>
        event.type === "tool_execution_start" && event.toolName === "read",
    )
    .map(
      (event) =>
        event.args?.path ??
        event.args?.file_path ??
        event.args?.filePath ??
        "",
    )
    .filter(Boolean);

  return [...new Set(paths)].sort();
}

function collectToolNames(events) {
  return [
    ...new Set(
      events
        .filter((event) => event.type === "tool_execution_start")
        .map((event) => event.toolName ?? "")
        .filter(Boolean),
    ),
  ].sort();
}

function extractLastJsonObject(text) {
  let lastObject = null;

  for (let start = 0; start < text.length; start += 1) {
    if (text[start] !== "{") {
      continue;
    }

    let depth = 0;
    let inString = false;
    let escaped = false;

    for (let end = start; end < text.length; end += 1) {
      const character = text[end];

      if (inString) {
        if (escaped) {
          escaped = false;
        } else if (character === "\\") {
          escaped = true;
        } else if (character === '"') {
          inString = false;
        }
        continue;
      }

      if (character === '"') {
        inString = true;
      } else if (character === "{") {
        depth += 1;
      } else if (character === "}") {
        depth -= 1;
        if (depth === 0) {
          const candidate = text.slice(start, end + 1);
          const parsed = parseWholeJsonObject(candidate);
          if (parsed !== null) {
            lastObject = parsed;
          }
          break;
        }
      }
    }
  }

  return lastObject;
}

function parseWholeJsonObject(text) {
  try {
    const parsed = JSON.parse(text);
    return parsed && typeof parsed === "object" && !Array.isArray(parsed)
      ? parsed
      : null;
  } catch {
    return null;
  }
}

function evaluateActivation({
  activation,
  anySkillExpanded,
  anySkillRead,
  skillLocationMatched,
  skillRead,
}) {
  if (activation === "baseline") {
    return !anySkillExpanded && !anySkillRead;
  }
  if (activation === "forced") {
    return skillLocationMatched;
  }
  return skillRead;
}

function normalizeSkillPath(value) {
  if (!value) {
    return "";
  }
  const resolved = path.resolve(value);
  return path.basename(resolved) === "SKILL.md"
    ? resolved
    : path.join(resolved, "SKILL.md");
}

function parseToolList(value) {
  if (value === null) {
    return [];
  }
  if (value === "none" || value.trim() === "") {
    return [];
  }
  return [
    ...new Set(
      value
        .split(",")
        .map((toolName) => toolName.trim())
        .filter(Boolean),
    ),
  ].sort();
}

function normalizeSuffix(value) {
  if (!value) {
    return "";
  }
  return path.normalize(value).replaceAll("\\", "/").replace(/^\.\//, "");
}

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(2);
}
