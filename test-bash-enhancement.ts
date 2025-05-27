#!/usr/bin/env -S deno run --allow-read --allow-write --allow-run --allow-env

/**
 * Test script to verify bash enhancements provide equivalent experience to zsh
 */

import { join } from "@std/path";
import { exists } from "@std/fs/exists";

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
      console.log(`   Output: ${result.output.split("\n")[0]}`); // Show first line only
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

async function main(): Promise<void> {
  console.log(`${colors.blue}🔧 Bash Enhancement Verification${colors.reset}`);
  console.log("=================================");
  console.log();

  // Check that enhanced dotfiles exist
  printTest("Checking enhanced dotfiles exist");
  const bashrcExists = await checkFileExists(".bashrc");
  const bashProfileExists = await checkFileExists(".bash_profile");
  const _platformExists = await checkFileExists(".platform");
  const _aliasesExists = await checkFileExists(".aliases");
  const _functionsExists = await checkFileExists(".functions");

  if (!bashrcExists || !bashProfileExists) {
    printFailure("Enhanced dotfiles not found! Run install script first.");
    Deno.exit(1);
  }

  console.log();

  // Test bash-specific features
  const bashTests = [
    {
      description: "status reporting",
      command: ["source ~/.bashrc && echo 'Bash loaded'"],
    },
    {
      description: "shell detection",
      command: ["source ~/.bashrc && current_shell"],
    },
    {
      description: "environment info",
      command: ["source ~/.bashrc && dotfiles_info | head -5"],
    },
    {
      description: "platform detection",
      command: ["source ~/.bashrc && echo $DOTFILES_OS"],
    },
    {
      description: "git branch in prompt",
      command: ["source ~/.bashrc && echo $PS1 | grep -o 'parse_git_branch'"],
    },
    {
      description: "modern bash features",
      command: ["source ~/.bashrc && shopt globstar | grep -q 'on' && echo 'globstar enabled'"],
    },
    {
      description: "shell-agnostic aliases",
      command: ["source ~/.bashrc && alias vv | grep vbash"],
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
        command: ["source ~/.zshrc && echo 'Zsh loaded'"],
      },
      {
        description: "shell detection",
        command: ["source ~/.zshrc && current_shell"],
      },
      {
        description: "shell-agnostic aliases",
        command: ["source ~/.zshrc && alias vv | grep vzsh"],
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

  if (bashScore === bashTests.length) {
    printSuccess("🎉 All bash enhancements working correctly!");
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
    Deno.exit(1);
  }
}

if (import.meta.main) {
  main();
}
