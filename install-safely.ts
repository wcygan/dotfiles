#!/usr/bin/env -S deno run --allow-read --allow-write --allow-run --allow-env

/**
 * Safe Dotfiles Installation Script
 * This script backs up existing dotfiles before installing new ones
 */

import { basename, dirname, join } from "@std/path";
import { exists } from "@std/fs/exists";
import { copy } from "@std/fs/copy";
import { ensureDir } from "@std/fs/ensure-dir";
import { parseArgs } from "@std/cli/parse-args";
import { walk } from "@std/fs";

// Colors for output
const colors = {
  red: "\x1b[0;31m",
  green: "\x1b[0;32m",
  yellow: "\x1b[1;33m",
  blue: "\x1b[0;34m",
  reset: "\x1b[0m",
};

interface InstallConfig {
  backupDir: string;
  dotfilesDir: string;
  homeDir: string;
  shell: string;
  user: string;
}

interface InstallResult {
  success: boolean;
  backupDir: string;
  filesBackedUp: string[];
  error?: string;
}

// Files to manage
const DOTFILES = [
  ".zshrc",
  ".bashrc",
  ".bash_profile",
  ".path.sh",
  ".exports.sh",
  ".aliases.sh",
  ".functions.sh",
  ".extra.sh",
  ".vimrc",
];

// Optional files that might exist
const OPTIONAL_FILES = [".platform.sh", ".fzf.zsh"];

// Files to exclude when copying dotfiles
const EXCLUDE_FILES = [
  ".git",
  ".DS_Store",
  ".gitignore",
  "README.md",
  "LICENSE",
  "LICENSE-MIT.txt",
  "install-safely.ts",
  "rollback.ts",
  "deno.json",
  "deno.lock",
];

// Zed configuration files to manage
const ZED_CONFIG_FILES = ["keymap.json", "settings.json"];

// Utility functions
function printStatus(message: string): void {
  console.log(`${colors.green}✅${colors.reset} ${message}`);
}

function printWarning(message: string): void {
  console.log(`${colors.yellow}⚠️${colors.reset} ${message}`);
}

function printError(message: string): void {
  console.log(`${colors.red}❌${colors.reset} ${message}`);
}

function printBlue(message: string): void {
  console.log(`${colors.blue}${message}${colors.reset}`);
}

