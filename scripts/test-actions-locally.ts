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

function listWorkflows(): void {
  console.log("\n📋 Available workflows:");

  const workflows = [
    { name: "ci.yml", description: "Main CI workflow (quality, integration tests, smoke tests)" },
    {
      name: "maintenance.yml",
      description: "Maintenance workflow (dependency checks, health checks)",
    },
    { name: "docs.yml", description: "Documentation workflow (markdown validation, stats)" },
  ];

  workflows.forEach((workflow) => {
    console.log(`   ${workflow.name.padEnd(20)} - ${workflow.description}`);
  });
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

async function runWorkflow(options: ActOptions): Promise<void> {
  const { workflow, job, event = "push", platform, verbose, dryRun } = options;

  if (!workflow) {
    console.error("❌ Workflow is required");
    return;
  }

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

  // Run act with real-time output
  const command = new Deno.Command("act", {
    args: actArgs.slice(1),
    stdout: "inherit",
    stderr: "inherit",
  });

  const result = await command.output();

  if (result.success) {
    console.log("\n✅ Workflow completed successfully!");
  } else {
    console.log("\n❌ Workflow failed. Check the output above for details.");
  }
}

function showHelp(): void {
  console.log(`
🎭 Local GitHub Actions Testing with Act

Usage: deno run --allow-all scripts/test-actions-locally.ts [options]

Options:
  -w, --workflow <name>    Workflow file to run (ci.yml, maintenance.yml, docs.yml)
  -j, --job <name>         Specific job to run (optional)
  -e, --event <name>       Event to trigger (default: push)
  -p, --platform <name>    Platform to use (ubuntu-latest, macos-latest, windows-latest)
  -v, --verbose            Enable verbose output
  -d, --dry-run            Show what would be executed without running
  -l, --list-jobs          List jobs in the specified workflow
  --list-workflows         List available workflows
  -h, --help               Show this help

Examples:
  # List available workflows
  deno run --allow-all scripts/test-actions-locally.ts --list-workflows

  # Run the entire CI workflow
  deno run --allow-all scripts/test-actions-locally.ts -w ci.yml

  # Run only the quality job from CI workflow
  deno run --allow-all scripts/test-actions-locally.ts -w ci.yml -j quality

  # Run maintenance workflow with verbose output
  deno run --allow-all scripts/test-actions-locally.ts -w maintenance.yml -v

  # List jobs in the CI workflow
  deno run --allow-all scripts/test-actions-locally.ts -w ci.yml -l

  # Dry run to see what would execute
  deno run --allow-all scripts/test-actions-locally.ts -w docs.yml -d

Common Workflows:
  ci.yml           - Full CI pipeline (code quality, tests, security)
  maintenance.yml  - Dependency and health checks
  docs.yml         - Documentation validation

Tips:
  - First run will be slow (downloading Docker images)
  - Use --dry-run to validate workflow syntax
  - Use --verbose for debugging workflow issues
  - Some jobs may not work perfectly locally (platform differences)
  `);
}

async function main(): Promise<void> {
  const args = parseArgs(Deno.args, {
    string: ["workflow", "job", "event", "platform"],
    boolean: ["verbose", "dry-run", "list-jobs", "list-workflows", "help"],
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

  if (args["list-workflows"]) {
    listWorkflows();
    return;
  }

  // Check prerequisites
  const prereqsOk = await checkPrerequisites();
  if (!prereqsOk) {
    Deno.exit(1);
  }

  if (args["list-jobs"]) {
    if (!args.workflow) {
      console.error("❌ --workflow is required when using --list-jobs");
      Deno.exit(1);
    }
    await listJobs(args.workflow);
    return;
  }

  if (!args.workflow) {
    console.log("No workflow specified. Use --help for usage information.\n");
    listWorkflows();
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
