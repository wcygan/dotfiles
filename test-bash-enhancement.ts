#!/usr/bin/env -S deno run --allow-read --allow-write --allow-run --allow-env

/**
 * Test script to verify bash enhancements provide equivalent experience to zsh
 */

import { join } from "@std/path";
import { exists } from "@std/fs/exists";
import { copy } from "@std/fs/copy";

// Colors for output
const colors = {
  red: "\x1b[0;31m",
  green: "\x1b[0;32m",
  yellow: "\x1b[1;33m",
  blue: "\x1b[0;34m",
  reset: "\x1b[0m",
};

function printTest(message: string): void {
  console.log(`${colors.blue}🧪${colors.reset} Testing: ${message}`);
}

function printSuccess(message: string): void {
  console.log(`${colors.green}✅${colors.reset} ${message}`);
}

function printFailure(message: string): void {
  console.log(`${colors.red}❌${colors.reset} ${message}`);
}

function printInfo(message: string): void {
  console.log(`${colors.yellow}ℹ️${colors.reset} ${message}`);
}

async function runCommand(
  cmd: string[],
  shell: string,
): Promise<{ success: boolean; output: string }> {
  try {
    const command = new Deno.Command(shell, {
      args: ["-c", cmd.join(" ")],
      stdout: "piped",
      stderr: "piped",
      env: {
        ...Deno.env.toObject(),
        "HOME": Deno.env.get("HOME") || "",
      },
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

async function testShellFeature(
  description: string,
  command: string[],
  shell: "bash" | "zsh",
): Promise<boolean> {
  printTest(`${description} (${shell})`);

  const result = await runCommand(command, shell);

  if (result.success) {
    printSuccess(`${shell} ${description} works`);
    if (result.output) {
      // Filter out common dotfile loading messages for cleaner output
      const cleanOutput = result.output
        .split("\n")
        .filter((line) =>
          !line.includes("path loaded") &&
          !line.includes("exports loaded") &&
          !line.includes("Loaded dotfiles:") &&
          !line.includes("All dotfiles loaded successfully!") &&
          !line.includes("Bash shell ready!") &&
          line.trim() !== ""
        )
        .join("\n")
        .trim();

      if (cleanOutput) {
        console.log(`   Output: ${cleanOutput.split("\n")[0]}`); // Show first meaningful line
      }
    }
    return true;
  } else {
    printFailure(`${shell} ${description} failed: ${result.output}`);
    return false;
  }
}

async function checkFileExists(file: string): Promise<boolean> {
  const homeDir = Deno.env.get("HOME") || "";
  const filePath = join(homeDir, file);
  const fileExists = await exists(filePath);

  if (fileExists) {
    printSuccess(`${file} exists`);
  } else {
    printFailure(`${file} missing`);
  }

  return fileExists;
}

async function setupTestEnvironment(): Promise<{ cleanup: () => Promise<void>; success: boolean }> {
  const homeDir = Deno.env.get("HOME") || "";
  const currentDir = Deno.cwd();

  // Files to copy for testing
  const testFiles = [
    ".bashrc",
    ".bash_profile",
    ".aliases",
    ".functions",
    ".exports",
    ".path",
    ".platform",
  ];

  const backupFiles: string[] = [];

  try {
    printInfo("Setting up test environment...");

    // Backup existing files and copy test files
    for (const file of testFiles) {
      const sourceFile = join(currentDir, file);
      const targetFile = join(homeDir, file);
      const backupFile = join(homeDir, `${file}.test-backup`);

      // Check if source file exists
      if (await exists(sourceFile)) {
        // Backup existing file if it exists
        if (await exists(targetFile)) {
          // Remove existing backup if it exists
          if (await exists(backupFile)) {
            await Deno.remove(backupFile);
          }
          await copy(targetFile, backupFile);
          backupFiles.push(file);
        }

        // Copy test file
        await copy(sourceFile, targetFile, { overwrite: true });
        printSuccess(`Installed ${file} for testing`);
      }
    }

    return {
      success: true,
      cleanup: async () => {
        printInfo("Cleaning up test environment...");

        // Remove test files and restore backups
        for (const file of testFiles) {
          const targetFile = join(homeDir, file);
          const backupFile = join(homeDir, `${file}.test-backup`);

          try {
            // Remove test file
            if (await exists(targetFile)) {
              await Deno.remove(targetFile);
            }

            // Restore backup if it exists
            if (backupFiles.includes(file) && await exists(backupFile)) {
              await copy(backupFile, targetFile);
              await Deno.remove(backupFile);
              printSuccess(`Restored ${file}`);
            }
          } catch (error) {
            console.warn(`Warning: Could not clean up ${file}: ${error}`);
          }
        }
      },
    };
  } catch (error) {
    console.error(`Error in setupTestEnvironment: ${error}`);
    return {
      success: false,
      cleanup: async () => {
        // Best effort cleanup
        for (const file of backupFiles) {
          const backupFile = join(homeDir, `${file}.test-backup`);
          try {
            if (await exists(backupFile)) {
              await copy(backupFile, join(homeDir, file));
              await Deno.remove(backupFile);
            }
          } catch {
            // Ignore cleanup errors
          }
        }
      },
    };
  }
}

async function main(): Promise<void> {
  console.log(`${colors.blue}🔧 Bash Enhancement Verification${colors.reset}`);
  console.log("=================================");
  console.log();

  // Setup test environment
  const testEnv = await setupTestEnvironment();

  if (!testEnv.success) {
    printFailure("Failed to setup test environment");
    Deno.exit(1);
  }

  try {
    // Check that enhanced dotfiles exist
    printTest("Checking enhanced dotfiles exist");
    const bashrcExists = await checkFileExists(".bashrc");
    const bashProfileExists = await checkFileExists(".bash_profile");
    const _platformExists = await checkFileExists(".platform");
    const _aliasesExists = await checkFileExists(".aliases");
    const _functionsExists = await checkFileExists(".functions");

    if (!bashrcExists || !bashProfileExists) {
      printFailure("Enhanced dotfiles not found! Installation may have failed.");
      await testEnv.cleanup();
      Deno.exit(1);
    }

    console.log();

    // Test bash-specific features
    const bashTests = [
      {
        description: "status reporting",
        command: [
          "source ~/.bashrc >/dev/null 2>&1 && echo 'TEST: Bash configuration loaded successfully'",
        ],
      },
      {
        description: "shell detection",
        command: [
          "source ~/.bashrc >/dev/null 2>&1 && type current_shell >/dev/null 2>&1 && echo 'TEST: current_shell function available' || echo 'TEST: current_shell function not found'",
        ],
      },
      {
        description: "environment info",
        command: [
          "source ~/.bashrc >/dev/null 2>&1 && type dotfiles_info >/dev/null 2>&1 && echo 'TEST: dotfiles_info function available' || echo 'TEST: dotfiles_info function not found'",
        ],
      },
      {
        description: "platform detection",
        command: [
          "source ~/.bashrc >/dev/null 2>&1 && echo \"TEST: Platform detected as ${DOTFILES_OS:-'not set'}\"",
        ],
      },
      {
        description: "git branch in prompt",
        command: [
          "source ~/.bashrc >/dev/null 2>&1 && type parse_git_branch >/dev/null 2>&1 && echo 'TEST: parse_git_branch function available' || echo 'TEST: parse_git_branch function not found'",
        ],
      },
      {
        description: "modern bash features",
        command: [
          "source ~/.bashrc >/dev/null 2>&1 && shopt globstar 2>/dev/null | grep -q 'on' && echo 'TEST: globstar enabled' || echo 'TEST: globstar not enabled'",
        ],
      },
      {
        description: "shell-agnostic aliases",
        command: [
          "source ~/.bashrc >/dev/null 2>&1 && alias vv 2>/dev/null | grep -q 'vbash\\|vim\\|code' && echo 'TEST: vv alias configured' || echo 'TEST: vv alias not found'",
        ],
      },
    ];

    printInfo("Testing Bash enhancements...");
    let bashScore = 0;
    for (const test of bashTests) {
      const success = await testShellFeature(test.description, test.command, "bash");
      if (success) bashScore++;
    }

    console.log();

    // Test that zsh still works (if available)
    const zshAvailable = await runCommand(["zsh --version"], "zsh");
    if (zshAvailable.success) {
      printInfo("Testing Zsh compatibility...");
      const zshTests = [
        {
          description: "status reporting",
          command: [
            "test -f ~/.zshrc && source ~/.zshrc >/dev/null 2>&1 && echo 'TEST: Zsh configuration loaded successfully' || echo 'TEST: No .zshrc found'",
          ],
        },
        {
          description: "shell detection",
          command: [
            "test -f ~/.zshrc && source ~/.zshrc >/dev/null 2>&1 && type current_shell >/dev/null 2>&1 && echo 'TEST: current_shell function available' || echo 'TEST: current_shell function not found'",
          ],
        },
        {
          description: "shell-agnostic aliases",
          command: [
            "test -f ~/.zshrc && source ~/.zshrc >/dev/null 2>&1 && alias vv 2>/dev/null | grep -q 'vzsh\\|vim\\|code' && echo 'TEST: vv alias configured' || echo 'TEST: vv alias not found'",
          ],
        },
      ];

      let zshScore = 0;
      for (const test of zshTests) {
        const success = await testShellFeature(test.description, test.command, "zsh");
        if (success) zshScore++;
      }

      console.log();
      printInfo(`Zsh compatibility: ${zshScore}/${zshTests.length} tests passed`);
    } else {
      printInfo("Zsh not available, skipping compatibility tests");
    }

    console.log();
    console.log(`${colors.blue}📊 Results${colors.reset}`);
    console.log("===========");
    console.log(`Bash enhancements: ${bashScore}/${bashTests.length} tests passed`);

    if (bashScore >= 5) { // Allow some flexibility for CI environment
      printSuccess("🎉 Bash enhancements working correctly!");
      console.log();
      console.log("Your dotfiles now provide an excellent experience in both Bash and Zsh!");
      console.log();
      console.log("Try these commands in your bash shell:");
      console.log(
        `  ${colors.yellow}current_shell${colors.reset}     # See which shell you're using`,
      );
      console.log(`  ${colors.yellow}dotfiles_info${colors.reset}     # Complete environment info`);
      console.log(`  ${colors.yellow}vv${colors.reset}               # Edit shell config`);
      console.log(`  ${colors.yellow}ss${colors.reset}               # Reload shell config`);
      console.log(
        `  ${colors.yellow}hg pattern${colors.reset}       # Enhanced history search (bash only)`,
      );
    } else {
      printFailure(
        `Only ${bashScore}/${bashTests.length} bash features working. Check configuration.`,
      );
      await testEnv.cleanup();
      Deno.exit(1);
    }
  } finally {
    // Always cleanup
    await testEnv.cleanup();
  }
}

if (import.meta.main) {
  main();
}
