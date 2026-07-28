#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

export function readManifest(manifestPath) {
  let contents;
  try {
    contents = fs.readFileSync(manifestPath, "utf8");
  } catch (error) {
    throw new Error(`Could not read ${manifestPath}: ${error.message}`);
  }

  try {
    return { contents, manifest: JSON.parse(contents) };
  } catch (error) {
    throw new Error(`Could not parse JSON from ${manifestPath}: ${error.message}`);
  }
}

export function validateManifest(manifest, options = {}) {
  const errors = [];
  const cases = Array.isArray(manifest?.cases) ? manifest.cases : [];
  const seenIds = new Set();
  const splitCounts = {};
  const answerCountsBySplit = {};

  if (!manifest || typeof manifest !== "object" || Array.isArray(manifest)) {
    errors.push("Manifest root must be a JSON object");
  }
  if (cases.length === 0) {
    errors.push("Manifest must contain at least one case");
  }

  for (const [index, testCase] of cases.entries()) {
    const label = testCase?.id || `case at index ${index}`;

    if (!/^[A-Za-z0-9_-]+$/.test(testCase?.id ?? "")) {
      errors.push(`${label}: id must contain only letters, numbers, underscores, or hyphens`);
    } else if (seenIds.has(testCase.id)) {
      errors.push(`${label}: duplicate case id`);
    } else {
      seenIds.add(testCase.id);
    }

    if (!isAllowedSplit(testCase?.split)) {
      errors.push(
        `${label}: split must be dev, a dev-* subtype, holdout, or certification`,
      );
    } else {
      splitCounts[testCase.split] = (splitCounts[testCase.split] ?? 0) + 1;
    }

    if (typeof testCase?.question !== "string" || testCase.question.trim() === "") {
      errors.push(`${label}: question must be a non-empty string`);
    }

    const choiceEntries =
      testCase?.choices &&
      typeof testCase.choices === "object" &&
      !Array.isArray(testCase.choices)
        ? Object.entries(testCase.choices)
        : [];

    if (choiceEntries.length < 2) {
      errors.push(`${label}: choices must contain at least two options`);
    }

    for (const [choiceLabel, choiceText] of choiceEntries) {
      if (!/^[A-Z]$/.test(choiceLabel)) {
        errors.push(`${label}: invalid choice label ${choiceLabel}`);
      }
      if (typeof choiceText !== "string" || choiceText.trim() === "") {
        errors.push(`${label}: choice ${choiceLabel} must be a non-empty string`);
      }
    }

    if (!Object.hasOwn(testCase?.choices ?? {}, testCase?.answer)) {
      errors.push(`${label}: answer must name one of the available choices`);
    } else if (isAllowedSplit(testCase.split)) {
      answerCountsBySplit[testCase.split] ??= {};
      answerCountsBySplit[testCase.split][testCase.answer] =
        (answerCountsBySplit[testCase.split][testCase.answer] ?? 0) + 1;
    }

    const requiredReads = testCase?.required_reads ?? [];
    if (!Array.isArray(requiredReads)) {
      errors.push(`${label}: required_reads must be an array`);
      continue;
    }

    for (const requiredRead of requiredReads) {
      if (typeof requiredRead !== "string" || requiredRead.trim() === "") {
        errors.push(`${label}: required_reads entries must be non-empty strings`);
        continue;
      }

      const normalized = path.normalize(requiredRead).replaceAll("\\", "/");
      if (
        path.isAbsolute(requiredRead) ||
        normalized === ".." ||
        normalized.startsWith("../")
      ) {
        errors.push(`${label}: required read must stay inside the skill: ${requiredRead}`);
        continue;
      }

      if (options.skillDir) {
        const resolvedRead = path.resolve(options.skillDir, requiredRead);
        if (!isWithin(path.resolve(options.skillDir), resolvedRead)) {
          errors.push(`${label}: required read escapes the skill: ${requiredRead}`);
        } else if (!fs.existsSync(resolvedRead)) {
          errors.push(`${label}: required read does not exist: ${requiredRead}`);
        }
      }
    }
  }

  validateCertificationBalance(cases, errors);

  return {
    valid: errors.length === 0,
    errors,
    case_count: cases.length,
    split_counts: sortedObject(splitCounts),
    answer_counts_by_split: Object.fromEntries(
      Object.entries(answerCountsBySplit)
        .sort(([left], [right]) => left.localeCompare(right))
        .map(([split, counts]) => [split, sortedObject(counts)]),
    ),
  };
}

function isAllowedSplit(split) {
  return (
    split === "holdout" ||
    split === "certification" ||
    /^dev(?:-[a-z0-9]+)*$/.test(split ?? "")
  );
}

function validateCertificationBalance(cases, errors) {
  const certificationCases = cases.filter(
    (testCase) => testCase?.split === "certification",
  );
  if (certificationCases.length < 4) {
    return;
  }

  const choiceLabels = [
    ...new Set(
      certificationCases.flatMap((testCase) =>
        Object.keys(testCase?.choices ?? {}),
      ),
    ),
  ].sort();

  if (choiceLabels.length < 2) {
    return;
  }

  const counts = Object.fromEntries(choiceLabels.map((label) => [label, 0]));
  for (const testCase of certificationCases) {
    if (Object.hasOwn(counts, testCase.answer)) {
      counts[testCase.answer] += 1;
    }
  }

  const values = Object.values(counts);
  if (Math.max(...values) - Math.min(...values) > 1) {
    errors.push(
      `certification answer counts must differ by at most one: ${JSON.stringify(counts)}`,
    );
  }
}

function sortedObject(value) {
  return Object.fromEntries(
    Object.entries(value).sort(([left], [right]) => left.localeCompare(right)),
  );
}

function isWithin(parent, candidate) {
  const relative = path.relative(parent, candidate);
  return relative === "" || (!relative.startsWith("..") && !path.isAbsolute(relative));
}

function parseArguments(args) {
  const manifestPath = args[0];
  let skillDir = "";

  if (!manifestPath || manifestPath.startsWith("-")) {
    throw new Error(
      "Usage: validate-eval-manifest.mjs <manifest.json> [--skill-dir <directory>]",
    );
  }

  for (let index = 1; index < args.length; index += 1) {
    if (args[index] !== "--skill-dir" || !args[index + 1]) {
      throw new Error(`Unknown or incomplete argument: ${args[index]}`);
    }
    skillDir = args[index + 1];
    index += 1;
  }

  return {
    manifestPath: path.resolve(manifestPath),
    skillDir: skillDir ? path.resolve(skillDir) : "",
  };
}

function main() {
  try {
    const options = parseArguments(process.argv.slice(2));
    const { contents, manifest } = readManifest(options.manifestPath);
    const result = validateManifest(manifest, { skillDir: options.skillDir });
    result.manifest_sha256 = crypto
      .createHash("sha256")
      .update(contents)
      .digest("hex");
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    process.exit(result.valid ? 0 : 1);
  } catch (error) {
    process.stderr.write(`validate-eval-manifest.mjs: ${error.message}\n`);
    process.exit(2);
  }
}

if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href
) {
  main();
}
