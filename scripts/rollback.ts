#!/usr/bin/env -S deno run --allow-read --allow-write --allow-run --allow-env

/**
 * Dotfiles Rollback Script
 * This script restores dotfiles from a backup directory
 */

import { join } from "@std/path";
import { exists } from "@std/fs/exists";
import { copy } from "@std/fs/copy";
import { parseArgs } from "@std/cli/parse-args";

// Colors for output
const colors = {
  red: "\x1b[0;31m",
  green: "\x1b[0;32m",
  yellow: "\x1b[1;33m",
  blue: "\x1b[0;34m",
  reset: "\x1b[0m",
};

interface RollbackConfig {
  backupDir: string;
  homeDir: string;
  force: boolean;
}

function printGreen(message: string) {
  console.log(`${colors.green}${message}${colors.reset}`);
}

function printRed(message: string) {
  console.log(`${colors.red}${message}${colors.reset}`);
}

function printYellow(message: string) {
  console.log(`${colors.yellow}${message}${colors.reset}`);
}

function printBlue(message: string) {
  console.log(`${colors.blue}${message}${colors.reset}`);
}

function showHelp() {
  console.log(`
${colors.blue}Dotfiles Rollback Script${colors.reset}

Usage: rollback.ts <backup-directory> [options]

Arguments:
  backup-directory    Path to the backup directory created during installation

Options:
  --force            Skip confirmation prompts
  --help             Show this help message

Examples:
  deno run --allow-all rollback.ts ~/.dotfiles-backup-2023-12-01_14-30-15
  deno run --allow-all rollback.ts ~/.dotfiles-backup-2023-12-01_14-30-15 --force
`);
}

async function promptUser(message: string): Promise<boolean> {
  console.log(`${colors.yellow}${message}${colors.reset}`);
  console.log("Type 'yes' to continue or 'no' to cancel:");

  const buf = new Uint8Array(1024);
  const n = await Deno.stdin.read(buf) ?? 0;
  const input = new TextDecoder().decode(buf.subarray(0, n)).trim().toLowerCase();

  return input === "yes" || input === "y";
}

async function rollbackDotfiles(config: RollbackConfig): Promise<void> {
  const { backupDir, homeDir, force } = config;

  // Verify backup directory exists
  if (!await exists(backupDir)) {
    throw new Error(`Backup directory ${backupDir} does not exist`);
  }

  printBlue("🔄 Starting dotfiles rollback...");
  printYellow(`Backup directory: ${backupDir}`);
  printYellow(`Home directory: ${homeDir}`);

  // Get list of files in backup directory
  const filesToRestore: string[] = [];
  for await (const dirEntry of Deno.readDir(backupDir)) {
    if (dirEntry.isFile && dirEntry.name.startsWith(".")) {
      filesToRestore.push(dirEntry.name);
    }
  }

  if (filesToRestore.length === 0) {
    printYellow("ℹ️  No dotfiles found in backup directory");
    return;
  }

  printBlue(`Found ${filesToRestore.length} files to restore:`);
  for (const file of filesToRestore) {
    console.log(`  • ${file}`);
  }

  // Confirm rollback
  if (!force) {
    const confirmed = await promptUser(
      "\n⚠️  This will overwrite your current dotfiles with the backup versions. Continue?",
    );
    if (!confirmed) {
      printYellow("Rollback cancelled");
      return;
    }
  }

  // Restore files
  let restoredCount = 0;
  for (const file of filesToRestore) {
    const backupFilePath = join(backupDir, file);
    const targetFilePath = join(homeDir, file);

    try {
      // Copy file from backup to home directory
      await copy(backupFilePath, targetFilePath, { overwrite: true });
      printGreen(`✓ Restored ${file}`);
      restoredCount++;
    } catch (error) {
      printRed(
        `✗ Failed to restore ${file}: ${error instanceof Error ? error.message : String(error)}`,
      );
    }
  }

  if (restoredCount === filesToRestore.length) {
    printGreen("\n🎉 Rollback completed successfully!");
    printBlue(`Restored ${restoredCount} dotfiles from backup`);
  } else {
    printYellow(
      `\n⚠️  Partial rollback completed: ${restoredCount}/${filesToRestore.length} files restored`,
    );
  }
}

async function main() {
  try {
    const args = parseArgs(Deno.args, {
      boolean: ["force", "help"],
      alias: {
        h: "help",
        f: "force",
      },
    });

    if (args.help) {
      showHelp();
      return;
    }

    if (args._.length === 0) {
      printRed("Error: Backup directory path is required");
      showHelp();
      Deno.exit(1);
    }

    const backupDir = String(args._[0]);
    const homeDir = Deno.env.get("HOME") || Deno.cwd();
    const force = args.force || false;

    const config: RollbackConfig = {
      backupDir,
      homeDir,
      force,
    };

    await rollbackDotfiles(config);
  } catch (error) {
    printRed(`Error: ${error instanceof Error ? error.message : String(error)}`);
    Deno.exit(1);
  }
}

if (import.meta.main) {
  await main();
}
