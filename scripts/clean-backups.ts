#!/usr/bin/env -S deno run --allow-read --allow-write --allow-env

/**
 * Clean up old dotfiles backup directories
 * This script finds and deletes all .dotfiles-backup-* directories in the home directory
 */

import { exists } from "@std/fs/exists";
import { parseArgs } from "@std/cli/parse-args";

// Colors for output
const colors = {
  red: "\x1b[0;31m",
  green: "\x1b[0;32m",
  yellow: "\x1b[1;33m",
  blue: "\x1b[0;34m",
  reset: "\x1b[0m",
};

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

async function findBackupDirectories(): Promise<string[]> {
  const homeDir = Deno.env.get("HOME") || Deno.env.get("USERPROFILE") || "";
  const backupDirs: string[] = [];

  try {
    for await (const entry of Deno.readDir(homeDir)) {
      if (entry.isDirectory && entry.name.startsWith(".dotfiles-backup-")) {
        const fullPath = `${homeDir}/${entry.name}`;
        if (await exists(fullPath)) {
          backupDirs.push(fullPath);
        }
      }
    }
  } catch (error) {
    printError(
      `Failed to read home directory: ${error instanceof Error ? error.message : String(error)}`,
    );
  }

  return backupDirs.sort();
}

async function getDirectorySize(path: string): Promise<number> {
  let totalSize = 0;

  try {
    for await (const entry of Deno.readDir(path)) {
      const fullPath = `${path}/${entry.name}`;
      const stat = await Deno.stat(fullPath);

      if (stat.isFile) {
        totalSize += stat.size;
      } else if (stat.isDirectory) {
        totalSize += await getDirectorySize(fullPath);
      }
    }
  } catch {
    // Ignore errors for individual files
  }

  return totalSize;
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`;
}

async function deleteBackupDirectory(path: string): Promise<boolean> {
  try {
    await Deno.remove(path, { recursive: true });
    return true;
  } catch (error) {
    printError(
      `Failed to delete ${path}: ${error instanceof Error ? error.message : String(error)}`,
    );
    return false;
  }
}

async function main(): Promise<void> {
  const args = parseArgs(Deno.args, {
    boolean: ["help", "force", "dry-run"],
    alias: { h: "help", f: "force", n: "dry-run" },
  });

  if (args.help) {
    console.log(`
Clean Dotfiles Backup Directories

Usage: deno run --allow-all clean-backups.ts [options]

Options:
  -n, --dry-run    Show what would be deleted without actually deleting
  -f, --force      Skip confirmation prompts
  -h, --help       Show this help message

This script will:
  • Find all .dotfiles-backup-* directories in your home directory
  • Show their creation dates and sizes
  • Delete them after confirmation (unless --dry-run is used)
    `);
    return;
  }

  printBlue("🧹 Dotfiles Backup Cleanup");
  printBlue("=========================");
  console.log();

  // Find backup directories
  printBlue("🔍 Searching for backup directories...");
  const backupDirs = await findBackupDirectories();

  if (backupDirs.length === 0) {
    printStatus("No backup directories found!");
    return;
  }

  console.log();
  console.log(`Found ${colors.yellow}${backupDirs.length}${colors.reset} backup directories:`);
  console.log();

  // Calculate sizes and show information
  let totalSize = 0;
  const dirInfo: Array<{ path: string; size: number; date: string }> = [];

  for (const dir of backupDirs) {
    const size = await getDirectorySize(dir);
    totalSize += size;

    // Extract date from directory name
    const match = dir.match(/\.dotfiles-backup-(\d{8})-(\d{6})/);
    let dateStr = "Unknown date";
    if (match) {
      const [, date, time] = match;
      const year = date.substring(0, 4);
      const month = date.substring(4, 6);
      const day = date.substring(6, 8);
      const hour = time.substring(0, 2);
      const minute = time.substring(2, 4);
      const second = time.substring(4, 6);
      dateStr = `${year}-${month}-${day} ${hour}:${minute}:${second}`;
    }

    dirInfo.push({ path: dir, size, date: dateStr });
    console.log(
      `  ${colors.yellow}${dateStr}${colors.reset} - ${formatBytes(size).padStart(10)} - ${
        dir.split("/").pop()
      }`,
    );
  }

  console.log();
  console.log(
    `Total space used: ${colors.yellow}${formatBytes(totalSize)}${colors.reset}`,
  );

  if (args["dry-run"]) {
    console.log();
    printWarning("Dry run mode - no files will be deleted");
    return;
  }

  // Confirm deletion
  if (!args.force) {
    console.log();
    printWarning(
      `This will permanently delete ${backupDirs.length} backup directories`,
    );
    const shouldContinue = confirm("Continue with deletion?");
    if (!shouldContinue) {
      printWarning("Cleanup cancelled by user");
      return;
    }
  }

  // Delete directories
  console.log();
  printBlue("🗑️  Deleting backup directories...");
  let deletedCount = 0;
  let freedSpace = 0;

  for (const info of dirInfo) {
    const success = await deleteBackupDirectory(info.path);
    if (success) {
      deletedCount++;
      freedSpace += info.size;
      printStatus(`Deleted ${info.path.split("/").pop()}`);
    }
  }

  // Summary
  console.log();
  printBlue("📊 Cleanup Summary");
  printBlue("==================");
  console.log(`  Directories found: ${backupDirs.length}`);
  console.log(`  Directories deleted: ${colors.green}${deletedCount}${colors.reset}`);
  console.log(`  Space freed: ${colors.green}${formatBytes(freedSpace)}${colors.reset}`);

  if (deletedCount < backupDirs.length) {
    console.log(
      `  Failed to delete: ${colors.red}${backupDirs.length - deletedCount}${colors.reset}`,
    );
  }

  console.log();
  printStatus("Cleanup completed!");
}

if (import.meta.main) {
  main();
}
