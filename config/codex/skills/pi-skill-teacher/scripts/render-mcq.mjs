#!/usr/bin/env node

import fs from "node:fs";

const [manifestPath, caseList] = process.argv.slice(2);

if (!manifestPath || !caseList) {
  fail("Usage: render-mcq.mjs <manifest.json> <case-id[,case-id...]>");
}

const manifest = readJson(manifestPath);
const cases = Array.isArray(manifest.cases) ? manifest.cases : [];
const caseIds = caseList
  .split(",")
  .map((caseId) => caseId.trim())
  .filter(Boolean);
if (caseIds.length === 0 || new Set(caseIds).size !== caseIds.length) {
  fail("Case list must contain unique, comma-separated case ids");
}

const testCases = caseIds.map((caseId) =>
  cases.find((entry) => entry.id === caseId),
);
const missingCaseIds = caseIds.filter((_caseId, index) => !testCases[index]);
if (missingCaseIds.length > 0) {
  fail(`Cases not found in ${manifestPath}: ${missingCaseIds.join(", ")}`);
}

for (const testCase of testCases) {
  validateCase(testCase);
}

const prompt = [
  "Role",
  testCases.length === 1
    ? "You are taking one independent multiple-choice evaluation."
    : "You are taking one multiple-choice batch stress evaluation.",
  "",
  "Rules",
  testCases.length === 1
    ? "- Choose exactly one option."
    : "- Choose exactly one option for every question.",
  "- Do not explain the answer.",
  "- Do not inspect project files unless a loaded skill explicitly directs you to one of its bundled resources.",
  `- Return one JSON object with exactly ${formatExpectedKeys(testCases)} and uppercase choice letters as values.`,
  "- Do not add prose or a Markdown fence.",
  "",
  testCases.length === 1 ? "Question" : "Questions",
  ...testCases.flatMap(renderCase),
].join("\n");

process.stdout.write(`${prompt}\n`);

function readJson(path) {
  try {
    return JSON.parse(fs.readFileSync(path, "utf8"));
  } catch (error) {
    fail(`Could not read JSON from ${path}: ${error.message}`);
  }
}

function validateCase(entry) {
  if (!/^[A-Za-z0-9_-]+$/.test(entry.id ?? "")) {
    fail("Case id must contain only letters, numbers, underscores, or hyphens");
  }
  if (typeof entry.question !== "string" || entry.question.trim() === "") {
    fail(`Case ${entry.id} is missing a question`);
  }
  if (!entry.choices || typeof entry.choices !== "object") {
    fail(`Case ${entry.id} is missing choices`);
  }

  const choiceEntries = Object.entries(entry.choices);
  if (choiceEntries.length < 2) {
    fail(`Case ${entry.id} must contain at least two choices`);
  }

  for (const [letter, text] of choiceEntries) {
    if (!/^[A-Z]$/.test(letter)) {
      fail(`Case ${entry.id} has invalid choice label: ${letter}`);
    }
    if (typeof text !== "string" || text.trim() === "") {
      fail(`Case ${entry.id} choice ${letter} is empty`);
    }
  }

  if (!Object.hasOwn(entry.choices, entry.answer)) {
    fail(`Case ${entry.id} answer does not name one of its choices`);
  }
}

function renderCase(testCase, index) {
  const lines = [
    `${testCase.id}. ${testCase.question}`,
    ...Object.entries(testCase.choices).map(
      ([letter, text]) => `${letter}. ${text}`,
    ),
  ];
  return index === 0 ? lines : ["", ...lines];
}

function formatExpectedKeys(testCases) {
  const quoted = testCases.map((testCase) => `"${testCase.id}"`);
  if (quoted.length === 1) {
    return `the key ${quoted[0]}`;
  }
  return `the keys ${quoted.join(", ")}`;
}

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(2);
}
