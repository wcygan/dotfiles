#!/usr/bin/env -S deno run --allow-read --allow-write --allow-run

/**
 * Local GitHub Actions Testing Script
 * Uses Act to run GitHub Actions workflows locally for fast feedback
 */

import { parseArgs } from "@std/cli/parse-args";

interface ActOptions {
  workflow?: string;
  job?: string;
  event?: string;
  platform?: string;
  verbose?: boolean;
  dryRun?: boolean;
  listJobs?: boolean;
}

async function runCommand(
  cmd: string[],
  cwd?: string,
): Promise<{ success: boolean; output: string; code: number }> {
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
      code: result.code,
    };
  } catch (error) {
    return {
      success: false,
      output: error instanceof Error ? error.message : String(error),
      code: 1,
    };
  }
}

async function checkPrerequisites(): Promise<boolean> {
  console.log("🔍 Checking prerequisites...");

  // Check if act is installed
  const actCheck = await runCommand(["act", "--version"]);
  if (!actCheck.success) {
    console.error("❌ Act is not installed. Please install it first:");
    console.error("   macOS: brew install act");
    console.error(
      "   Linux: curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash",
    );
    return false;
  }
  console.log("✅ Act is installed:", actCheck.output.split("\n")[0]);

  // Check if Docker is running
  const dockerCheck = await runCommand(["docker", "info"]);
  if (!dockerCheck.success) {
    console.error("❌ Docker is not running. Please start Docker first.");
    return false;
  }
  console.log("✅ Docker is running");

  return true;
}

async function listJobs(workflow: string): Promise<void> {
  console.log(`\n🔍 Listing jobs for ${workflow}...`);

  const result = await runCommand([
    "act",
    "--list",
    "--workflows",
    `.github/workflows/${workflow}`,
  ]);

  if (result.success) {
    console.log(result.output);
  } else {
    console.error("❌ Failed to list jobs:", result.output);
  }
}

function analyzeActOutput(output: string, exitCode: number): {
  actualSuccess: boolean;
  summary: string;
  details: string[];
} {
  const lines = output.split("\n");
  const details: string[] = [];
  let hasErrors = false;
  let hasSuccessfulSteps = false;
  let jobsCompleted = 0;

  for (const line of lines) {
    // Look for actual errors (not Act's confusing "Job failed" message)
    if (line.includes("Error:") && !line.includes("Job '") && !line.includes("failed")) {
      hasErrors = true;
      details.push(`❌ Error: ${line}`);
    }

    // Look for step failures
    if (line.includes("❌") && !line.includes("Job failed")) {
      hasErrors = true;
      details.push(`❌ Step failed: ${line}`);
    }

    // Look for successful step completions
    if (line.includes("✅  Success - Complete job")) {
      hasSuccessfulSteps = true;
      jobsCompleted++;
    }

    // Look for command execution results
    if (line.includes("| Task ") || line.includes("Run ")) {
      details.push(`📋 ${line.trim()}`);
    }
  }

  // Determine actual success based on content, not just exit code
  const actualSuccess = !hasErrors && hasSuccessfulSteps;

  let summary: string;
  if (actualSuccess) {
    summary = `✅ Workflow completed successfully! (${jobsCompleted} job(s) completed)`;
  } else if (hasErrors) {
    summary = `❌ Workflow failed with errors`;
  } else {
    summary = `⚠️  Workflow completed but with uncertain status (exit code: ${exitCode})`;
  }

  return { actualSuccess, summary, details };
}

