#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { readManifest, validateManifest } from "./validate-eval-manifest.mjs";

const options = parseArguments(process.argv.slice(2));

try {
  if (options.command === "create") {
    createLock(options);
  } else {
    verifyLock(options);
  }
} catch (error) {
  process.stderr.write(`certification-lock.mjs: ${error.message}\n`);
  process.exit(2);
}

function createLock(input) {
  if (fs.existsSync(input.output)) {
    throw new Error(`refusing to overwrite existing lock: ${input.output}`);
  }
  if (isWithin(input.project, input.output)) {
    throw new Error("--output must be outside the target project");
  }

  const snapshot = buildSnapshot(input);
  const temporaryPath = `${input.output}.tmp-${process.pid}`;
  fs.mkdirSync(path.dirname(input.output), { recursive: true });
  fs.writeFileSync(
    temporaryPath,
    `${JSON.stringify(
      {
        version: 1,
        created_at: new Date().toISOString(),
        ...snapshot,
      },
      null,
      2,
    )}\n`,
    { flag: "wx" },
  );
  fs.renameSync(temporaryPath, input.output);
  process.stdout.write(`${JSON.stringify(snapshot, null, 2)}\n`);
}

function verifyLock(input) {
  const expected = readJson(input.lock);
  const actual = buildSnapshot(input);
  const fields = [
    "manifest_path",
    "manifest_sha256",
    "certification_case_ids",
    "skill_path",
    "skill_sha256",
    "project_path",
    "project_git_root",
    "project_head",
    "project_state_sha256",
    "provider",
    "model",
    "pi_version",
    "thinking_levels",
  ];
  const mismatches = [];

  for (const field of fields) {
    if (JSON.stringify(expected[field]) !== JSON.stringify(actual[field])) {
      mismatches.push({
        field,
        expected: expected[field] ?? null,
        actual: actual[field] ?? null,
      });
    }
  }

  const result = {
    valid: mismatches.length === 0,
    lock: input.lock,
    mismatches,
  };
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  process.exit(result.valid ? 0 : 1);
}

function buildSnapshot(input) {
  const { contents, manifest } = readManifest(input.manifest);
  const validation = validateManifest(manifest, { skillDir: input.skill });
  if (!validation.valid) {
    throw new Error(`manifest is invalid: ${validation.errors.join("; ")}`);
  }

  const certificationCaseIds = manifest.cases
    .filter((testCase) => testCase.split === "certification")
    .map((testCase) => testCase.id)
    .sort();
  if (certificationCaseIds.length === 0) {
    throw new Error("manifest has no certification cases");
  }

  const projectState = readProjectState(input.project);
  if (!projectState.gitRoot) {
    throw new Error(
      "target project must be a Git worktree so certification can lock project state",
    );
  }

  return {
    manifest_path: input.manifest,
    manifest_sha256: sha256(contents),
    certification_case_ids: certificationCaseIds,
    skill_path: input.skill,
    skill_sha256: hashDirectory(input.skill),
    project_path: input.project,
    project_git_root: projectState.gitRoot,
    project_head: projectState.head,
    project_state_sha256: projectState.stateSha256,
    provider: input.provider,
    model: input.model,
    pi_version: input.piVersion,
    thinking_levels: normalizeThinkingLevels(input.thinking),
  };
}

function hashDirectory(directory) {
  if (!fs.statSync(directory).isDirectory()) {
    throw new Error(`skill path is not a directory: ${directory}`);
  }

  const entries = [];
  walk(directory, directory, entries);
  const hash = crypto.createHash("sha256");
  for (const entry of entries.sort((left, right) =>
    left.relative.localeCompare(right.relative),
  )) {
    hash.update(entry.relative);
    hash.update("\0");
    hash.update(entry.kind);
    hash.update("\0");
    hash.update(entry.contents);
    hash.update("\0");
  }
  return hash.digest("hex");
}

function walk(root, current, entries) {
  for (const name of fs.readdirSync(current)) {
    const absolute = path.join(current, name);
    const relative = path.relative(root, absolute).replaceAll("\\", "/");
    const stat = fs.lstatSync(absolute);
    if (stat.isDirectory()) {
      walk(root, absolute, entries);
    } else if (stat.isSymbolicLink()) {
      entries.push({
        relative,
        kind: "symlink",
        contents: fs.readlinkSync(absolute),
      });
    } else if (stat.isFile()) {
      entries.push({
        relative,
        kind: "file",
        contents: fs.readFileSync(absolute),
      });
    }
  }
}

