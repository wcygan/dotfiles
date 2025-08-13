#!/usr/bin/env -S deno run --allow-run --allow-read
/**
 * Git-aware status line script for Claude Code
 * Translated from bash to Deno TypeScript
 */

// Read JSON input from stdin
const input = await new Response(Deno.stdin.readable).text();

try {
  const data = JSON.parse(input);

  // Extract values from JSON
  const modelDisplay = data.model?.display_name || "Claude";
  const currentDir = data.workspace?.current_dir || "";

  // Get directory name (equivalent to ${CURRENT_DIR##*/})
  const dirName = currentDir.split("/").pop() || "";

  // Show git branch if in a git repo
  let gitBranch = "";

  try {
    // Check if we're in a git repository
    const gitCheck = new Deno.Command("git", {
      args: ["rev-parse", "--git-dir"],
      stdout: "null",
      stderr: "null",
    });

    const gitCheckResult = await gitCheck.output();

    if (gitCheckResult.success) {
      // Get current branch
      const branchCmd = new Deno.Command("git", {
        args: ["branch", "--show-current"],
        stdout: "piped",
        stderr: "null",
      });

      const branchResult = await branchCmd.output();

      if (branchResult.success) {
        const branch = new TextDecoder().decode(branchResult.stdout).trim();
        if (branch) {
          gitBranch = ` | 🌿 ${branch}`;
        }
      }
    }
  } catch {
    // Git commands failed, no git branch info
  }

  // Output the status line
  console.log(`[${modelDisplay}] 📁 ${dirName}${gitBranch}`);
} catch (_error) {
  // Fallback if JSON parsing fails
  console.log("[Claude] 📁 Unknown");
}
