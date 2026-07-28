#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const scoreDirectory = process.argv[2];
if (!scoreDirectory) {
  fail("Usage: summarize-eval.mjs <score-directory>");
}

const files = findScoreFiles(path.resolve(scoreDirectory));
if (files.length === 0) {
  fail(`No .score.json files found under ${scoreDirectory}`);
}

const scores = files.map(readJson);
const groups = new Map();

for (const score of scores) {
  const key = [
    score.activation_mode ?? "unknown",
    score.split ?? "unknown",
    score.thinking ?? "unspecified",
  ].join("|");
  const group = groups.get(key) ?? {
    activation_mode: score.activation_mode ?? "unknown",
    split: score.split ?? "unknown",
    thinking: score.thinking ?? "unspecified",
    cases: 0,
    correct: 0,
    schema_exact: 0,
    activation_passed: 0,
    required_reads_applicable: 0,
    required_reads_passed: 0,
    strict_json_only: 0,
    tool_policy_checked: 0,
    tool_policy_passed: 0,
    runtime_passed: 0,
    passed: 0,
  };

  const caseCount = Array.isArray(score.case_ids) ? score.case_ids.length : 1;
  group.cases += caseCount;
  group.correct += countCaseMetric(score, "answer_correct", caseCount);
  group.schema_exact += score.schema_exact ? caseCount : 0;
  group.activation_passed += score.activation_passed ? caseCount : 0;
  if (score.required_reads_applicable) {
    group.required_reads_applicable += caseCount;
    group.required_reads_passed += score.required_reads_passed ? caseCount : 0;
  }
  group.strict_json_only += score.strict_json_only ? caseCount : 0;
  if (score.tool_policy_checked) {
    group.tool_policy_checked += caseCount;
    group.tool_policy_passed += score.tool_policy_passed ? caseCount : 0;
  }
  group.runtime_passed += score.runtime_status === "ok" ? caseCount : 0;
  group.passed += score.passed ? caseCount : 0;
  groups.set(key, group);
}

const result = {
  overall_passed: scores.every((score) => score.passed === true),
  score_files: files.length,
  groups: [...groups.values()].sort((left, right) =>
    `${left.activation_mode}|${left.split}|${left.thinking}`.localeCompare(
      `${right.activation_mode}|${right.split}|${right.thinking}`,
    ),
  ),
};

process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
process.exit(result.overall_passed ? 0 : 1);

function countCaseMetric(score, field, fallbackCount) {
  if (Array.isArray(score.case_results)) {
    return score.case_results.filter((entry) => entry[field] === true).length;
  }
  return score[field] ? fallbackCount : 0;
}

function findScoreFiles(directory) {
  if (!fs.existsSync(directory)) {
    fail(`Score directory does not exist: ${directory}`);
  }

  const files = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const absolute = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      files.push(...findScoreFiles(absolute));
    } else if (entry.isFile() && entry.name.endsWith(".score.json")) {
      files.push(absolute);
    }
  }
  return files.sort();
}

function readJson(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch (error) {
    fail(`Could not read JSON from ${filePath}: ${error.message}`);
  }
}

function fail(message) {
  process.stderr.write(`summarize-eval.mjs: ${message}\n`);
  process.exit(2);
}