function readProjectState(project) {
  try {
    const gitRoot = runGit(project, ["rev-parse", "--show-toplevel"]).trim();
    let head = null;
    try {
      head = runGit(project, ["rev-parse", "HEAD"]).trim();
    } catch {
      head = null;
    }
    const status = runGit(gitRoot, [
      "status",
      "--porcelain=v1",
      "-z",
      "--untracked-files=all",
    ]);
    const diff = runGit(gitRoot, [
      "diff",
      "--binary",
      "--no-ext-diff",
      ...(head ? ["HEAD"] : []),
      "--",
    ]);
    const untracked = runGit(gitRoot, [
      "ls-files",
      "--others",
      "--exclude-standard",
      "-z",
    ])
      .split("\0")
      .filter(Boolean)
      .sort();
    const stateHash = crypto.createHash("sha256");
    stateHash.update(status);
    stateHash.update("\0");
    stateHash.update(diff);
    stateHash.update("\0");
    for (const relativePath of untracked) {
      const absolutePath = path.join(gitRoot, relativePath);
      const stat = fs.lstatSync(absolutePath);
      stateHash.update(relativePath);
      stateHash.update("\0");
      if (stat.isSymbolicLink()) {
        stateHash.update("symlink");
        stateHash.update("\0");
        stateHash.update(fs.readlinkSync(absolutePath));
      } else if (stat.isFile()) {
        stateHash.update("file");
        stateHash.update("\0");
        stateHash.update(fs.readFileSync(absolutePath));
      }
      stateHash.update("\0");
    }
    return {
      gitRoot: path.resolve(gitRoot),
      head,
      stateSha256: stateHash.digest("hex"),
    };
  } catch {
    return {
      gitRoot: null,
      head: null,
      stateSha256: null,
    };
  }
}

function runGit(project, args) {
  return execFileSync("git", ["-C", project, ...args], {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  });
}

function normalizeThinkingLevels(value) {
  const levels = [
    ...new Set(
      value
        .split(",")
        .map((level) => level.trim())
        .filter(Boolean),
    ),
  ].sort();
  if (levels.length === 0) {
    throw new Error("--thinking must contain at least one level");
  }
  return levels;
}

function readJson(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch (error) {
    throw new Error(`could not read JSON from ${filePath}: ${error.message}`);
  }
}

function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function isWithin(parent, candidate) {
  const relative = path.relative(path.resolve(parent), path.resolve(candidate));
  return relative === "" || (!relative.startsWith("..") && !path.isAbsolute(relative));
}

function parseArguments(args) {
  const command = args.shift();
  if (!["create", "verify"].includes(command)) {
    throw new Error(
      "Usage: certification-lock.mjs <create|verify> --manifest <file> --skill <directory> --project <directory> --provider <name> --model <id> --pi-version <version> --thinking <levels> <--output <file>|--lock <file>>",
    );
  }

  const parsed = {
    command,
    manifest: "",
    skill: "",
    project: "",
    provider: "",
    model: "",
    piVersion: "",
    thinking: "",
    output: "",
    lock: "",
  };

  for (let index = 0; index < args.length; index += 2) {
    const flag = args[index];
    const value = args[index + 1];
    if (!value) {
      throw new Error(`${flag} requires a value`);
    }
    const field = {
      "--manifest": "manifest",
      "--skill": "skill",
      "--project": "project",
      "--provider": "provider",
      "--model": "model",
      "--pi-version": "piVersion",
      "--thinking": "thinking",
      "--output": "output",
      "--lock": "lock",
    }[flag];
    if (!field) {
      throw new Error(`unknown argument: ${flag}`);
    }
    parsed[field] = value;
  }

  for (const field of [
    "manifest",
    "skill",
    "project",
    "provider",
    "model",
    "piVersion",
    "thinking",
  ]) {
    if (!parsed[field]) {
      throw new Error(`missing required value: ${field}`);
    }
  }

  parsed.manifest = path.resolve(parsed.manifest);
  parsed.skill = path.resolve(parsed.skill);
  parsed.project = path.resolve(parsed.project);

  if (command === "create") {
    if (!parsed.output) {
      throw new Error("create requires --output");
    }
    parsed.output = path.resolve(parsed.output);
  } else {
    if (!parsed.lock) {
      throw new Error("verify requires --lock");
    }
    parsed.lock = path.resolve(parsed.lock);
  }

  return parsed;
}
