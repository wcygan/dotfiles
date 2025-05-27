#!/usr/bin/env -S deno run --allow-read --allow-write --allow-run

/**
 * Pre-commit Check Script
 * Runs essential checks before allowing commits
 */

import { parseArgs } from "@std/cli/parse-args";

async function runCommand(
  cmd: string[],
  cwd?: string,
): Promise<{ success: boolean; output: string }> {
  try {
    const command = new Deno.Command(cmd[0], {
      args: cmd.slice(1),
      cwd,
      stdout: "piped",
      stderr: "piped",
    });

    const result = await command.output();
    const output = new TextDecoder().decode(result.stdout) +
      new TextDecoder().decode(result.stderr);

    return {
      success: result.success,
      output: output.trim(),
    };
  } catch (error) {
    return {
      success: false,
      output: error instanceof Error ? error.message : String(error),
    };
  }
}

async function runCheck(name: string, command: string[]): Promise<boolean> {
  console.log(`🔍 ${name}...`);

  const result = await runCommand(command);

  if (result.success) {
    console.log(`✅ ${name} passed`);
    return true;
  } else {
    console.log(`❌ ${name} failed:`);
    console.log(result.output);
    return false;
  }
}

async function main(): Promise<void> {
  const args = parseArgs(Deno.args, {
    boolean: ["help", "fix"],
    alias: { h: "help", f: "fix" },
  });

  if (args.help) {
    console.log(`
Pre-commit Check Script

Usage: deno run --allow-all scripts/pre-commit-check.ts [options]

Options:
  -f, --fix    Auto-fix formatting issues
  -h, --help   Show this help

This script runs:
  • Type checking
  • Linting
  • Formatting check
  • Tests

If any check fails, the commit should be aborted.
    `);
    return;
  }

  console.log("🚀 Pre-commit checks");
  console.log("====================\n");

  const checks = [
    { name: "Type checking", command: ["deno", "task", "check"] },
    { name: "Linting", command: ["deno", "lint"] },
    { name: "Formatting", command: ["deno", "fmt", "--check"] },
    { name: "Tests", command: ["deno", "task", "test"] },
  ];

  let allPassed = true;
  let formatFailed = false;

  for (const check of checks) {
    const passed = await runCheck(check.name, check.command);

    if (!passed) {
      allPassed = false;

      if (check.name === "Formatting") {
        formatFailed = true;
      }
    }
  }

  if (formatFailed && args.fix) {
    console.log("\n🔧 Auto-fixing formatting...");
    const formatResult = await runCommand(["deno", "fmt"]);

    if (formatResult.success) {
      console.log("✅ Formatting fixed");
      console.log("📝 Please stage the formatting changes and commit again");
    } else {
      console.log("❌ Failed to fix formatting");
    }
  }

  console.log("\n" + "=".repeat(40));

  if (allPassed) {
    console.log("✅ All pre-commit checks passed!");
    console.log("🚀 Ready to commit");
  } else {
    console.log("❌ Pre-commit checks failed");
    console.log("🛑 Please fix the issues above before committing");

    if (formatFailed && !args.fix) {
      console.log("\n💡 Tip: Use --fix to auto-fix formatting issues");
    }

    Deno.exit(1);
  }
}

if (import.meta.main) {
  main();
}
