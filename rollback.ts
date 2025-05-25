#!/usr/bin/env -S deno run --allow-read --allow-write --allow-run --allow-env

/**
 * Dotfiles Rollback Script
 * Restores dotfiles from a backup directory
 */

import { join, basename } from "@std/path";
import { exists } from "@std/fs/exists";
import { copy } from "@std/fs/copy";
import { parseArgs } from "@std/cli/parse-args";

// Colors for output
const colors = {
  red: '\x1b[0;31m',
  green: '\x1b[0;32m',
  yellow: '\x1b[1;33m',
  blue: '\x1b[0;34m',
  reset: '\x1b[0m'
};

interface RollbackConfig {
  backupDir: string;
  homeDir: string;
  shell: string;
}

interface RollbackResult {
  success: boolean;
  filesRestored: string[];
  error?: string;
}

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

async function runCommand(cmd: string[], cwd?: string): Promise<{success: boolean, output: string}> {
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
      output: output.trim()
    };
  } catch (error) {
    return {
      success: false,
      output: error instanceof Error ? error.message : String(error)
    };
  }
}

async function getRollbackConfig(backupDir: string): Promise<RollbackConfig> {
  const homeDir = Deno.env.get("HOME") || Deno.env.get("USERPROFILE") || "";
  const shell = Deno.env.get("SHELL") || "";

  return {
    backupDir,
    homeDir,
    shell
  };
}

async function listAvailableBackups(homeDir: string): Promise<string[]> {
  const backups: string[] = [];
  
  try {
    for await (const dirEntry of Deno.readDir(homeDir)) {
      if (dirEntry.isDirectory && dirEntry.name.startsWith(".dotfiles-backup-")) {
        backups.push(join(homeDir, dirEntry.name));
      }
    }
  } catch {
    // Directory might not exist or be readable
  }
  
  return backups.sort().reverse(); // Most recent first
}

async function validateBackupDirectory(backupDir: string): Promise<boolean> {
  try {
    const stat = await Deno.stat(backupDir);
    return stat.isDirectory;
  } catch {
    return false;
  }
}

async function listBackupContents(backupDir: string): Promise<string[]> {
  const files: string[] = [];
  
  try {
    for await (const dirEntry of Deno.readDir(backupDir)) {
      if (dirEntry.isFile) {
        files.push(dirEntry.name);
      }
    }
  } catch {
    // Directory might not be readable
  }
  
  return files.sort();
}

async function restoreFile(file: string, backupDir: string, homeDir: string): Promise<boolean> {
  const backupFile = join(backupDir, file);
  const homeFile = join(homeDir, file);
  
  try {
    await copy(backupFile, homeFile, { overwrite: true });
    printStatus(`Restored ${file}`);
    return true;
  } catch (error) {
    printWarning(`Could not restore ${file}: ${error instanceof Error ? error.message : String(error)}`);
    return false;
  }
}

async function reloadShell(shell: string, homeDir: string): Promise<void> {
  printBlue("🔃 Reloading shell configuration...");
  
  try {
    if (shell.includes("zsh")) {
      const zshrcPath = join(homeDir, ".zshrc");
      if (await exists(zshrcPath)) {
        await runCommand(["zsh", "-c", `source ${zshrcPath}`]);
      }
      printStatus("Reloaded zsh configuration");
    } else if (shell.includes("bash")) {
      const bashProfilePath = join(homeDir, ".bash_profile");
      if (await exists(bashProfilePath)) {
        await runCommand(["bash", "-c", `source ${bashProfilePath}`]);
      }
      printStatus("Reloaded bash configuration");
    }
  } catch {
    printWarning("Could not reload shell configuration automatically");
  }
}

async function showHelp(homeDir: string): Promise<void> {
  console.log(`
Dotfiles Rollback Script

Usage: deno run --allow-all rollback.ts <backup_directory>

Options:
  -h, --help     Show this help message

Examples:
  deno run --allow-all rollback.ts ~/.dotfiles-backup-20240525-102500
  deno run --allow-all rollback.ts --help
  `);

  const backups = await listAvailableBackups(homeDir);
  if (backups.length > 0) {
    console.log("Available backups:");
    for (const backup of backups) {
      console.log(`  ${backup}`);
    }
  } else {
    console.log("No backups found");
  }
}

async function main(): Promise<void> {
  const args = parseArgs(Deno.args, {
    boolean: ["help"],
    alias: { h: "help" },
    string: ["_"]
  });

  const homeDir = Deno.env.get("HOME") || Deno.env.get("USERPROFILE") || "";

  if (args.help) {
    await showHelp(homeDir);
    return;
  }

  printBlue("🔄 Dotfiles Rollback");
  printBlue("==================");
  console.log();

  // Check if backup directory is provided
  if (args._.length === 0) {
    printError("No backup directory specified!");
    console.log();
    await showHelp(homeDir);
    Deno.exit(1);
  }

  const backupDir = String(args._[0]);

  try {
    const config = await getRollbackConfig(backupDir);

    // Check if backup directory exists
    const isValid = await validateBackupDirectory(backupDir);
    if (!isValid) {
      printError(`Backup directory does not exist: ${backupDir}`);
      console.log();
      await showHelp(homeDir);
      Deno.exit(1);
    }

    console.log(`📂 Backup directory: ${colors.yellow}${backupDir}${colors.reset}`);
    console.log(`🏠 Home directory: ${colors.yellow}${config.homeDir}${colors.reset}`);
    console.log();

    // List files in backup
    printBlue("📋 Files in backup:");
    const backupFiles = await listBackupContents(backupDir);
    
    if (backupFiles.length === 0) {
      printWarning("No files found in backup directory");
      Deno.exit(1);
    }

    for (const file of backupFiles) {
      console.log(`   ${file}`);
    }
    console.log();

    // Confirm rollback
    printYellow("⚠️  This will restore your dotfiles from the backup directory.");
    printYellow("   Current dotfiles will be overwritten!");
    console.log();
    
    const shouldContinue = confirm("Continue with rollback?");
    if (!shouldContinue) {
      printWarning("Rollback cancelled by user");
      Deno.exit(0);
    }

    // Perform rollback
    printBlue("🔄 Restoring files...");
    
    let restoredCount = 0;
    const restoredFiles: string[] = [];
    
    for (const file of backupFiles) {
      const restored = await restoreFile(file, backupDir, config.homeDir);
      if (restored) {
        restoredCount++;
        restoredFiles.push(file);
      }
    }

    // Reload shell configuration
    console.log();
    await reloadShell(config.shell, config.homeDir);

    // Rollback complete
    console.log();
    console.log(`${colors.green}🎉 Rollback completed successfully!${colors.reset}`);
    console.log();
    printBlue("📋 Summary:");
    console.log(`   ✅ Restored ${colors.green}${restoredCount}${colors.reset} files from backup`);
    console.log("   ✅ Reloaded shell configuration");
    console.log();
    printBlue("💡 The backup directory is preserved at:");
    console.log(`   ${colors.yellow}${backupDir}${colors.reset}`);
    console.log();
    console.log(`${colors.green}Your original dotfiles have been restored! 🔄${colors.reset}`);

  } catch (error) {
    printError(`Rollback failed: ${error instanceof Error ? error.message : String(error)}`);
    Deno.exit(1);
  }
}

if (import.meta.main) {
  main();
} 