#!/usr/bin/env -S deno run --allow-read --allow-write --allow-run --allow-env

/**
 * CI Environment Check Script
 * Validates that the environment is properly set up for CI/CD
 */

import { parseArgs } from "@std/cli/parse-args";
import { exists } from "@std/fs/exists";

interface CheckResult {
  name: string;
  success: boolean;
  message: string;
  critical: boolean;
}

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

async function checkDenoInstallation(): Promise<CheckResult> {
  const result = await runCommand(["deno", "--version"]);

  if (result.success) {
    const version = result.output.split("\n")[0];
    return {
      name: "Deno Installation",
      success: true,
      message: `✅ ${version}`,
      critical: true,
    };
  } else {
    return {
      name: "Deno Installation",
      success: false,
      message: "❌ Deno not found or not working",
      critical: true,
    };
  }
}

async function checkDenoJson(): Promise<CheckResult> {
  const denoJsonExists = await exists("deno.json");

  if (!denoJsonExists) {
    return {
      name: "deno.json Configuration",
      success: false,
      message: "❌ deno.json not found",
      critical: true,
    };
  }

  try {
    const content = await Deno.readTextFile("deno.json");
    const config = JSON.parse(content);

    const requiredTasks = ["check", "test", "test:bash"];
    const missingTasks = requiredTasks.filter((task) => !config.tasks?.[task]);

    if (missingTasks.length > 0) {
      return {
        name: "deno.json Configuration",
        success: false,
        message: `❌ Missing tasks: ${missingTasks.join(", ")}`,
        critical: true,
      };
    }

    return {
      name: "deno.json Configuration",
      success: true,
      message: "✅ All required tasks defined",
      critical: true,
    };
  } catch (error) {
    return {
      name: "deno.json Configuration",
      success: false,
      message: `❌ Invalid JSON: ${error instanceof Error ? error.message : String(error)}`,
      critical: true,
    };
  }
}

async function checkRequiredFiles(): Promise<CheckResult> {
  const requiredFiles = [
    "install-safely.ts",
    "rollback.ts",
    "integration-test.ts",
    "test-bash-enhancement.ts",
  ];

  const missingFiles = [];

  for (const file of requiredFiles) {
    if (!await exists(file)) {
      missingFiles.push(file);
    }
  }

  if (missingFiles.length > 0) {
    return {
      name: "Required Files",
      success: false,
      message: `❌ Missing files: ${missingFiles.join(", ")}`,
      critical: true,
    };
  }

  return {
    name: "Required Files",
    success: true,
    message: "✅ All required files present",
    critical: false,
  };
}

async function checkTypeChecking(): Promise<CheckResult> {
  const result = await runCommand(["deno", "task", "check"]);

  if (result.success) {
    return {
      name: "Type Checking",
      success: true,
      message: "✅ Type checking passed",
      critical: true,
    };
  } else {
    return {
      name: "Type Checking",
      success: false,
      message: `❌ Type checking failed: ${result.output}`,
      critical: true,
    };
  }
}

async function checkLinting(): Promise<CheckResult> {
  const result = await runCommand(["deno", "lint"]);

  if (result.success) {
    return {
      name: "Linting",
      success: true,
      message: "✅ Linting passed",
      critical: false,
    };
  } else {
    return {
      name: "Linting",
      success: false,
      message: `❌ Linting failed: ${result.output}`,
      critical: false,
    };
  }
}

async function checkFormatting(): Promise<CheckResult> {
  const result = await runCommand(["deno", "fmt", "--check"]);

  if (result.success) {
    return {
      name: "Formatting",
      success: true,
      message: "✅ Formatting is correct",
      critical: false,
    };
  } else {
    return {
      name: "Formatting",
      success: false,
      message: "❌ Formatting issues found (run 'deno fmt' to fix)",
      critical: false,
    };
  }
}

async function checkTests(): Promise<CheckResult> {
  const result = await runCommand(["deno", "task", "test"]);

  if (result.success) {
    return {
      name: "Tests",
      success: true,
      message: "✅ Tests passed",
      critical: true,
    };
  } else {
    return {
      name: "Tests",
      success: false,
      message: `❌ Tests failed: ${result.output}`,
      critical: true,
    };
  }
}