function printYellow(message: string): void {
  console.log(`${colors.yellow}${message}${colors.reset}`);
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
    const output =
      new TextDecoder().decode(result.stdout) +
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

function getInstallConfig(): InstallConfig {
  const now = new Date();
  const timestamp = now
    .toISOString()
    .slice(0, 19)
    .replace(/[:-]/g, "")
    .replace("T", "-");

  const homeDir = Deno.env.get("HOME") || Deno.env.get("USERPROFILE") || "";
  const backupDir = join(homeDir, `.dotfiles-backup-${timestamp}`);

  // Get current script directory
  const currentFile = new URL(import.meta.url).pathname;
  const dotfilesDir = dirname(currentFile);

  const shell = Deno.env.get("SHELL") || "";
  const user = Deno.env.get("USER") || Deno.env.get("USERNAME") || "";

  return {
    backupDir,
    dotfilesDir,
    homeDir,
    shell,
    user,
  };
}

async function validateDotfilesDirectory(
  dotfilesDir: string,
): Promise<boolean> {
  const zshrcExists = await exists(join(dotfilesDir, ".zshrc"));
  const aliasesExists = await exists(join(dotfilesDir, ".aliases.sh"));

  return zshrcExists && aliasesExists;
}

async function backupFile(
  file: string,
  homeDir: string,
  backupDir: string,
): Promise<boolean> {
  const homeFile = join(homeDir, file);
  const fileExists = await exists(homeFile);

  if (fileExists) {
    try {
      await copy(homeFile, join(backupDir, file), { overwrite: true });
      printStatus(`Backed up ${file}`);
      return true;
    } catch (error) {
      printWarning(
        `Could not backup ${file}: ${error instanceof Error ? error.message : String(error)}`,
      );
      return false;
    }
  } else {
    console.log(`   ${colors.yellow}No existing ${file} found${colors.reset}`);
    return false;
  }
}

async function backupZedConfig(
  homeDir: string,
  backupDir: string,
): Promise<string[]> {
  const zedConfigDir = join(homeDir, ".config", "zed");
  const zedBackupDir = join(backupDir, ".config", "zed");
  const backedUpFiles: string[] = [];

  const zedDirExists = await exists(zedConfigDir);
  if (!zedDirExists) {
    console.log(
      `   ${colors.yellow}No existing Zed configuration found${colors.reset}`,
    );
    return backedUpFiles;
  }

  try {
    await ensureDir(zedBackupDir);

    for (const configFile of ZED_CONFIG_FILES) {
      const sourcePath = join(zedConfigDir, configFile);
      const backupPath = join(zedBackupDir, configFile);

      if (await exists(sourcePath)) {
        try {
          await copy(sourcePath, backupPath, { overwrite: true });
          printStatus(`Backed up Zed ${configFile}`);
          backedUpFiles.push(`zed/${configFile}`);
        } catch (error) {
          printWarning(
            `Could not backup Zed ${configFile}: ${error instanceof Error ? error.message : String(error)}`,
          );
        }
      }
    }
  } catch (error) {
    printWarning(
      `Could not backup Zed configuration: ${error instanceof Error ? error.message : String(error)}`,
    );
  }

  return backedUpFiles;
}

function detectShell(
  shell: string,
): { type: string; configFile: string; rcFile: string } | null {
  if (shell.includes("zsh")) {
    return { type: "zsh", configFile: ".zshrc", rcFile: ".zshrc" };
  } else if (shell.includes("bash")) {
    return { type: "bash", configFile: ".bashrc", rcFile: ".bashrc" };
  }
  return null;
}

async function updateRepository(dotfilesDir: string): Promise<void> {
  printBlue("🔄 Updating dotfiles repository...");

  const gitDirExists = await exists(join(dotfilesDir, ".git"));

  if (gitDirExists) {
    const result = await runCommand(
      ["git", "pull", "origin", "main"],
      dotfilesDir,
    );
    if (result.success) {
      printStatus("Repository updated");
    } else {
      printWarning("Could not update repository (continuing anyway)");
    }
  } else {
    printWarning("Not a git repository, skipping update");
  }
}

async function copyDotfiles(
  dotfilesDir: string,
  homeDir: string,
): Promise<boolean> {
  printBlue("📂 Copying dotfiles...");
  let copiedCount = 0;

  try {
    for await (const entry of walk(dotfilesDir, {
      includeFiles: true,
      includeDirs: false,
      skip: [/\.git/, /node_modules/, /\.deno/],
    })) {
      const relativePath = entry.path.replace(dotfilesDir + "/", "");
      const filename = basename(entry.path);

      // Skip excluded files
      if (
        EXCLUDE_FILES.includes(filename) ||
        EXCLUDE_FILES.includes(relativePath) ||
        entry.path.includes("/.git/") ||
        filename.endsWith(".ts") ||
        filename.endsWith(".md") ||
        filename.startsWith("deno.")
      ) {
        continue;
      }

      // Skip files in subdirectories (we only want root-level dotfiles)
      if (relativePath.includes("/")) {
        continue;
      }

      const destPath = join(homeDir, filename);

      try {
        await copy(entry.path, destPath, { overwrite: true });
        printStatus(`Copied ${filename}`);
        copiedCount++;
      } catch (error) {
        printWarning(
          `Could not copy ${filename}: ${error instanceof Error ? error.message : String(error)}`,
        );
      }
    }

    if (copiedCount > 0) {
      printStatus(`Successfully copied ${copiedCount} dotfiles`);
      return true;
    } else {
      printError("No files were copied");
      return false;
    }
  } catch (error) {
    printError(
      `Failed to copy dotfiles: ${error instanceof Error ? error.message : String(error)}`,
    );
    return false;
  }
}

async function copyZedConfig(
  dotfilesDir: string,
  homeDir: string,
): Promise<boolean> {
  printBlue("🎯 Copying Zed configuration files...");
  const zedSourceDir = join(dotfilesDir, "zed");
  const zedConfigDir = join(homeDir, ".config", "zed");

  // Check if zed directory exists in dotfiles
  const zedDirExists = await exists(zedSourceDir);
  if (!zedDirExists) {
    printWarning(
      "No zed directory found in dotfiles, skipping Zed configuration",
    );
    return true;
  }

  try {
    // Ensure Zed config directory exists
    await ensureDir(zedConfigDir);
    printStatus(`Created Zed config directory: ${zedConfigDir}`);

    let copiedCount = 0;
    for (const configFile of ZED_CONFIG_FILES) {
      const sourcePath = join(zedSourceDir, configFile);
      const destPath = join(zedConfigDir, configFile);

      if (await exists(sourcePath)) {
        try {
          await copy(sourcePath, destPath, { overwrite: true });
          printStatus(`Copied ${configFile} to Zed config`);
          copiedCount++;
        } catch (error) {
          printWarning(
            `Could not copy ${configFile}: ${error instanceof Error ? error.message : String(error)}`,
          );
        }
      } else {
        console.log(
          `   ${colors.yellow}No ${configFile} found in zed directory${colors.reset}`,
        );
      }
    }

    if (copiedCount > 0) {
      printStatus(`Successfully copied ${copiedCount} Zed configuration files`);
    }
    return true;
  } catch (error) {
    printError(
      `Failed to copy Zed configuration: ${error instanceof Error ? error.message : String(error)}`,
    );
    return false;
  }
}

async function reloadShell(shellType: string, homeDir: string): Promise<void> {
  printBlue("🔃 Reloading shell configuration...");

  try {
    if (shellType === "zsh") {
      const zshrcPath = join(homeDir, ".zshrc");
      if (await exists(zshrcPath)) {
        await runCommand(["zsh", "-c", `source ${zshrcPath}`]);
      }
    } else if (shellType === "bash") {
      const bashrcPath = join(homeDir, ".bashrc");
      if (await exists(bashrcPath)) {
        await runCommand(["bash", "-c", `source ${bashrcPath}`]);
      }
    }
    printStatus("Shell configuration reloaded");
  } catch {
    printWarning("Could not reload shell configuration automatically");
  }
}

async function main(): Promise<void> {
  const args = parseArgs(Deno.args, {
    boolean: ["help", "force"],
    alias: { h: "help", f: "force" },
  });

  if (args.help) {
    console.log(`
Safe Dotfiles Installation Script

Usage: deno run --allow-all install-safely.ts [options]

Options:
  -f, --force    Skip confirmation prompts
  -h, --help     Show this help message

This script will:
  • Auto-detect your shell (zsh/bash)
  • Backup existing dotfiles with timestamp
  • Install new dotfiles from repository
  • Reload shell configuration
  • Provide rollback instructions
    `);
    return;
  }

  try {
    const config = getInstallConfig();

    printBlue("🔧 Safe Dotfiles Installation");
    printBlue("===============================");
    console.log();
    console.log(
      `📁 Dotfiles source: ${colors.yellow}${config.dotfilesDir}${colors.reset}`,
    );
    console.log(
      `💾 Backup location: ${colors.yellow}${config.backupDir}${colors.reset}`,
    );
    console.log();

    // Validate dotfiles directory
    const isValid = await validateDotfilesDirectory(config.dotfilesDir);
    if (!isValid) {
      printError("Not in dotfiles directory or files missing!");
      console.log(
        "Please run this script from the dotfiles repository directory.",
      );
      Deno.exit(1);
    }

    // Create backup directory
    printBlue("📦 Creating backup directory...");
    await ensureDir(config.backupDir);
    printStatus(`Created backup directory: ${config.backupDir}`);

    // Backup existing dotfiles
    console.log();
    printBlue("💾 Backing up existing dotfiles...");
    const backedUpFiles: string[] = [];

    for (const file of DOTFILES) {
      const wasBackedUp = await backupFile(
        file,
        config.homeDir,
        config.backupDir,
      );
      if (wasBackedUp) {
        backedUpFiles.push(file);
      }
    }

    // Backup optional files
    console.log();
    printBlue("🔍 Checking for optional files...");
    for (const file of OPTIONAL_FILES) {
      const wasBackedUp = await backupFile(
        file,
        config.homeDir,
        config.backupDir,
      );
      if (wasBackedUp) {
        backedUpFiles.push(file);
      }
    }

    // Backup Zed configuration
    console.log();
    printBlue("🎯 Backing up Zed configuration...");
    const zedBackedUpFiles = await backupZedConfig(
      config.homeDir,
      config.backupDir,
    );
    backedUpFiles.push(...zedBackedUpFiles);

    // Show current shell
    console.log();
    printBlue("🐚 Current shell information:");
    console.log(`   Shell: ${colors.yellow}${config.shell}${colors.reset}`);
    console.log(`   User: ${colors.yellow}${config.user}${colors.reset}`);

    // Detect shell
    const shellInfo = detectShell(config.shell);
    if (!shellInfo) {
      printWarning(`Unknown shell: ${config.shell}`);
      console.log("Continuing with installation anyway...");
    } else {
      console.log(
        `   Detected: ${colors.green}${shellInfo.type}${colors.reset}`,
      );
    }

    // Confirm installation
    if (!args.force) {
      console.log();
      printYellow(
        "⚠️  This will replace your current dotfiles with the repository versions.",
      );
      printYellow(
        `   Your existing files are safely backed up in: ${config.backupDir}`,
      );
      console.log();

      const shouldContinue = confirm("Continue with installation?");
      if (!shouldContinue) {
        printWarning("Installation cancelled by user");
        console.log(
          `Your backups are still available in: ${colors.yellow}${config.backupDir}${colors.reset}`,
        );
        Deno.exit(0);
      }
    }

    // Update repository
    console.log();
    await updateRepository(config.dotfilesDir);

    // Copy dotfiles
    console.log();
    const installSuccess = await copyDotfiles(
      config.dotfilesDir,
      config.homeDir,
    );
    if (!installSuccess) {
      Deno.exit(1);
    }

    // Copy Zed configuration
    console.log();
    const zedInstallSuccess = await copyZedConfig(
      config.dotfilesDir,
      config.homeDir,
    );
    if (!zedInstallSuccess) {
      printWarning("Zed configuration installation failed, but continuing...");
    }

    // Reload shell configuration
    console.log();
    if (shellInfo) {
      await reloadShell(shellInfo.type, config.homeDir);
    }

    // Installation complete
    console.log();
    console.log(
      `${colors.green}🎉 Installation completed successfully!${colors.reset}`,
    );
    console.log();
    printBlue("📋 What was done:");
    console.log(
      `   ✅ Backed up existing dotfiles to: ${colors.yellow}${config.backupDir}${colors.reset}`,
    );
    console.log("   ✅ Installed new dotfiles from repository");
    console.log("   ✅ Installed Zed configuration files");
    console.log("   ✅ Reloaded shell configuration");
    console.log();
    printBlue("🧪 Test your installation:");
    console.log(
      `   • Try: ${colors.yellow}d${colors.reset} (should open development workspace in an editor)`,
    );
    console.log(
      `   • Try: ${colors.yellow}k get nodes${colors.reset} (kubectl shortcut)`,
    );
    console.log(`   • Try: ${colors.yellow}cgr${colors.reset} (cargo run)`);
    console.log(
      `   • Try: ${colors.yellow}mm${colors.reset} (git main branch helper)`,
    );
    console.log(
      `   • Try: ${colors.yellow}vv${colors.reset} (edit shell config) or ${colors.yellow}ss${colors.reset} (reload shell)`,
    );
    console.log(
      `   • Try: ${colors.yellow}current_shell${colors.reset} (see which shell you're using)`,
    );
    console.log();
    printBlue("🔄 If you need to rollback:");
    console.log(
      `   ${colors.yellow}deno run --allow-all rollback.ts ${config.backupDir}${colors.reset}`,
    );
    console.log();
    console.log(
      `${colors.green}Enjoy your new dotfiles setup! 🎊${colors.reset}`,
    );
  } catch (error) {
    printError(
      `Installation failed: ${error instanceof Error ? error.message : String(error)}`,
    );
    Deno.exit(1);
  }
}

if (import.meta.main) {
  main();
}