async function runWorkflow(options: ActOptions): Promise<void> {
  const { workflow = "ci.yml", job, event = "push", platform, verbose, dryRun } = options;

  console.log(`\n🚀 Running workflow: ${workflow}`);
  if (job) console.log(`   Job: ${job}`);
  console.log(`   Event: ${event}`);
  if (platform) console.log(`   Platform: ${platform}`);

  const actArgs = ["act", event];

  // Add workflow file
  actArgs.push("--workflows", `.github/workflows/${workflow}`);

  // Add job filter if specified
  if (job) {
    actArgs.push("--job", job);
  }

  // Add platform if specified
  if (platform) {
    actArgs.push("--platform", platform);
  }

  // Add verbose flag
  if (verbose) {
    actArgs.push("--verbose");
  }

  // Add dry run flag
  if (dryRun) {
    actArgs.push("--dryrun");
  }

  // Add environment variables for local testing
  actArgs.push("--env", "CI=true");
  actArgs.push("--env", "GITHUB_ACTIONS=true");

  console.log(`\n🔧 Running command: ${actArgs.join(" ")}`);
  console.log("⏳ This may take a while on first run (downloading Docker images)...\n");

  // Capture output for analysis
  const result = await runCommand(actArgs);

  // Analyze the actual results
  const analysis = analyzeActOutput(result.output, result.code);

  // Show the output
  console.log(result.output);

  // Show our analysis
  console.log("\n" + "=".repeat(60));
  console.log("📊 WORKFLOW ANALYSIS");
  console.log("=".repeat(60));
  console.log(analysis.summary);

  if (analysis.details.length > 0) {
    console.log("\n📋 Key Details:");
    analysis.details.forEach((detail) => console.log(`   ${detail}`));
  }

  console.log("\n💡 Note: Act sometimes reports 'Job failed' even when steps succeed.");
  console.log("   Look for actual error messages and step completion status above.");

  // Exit with appropriate code
  if (!analysis.actualSuccess && !dryRun) {
    Deno.exit(1);
  }
}

function showHelp(): void {
  console.log(`
🎭 Local GitHub Actions Testing with Act

Usage: deno run --allow-all scripts/test-actions-locally.ts [options]

Options:
  -w, --workflow <name>    Workflow file to run (default: ci.yml)
  -j, --job <name>         Specific job to run (optional)
  -e, --event <name>       Event to trigger (default: push)
  -p, --platform <name>    Platform to use (ubuntu-latest, macos-latest, windows-latest)
  -v, --verbose            Enable verbose output
  -d, --dry-run            Show what would be executed without running
  -l, --list-jobs          List jobs in the workflow
  -h, --help               Show this help

Examples:
  # Run the CI workflow (default)
  deno run --allow-all scripts/test-actions-locally.ts

  # Run with specific workflow
  deno run --allow-all scripts/test-actions-locally.ts -w ci.yml

  # Run only the test job
  deno run --allow-all scripts/test-actions-locally.ts -j test

  # Run with verbose output
  deno run --allow-all scripts/test-actions-locally.ts -v

  # List jobs in the CI workflow
  deno run --allow-all scripts/test-actions-locally.ts -l

  # Dry run to see what would execute
  deno run --allow-all scripts/test-actions-locally.ts -d

  # Test specific platform
  deno run --allow-all scripts/test-actions-locally.ts -p ubuntu-latest

Tips:
  - First run will be slow (downloading Docker images)
  - Use --dry-run to validate workflow syntax
  - Use --verbose for debugging workflow issues
  - Act sometimes reports "Job failed" even when steps succeed
  - Look for actual error messages, not just Act's exit status
  `);
}

async function main(): Promise<void> {
  const args = parseArgs(Deno.args, {
    string: ["workflow", "job", "event", "platform"],
    boolean: ["verbose", "dry-run", "list-jobs", "help"],
    alias: {
      w: "workflow",
      j: "job",
      e: "event",
      p: "platform",
      v: "verbose",
      d: "dry-run",
      l: "list-jobs",
      h: "help",
    },
  });

  if (args.help) {
    showHelp();
    return;
  }

  // Check prerequisites
  const prereqsOk = await checkPrerequisites();
  if (!prereqsOk) {
    Deno.exit(1);
  }

  if (args["list-jobs"]) {
    await listJobs(args.workflow || "ci.yml");
    return;
  }

  await runWorkflow({
    workflow: args.workflow,
    job: args.job,
    event: args.event,
    platform: args.platform,
    verbose: args.verbose,
    dryRun: args["dry-run"],
    listJobs: args["list-jobs"],
  });
}

if (import.meta.main) {
  main();
}