async function checkBashEnhancements(): Promise<CheckResult> {
  // Skip on Windows
  if (Deno.build.os === "windows") {
    return {
      name: "Bash Enhancements",
      success: true,
      message: "⏭️ Skipped on Windows",
      critical: false,
    };
  }

  const result = await runCommand(["deno", "task", "test:bash"]);

  if (result.success) {
    return {
      name: "Bash Enhancements",
      success: true,
      message: "✅ Bash enhancement tests passed",
      critical: false,
    };
  } else {
    return {
      name: "Bash Enhancements",
      success: false,
      message: `❌ Bash enhancement tests failed: ${result.output}`,
      critical: false,
    };
  }
}

function checkEnvironmentVariables(): CheckResult {
  const isCI = Deno.env.get("CI") === "true";
  const isGitHubActions = Deno.env.get("GITHUB_ACTIONS") === "true";

  if (isCI || isGitHubActions) {
    return {
      name: "CI Environment",
      success: true,
      message: `✅ Running in CI (CI=${isCI}, GITHUB_ACTIONS=${isGitHubActions})`,
      critical: false,
    };
  } else {
    return {
      name: "CI Environment",
      success: true,
      message: "ℹ️ Running locally (not in CI)",
      critical: false,
    };
  }
}

function showHelp(): void {
  console.log(`
CI Environment Check Script

Usage: deno run --allow-all scripts/ci-environment-check.ts [options]

Options:
  --fix              Attempt to fix non-critical issues
  --critical-only    Only run critical checks
  -h, --help         Show this help

This script validates:
  • Deno installation and version
  • deno.json configuration
  • Required files presence
  • Type checking
  • Linting
  • Formatting
  • Tests
  • Bash enhancements (non-Windows)
  • Environment variables

Exit codes:
  0 - All checks passed
  1 - Critical checks failed
  2 - Non-critical checks failed
  `);
}

async function main(): Promise<void> {
  const args = parseArgs(Deno.args, {
    boolean: ["help", "fix", "critical-only"],
    alias: { h: "help" },
  });

  if (args.help) {
    showHelp();
    return;
  }

  console.log("🔍 CI Environment Check");
  console.log("========================\n");

  const checks = [
    checkDenoInstallation,
    checkDenoJson,
    checkRequiredFiles,
    checkTypeChecking,
    checkLinting,
    checkFormatting,
    checkTests,
    checkBashEnhancements,
    checkEnvironmentVariables,
  ];

  const results: CheckResult[] = [];

  for (const check of checks) {
    const result = check === checkEnvironmentVariables ? check() : await check();
    results.push(result);

    // Skip non-critical checks if requested
    if (args["critical-only"] && !result.critical) {
      continue;
    }

    console.log(`${result.message}`);
  }

  console.log("\n" + "=".repeat(50));

  const criticalFailures = results.filter((r) => !r.success && r.critical);
  const nonCriticalFailures = results.filter((r) => !r.success && !r.critical);
  const totalChecks = args["critical-only"]
    ? results.filter((r) => r.critical).length
    : results.length;
  const passedChecks = results.filter((r) => r.success).length;

  console.log(`📊 Summary: ${passedChecks}/${totalChecks} checks passed`);

  if (criticalFailures.length > 0) {
    console.log(`❌ ${criticalFailures.length} critical failure(s)`);
    console.log("\nCritical issues must be fixed before CI will pass:");
    criticalFailures.forEach((f) => console.log(`   • ${f.name}: ${f.message}`));
    Deno.exit(1);
  }

  if (nonCriticalFailures.length > 0) {
    console.log(`⚠️ ${nonCriticalFailures.length} non-critical issue(s)`);
    if (args.fix) {
      console.log("\n🔧 Attempting to fix non-critical issues...");

      // Auto-fix formatting
      const formatIssue = nonCriticalFailures.find((f) => f.name === "Formatting");
      if (formatIssue) {
        console.log("   Fixing formatting...");
        await runCommand(["deno", "fmt"]);
        console.log("   ✅ Formatting fixed");
      }
    } else {
      console.log("\nNon-critical issues (use --fix to auto-fix):");
      nonCriticalFailures.forEach((f) => console.log(`   • ${f.name}: ${f.message}`));
    }
    Deno.exit(2);
  }

  console.log("✅ All checks passed! CI should succeed.");
}

if (import.meta.main) {
  main();
}
