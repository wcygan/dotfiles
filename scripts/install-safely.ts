#!/usr/bin/env -S deno run --allow-read --allow-write --allow-run --allow-env

/**
 * Safe Dotfiles Installation Script
 * This script backs up existing dotfiles before installing new ones
 */

import { dirname, join } from "@std/path";
import { exists } from "@std/fs/exists";
import { copy } from "@std/fs/copy";
import { ensureDir } from "@std/fs/ensure-dir";
import { parseArgs } from "@std/cli/parse-args";

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

// File mappings from source to destination
const FILE_MAPPINGS: Record<string, string> = {
  "shell/bash/bashrc": ".bashrc",
  "shell/bash/bash_profile": ".bash_profile",
  "shell/zsh/zshrc": ".zshrc",
  "shell/common/aliases.sh": ".aliases.sh",
  "shell/common/exports.sh": ".exports.sh",
  "shell/common/functions.sh": ".functions.sh",
  "shell/common/path.sh": ".path.sh",
  "shell/common/extra.sh": ".extra.sh",
  "shell/common/platform.sh": ".platform.sh",
  "shell/vim/vimrc": ".vimrc",
  "tmux/tmux.conf": ".tmux.conf",
};

// Files to manage (for backward compatibility)
const DOTFILES = Object.values(FILE_MAPPINGS);

// Optional files that might exist
const OPTIONAL_FILES = [".fzf.zsh"];

// Zed configuration files to manage
const ZED_CONFIG_FILES = ["keymap.json", "settings.json", "tasks.json"];

// Claude configuration files to manage
const CLAUDE_CONFIG_FILES = ["CLAUDE.md", "settings.json", "mcp.json"];

// Claude commands directory to manage
const CLAUDE_COMMANDS_DIR = "commands";

// Claude agents directory to manage
const CLAUDE_AGENTS_DIR = "agents";

// Gemini configuration files to manage
const GEMINI_CONFIG_FILES = ["GEMINI.md", "settings.json"];

// Ghostty configuration file
const GHOSTTY_CONFIG_FILE = "config";

// GitHub prompts directory name
const GITHUB_PROMPTS_DIR = "github/prompts";

// Scripts directory name
const SCRIPTS_DIR = "tools";

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

function getInstallConfig(): InstallConfig {
  const now = new Date();
  const timestamp = now
    .toISOString()
    .slice(0, 19)
    .replace(/[:-]/g, "")
    .replace("T", "-");

  const homeDir = Deno.env.get("HOME") || Deno.env.get("USERPROFILE") || "";
  const backupDir = join(homeDir, `.dotfiles-backup-${timestamp}`);

  // Get current script directory and go up one level to get dotfiles root
  const currentFile = new URL(import.meta.url).pathname;
  const scriptsDir = dirname(currentFile);
  const dotfilesDir = dirname(scriptsDir);

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
  // Check if the shell directory structure exists
  const shellDirExists = await exists(join(dotfilesDir, "shell"));
  const zshrcExists = await exists(join(dotfilesDir, "shell", "zsh", "zshrc"));
  const aliasesExists = await exists(
    join(dotfilesDir, "shell", "common", "aliases.sh"),
  );

  return shellDirExists && (zshrcExists || aliasesExists);
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
            `Could not backup Zed ${configFile}: ${
              error instanceof Error ? error.message : String(error)
            }`,
          );
        }
      }
    }
  } catch (error) {
    printWarning(
      `Could not backup Zed configuration: ${
        error instanceof Error ? error.message : String(error)
      }`,
    );
  }

  return backedUpFiles;
}

async function backupClaudeConfig(
  homeDir: string,
  backupDir: string,
): Promise<string[]> {
  const claudeConfigDir = join(homeDir, ".claude");
  const claudeBackupDir = join(backupDir, ".claude");
  const backedUpFiles: string[] = [];

  const claudeDirExists = await exists(claudeConfigDir);
  if (!claudeDirExists) {
    console.log(
      `   ${colors.yellow}No existing Claude configuration found${colors.reset}`,
    );
    return backedUpFiles;
  }

  try {
    await ensureDir(claudeBackupDir);

    // Backup individual config files
    for (const configFile of CLAUDE_CONFIG_FILES) {
      const sourcePath = join(claudeConfigDir, configFile);
      const backupPath = join(claudeBackupDir, configFile);

      if (await exists(sourcePath)) {
        try {
          await copy(sourcePath, backupPath, { overwrite: true });
          printStatus(`Backed up Claude ${configFile}`);
          backedUpFiles.push(`claude/${configFile}`);
        } catch (error) {
          printWarning(
            `Could not backup Claude ${configFile}: ${
              error instanceof Error ? error.message : String(error)
            }`,
          );
        }
      }
    }

    // Backup commands directory if it exists
    const commandsSourceDir = join(claudeConfigDir, CLAUDE_COMMANDS_DIR);
    const commandsBackupDir = join(claudeBackupDir, CLAUDE_COMMANDS_DIR);

    if (await exists(commandsSourceDir)) {
      try {
        await copy(commandsSourceDir, commandsBackupDir, { overwrite: true });
        printStatus(`Backed up Claude commands directory`);
        backedUpFiles.push(`claude/${CLAUDE_COMMANDS_DIR}`);
      } catch (error) {
        printWarning(
          `Could not backup Claude commands directory: ${
            error instanceof Error ? error.message : String(error)
          }`,
        );
      }
    }

    // Backup agents directory if it exists
    const agentsSourceDir = join(claudeConfigDir, CLAUDE_AGENTS_DIR);
    const agentsBackupDir = join(claudeBackupDir, CLAUDE_AGENTS_DIR);

    if (await exists(agentsSourceDir)) {
      try {
        await copy(agentsSourceDir, agentsBackupDir, { overwrite: true });
        printStatus(`Backed up Claude agents directory`);
        backedUpFiles.push(`claude/${CLAUDE_AGENTS_DIR}`);
      } catch (error) {
        printWarning(
          `Could not backup Claude agents directory: ${
            error instanceof Error ? error.message : String(error)
          }`,
        );
      }
    }
  } catch (error) {
    printWarning(
      `Could not backup Claude configuration: ${
        error instanceof Error ? error.message : String(error)
      }`,
    );
  }

  return backedUpFiles;
}

async function backupGeminiConfig(
  homeDir: string,
  backupDir: string,
): Promise<string[]> {
  const geminiConfigDir = join(homeDir, ".gemini");
  const geminiBackupDir = join(backupDir, ".gemini");
  const backedUpFiles: string[] = [];

  const geminiDirExists = await exists(geminiConfigDir);
  if (!geminiDirExists) {
    console.log(
      `   ${colors.yellow}No existing Gemini configuration found${colors.reset}`,
    );
    return backedUpFiles;
  }

  try {
    await ensureDir(geminiBackupDir);

    // Backup individual config files
    for (const configFile of GEMINI_CONFIG_FILES) {
      const sourcePath = join(geminiConfigDir, configFile);
      const backupPath = join(geminiBackupDir, configFile);

      if (await exists(sourcePath)) {
        try {
          await copy(sourcePath, backupPath, { overwrite: true });
          printStatus(`Backed up Gemini ${configFile}`);
          backedUpFiles.push(`gemini/${configFile}`);
        } catch (error) {
          printWarning(
            `Could not backup Gemini ${configFile}: ${
              error instanceof Error ? error.message : String(error)
            }`,
          );
        }
      }
    }
  } catch (error) {
    printWarning(
      `Could not backup Gemini configuration: ${
        error instanceof Error ? error.message : String(error)
      }`,
    );
  }

  return backedUpFiles;
}

async function backupGhosttyConfig(
  homeDir: string,
  backupDir: string,
): Promise<string[]> {
  const ghosttyConfigDir = join(
    homeDir,
    "Library",
    "Application Support",
    "com.mitchellh.ghostty",
  );
  const ghosttyBackupDir = join(
    backupDir,
    "Library",
    "Application Support",
    "com.mitchellh.ghostty",
  );
  const backedUpFiles: string[] = [];

  const ghosttyConfigExists = await exists(
    join(ghosttyConfigDir, GHOSTTY_CONFIG_FILE),
  );
  if (!ghosttyConfigExists) {
    console.log(
      `   ${colors.yellow}No existing Ghostty configuration found${colors.reset}`,
    );
    return backedUpFiles;
  }

  try {
    await ensureDir(ghosttyBackupDir);

    const sourcePath = join(ghosttyConfigDir, GHOSTTY_CONFIG_FILE);
    const backupPath = join(ghosttyBackupDir, GHOSTTY_CONFIG_FILE);

    try {
      await copy(sourcePath, backupPath, { overwrite: true });
      printStatus(`Backed up Ghostty ${GHOSTTY_CONFIG_FILE}`);
      backedUpFiles.push(`ghostty/${GHOSTTY_CONFIG_FILE}`);
    } catch (error) {
      printWarning(
        `Could not backup Ghostty ${GHOSTTY_CONFIG_FILE}: ${
          error instanceof Error ? error.message : String(error)
        }`,
      );
    }
  } catch (error) {
    printWarning(
      `Could not backup Ghostty configuration: ${
        error instanceof Error ? error.message : String(error)
      }`,
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
    // Copy files based on the file mappings
    for (const [sourcePath, destFile] of Object.entries(FILE_MAPPINGS)) {
      const sourceFullPath = join(dotfilesDir, sourcePath);
      const destFullPath = join(homeDir, destFile);

      if (await exists(sourceFullPath)) {
        try {
          await copy(sourceFullPath, destFullPath, { overwrite: true });
          printStatus(`Copied ${destFile}`);
          copiedCount++;
        } catch (error) {
          printWarning(
            `Could not copy ${destFile}: ${error instanceof Error ? error.message : String(error)}`,
          );
        }
      } else {
        printWarning(`Source file not found: ${sourcePath}`);
      }
    }

    // Also check for optional files in the shell directory structure
    for (const optFile of OPTIONAL_FILES) {
      // Check in common directory first
      let sourcePath = join(
        dotfilesDir,
        "shell",
        "common",
        optFile.substring(1),
      );
      if (!(await exists(sourcePath))) {
        // Try root directory for backward compatibility
        sourcePath = join(dotfilesDir, optFile);
      }

      if (await exists(sourcePath)) {
        const destPath = join(homeDir, optFile);
        try {
          await copy(sourcePath, destPath, { overwrite: true });
          printStatus(`Copied optional file: ${optFile}`);
          copiedCount++;
        } catch (error) {
          printWarning(
            `Could not copy ${optFile}: ${error instanceof Error ? error.message : String(error)}`,
          );
        }
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
            `Could not copy ${configFile}: ${
              error instanceof Error ? error.message : String(error)
            }`,
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

async function copyClaudeConfig(
  dotfilesDir: string,
  homeDir: string,
): Promise<boolean> {
  printBlue("🤖 Copying Claude configuration files...");
  const claudeSourceDir = join(dotfilesDir, "claude");
  const claudeConfigDir = join(homeDir, ".claude");

  // Check if claude directory exists in dotfiles
  const claudeDirExists = await exists(claudeSourceDir);
  if (!claudeDirExists) {
    printWarning(
      "No claude directory found in dotfiles, skipping Claude configuration",
    );
    return true;
  }

  try {
    // Ensure Claude config directory exists
    await ensureDir(claudeConfigDir);
    printStatus(`Created Claude config directory: ${claudeConfigDir}`);

    let copiedCount = 0;

    // Copy individual config files
    for (const configFile of CLAUDE_CONFIG_FILES) {
      const sourcePath = join(claudeSourceDir, configFile);
      const destPath = join(claudeConfigDir, configFile);

      if (await exists(sourcePath)) {
        try {
          await copy(sourcePath, destPath, { overwrite: true });
          printStatus(`Copied ${configFile} to Claude config`);
          copiedCount++;
        } catch (error) {
          printWarning(
            `Could not copy ${configFile}: ${
              error instanceof Error ? error.message : String(error)
            }`,
          );
        }
      } else {
        console.log(
          `   ${colors.yellow}No ${configFile} found in claude directory${colors.reset}`,
        );
      }
    }

    // Copy commands directory if it exists
    const commandsSourceDir = join(claudeSourceDir, CLAUDE_COMMANDS_DIR);
    const commandsDestDir = join(claudeConfigDir, CLAUDE_COMMANDS_DIR);

    if (await exists(commandsSourceDir)) {
      try {
        await copy(commandsSourceDir, commandsDestDir, { overwrite: true });
        printStatus(`Copied Claude commands directory`);
        copiedCount++;
      } catch (error) {
        printWarning(
          `Could not copy Claude commands directory: ${
            error instanceof Error ? error.message : String(error)
          }`,
        );
      }
    } else {
      console.log(
        `   ${colors.yellow}No commands directory found in claude directory${colors.reset}`,
      );
    }

    // Copy agents directory if it exists
    const agentsSourceDir = join(claudeSourceDir, CLAUDE_AGENTS_DIR);
    const agentsDestDir = join(claudeConfigDir, CLAUDE_AGENTS_DIR);

    if (await exists(agentsSourceDir)) {
      try {
        await copy(agentsSourceDir, agentsDestDir, { overwrite: true });
        printStatus(`Copied Claude agents directory`);
        copiedCount++;
      } catch (error) {
        printWarning(
          `Could not copy Claude agents directory: ${
            error instanceof Error ? error.message : String(error)
          }`,
        );
      }
    } else {
      console.log(
        `   ${colors.yellow}No agents directory found in claude directory${colors.reset}`,
      );
    }

    if (copiedCount > 0) {
      printStatus(
        `Successfully copied ${copiedCount} Claude configuration items`,
      );
    }
    return true;
  } catch (error) {
    printError(
      `Failed to copy Claude configuration: ${
        error instanceof Error ? error.message : String(error)
      }`,
    );
    return false;
  }
}

async function copyGeminiConfig(
  dotfilesDir: string,
  homeDir: string,
): Promise<boolean> {
  printBlue("♊️ Copying Gemini configuration files...");
  const geminiSourceDir = join(dotfilesDir, "gemini");
  const geminiConfigDir = join(homeDir, ".gemini");

  // Check if gemini directory exists in dotfiles
  const geminiDirExists = await exists(geminiSourceDir);
  if (!geminiDirExists) {
    printWarning(
      "No gemini directory found in dotfiles, skipping Gemini configuration",
    );
    return true;
  }

  try {
    // Ensure Gemini config directory exists
    await ensureDir(geminiConfigDir);
    printStatus(`Created Gemini config directory: ${geminiConfigDir}`);

    let copiedCount = 0;

    // Copy individual config files
    for (const configFile of GEMINI_CONFIG_FILES) {
      const sourcePath = join(geminiSourceDir, configFile);
      const destPath = join(geminiConfigDir, configFile);

      if (await exists(sourcePath)) {
        try {
          await copy(sourcePath, destPath, { overwrite: true });
          printStatus(`Copied ${configFile} to Gemini config`);
          copiedCount++;
        } catch (error) {
          printWarning(
            `Could not copy ${configFile}: ${
              error instanceof Error ? error.message : String(error)
            }`,
          );
        }
      }
    }

    // Copy discover_tools.ts script
    const discoverToolsSource = join(
      dotfilesDir,
      "gemini",
      "discover_tools.ts",
    );
    const discoverToolsDest = join(geminiConfigDir, "discover_tools.ts");
    if (await exists(discoverToolsSource)) {
      try {
        await copy(discoverToolsSource, discoverToolsDest, { overwrite: true });
        printStatus("Copied discover_tools.ts to Gemini config");
        copiedCount++;
      } catch (error) {
        printWarning(
          `Could not copy discover_tools.ts: ${
            error instanceof Error ? error.message : String(error)
          }`,
        );
      }
    }

    // Copy extensions directory if it exists
    const extSource = join(dotfilesDir, "gemini", "extensions");
    const extDest = join(homeDir, ".gemini", "extensions");
    if (await exists(extSource)) {
      try {
        await ensureDir(extDest);
        await copy(extSource, extDest, { overwrite: true });
        printStatus("Copied Gemini CLI extensions");
        copiedCount++;
      } catch (error) {
        printWarning(
          `Could not copy Gemini extensions: ${
            error instanceof Error ? error.message : String(error)
          }`,
        );
      }
    } else {
      console.log(
        `   ${colors.yellow}No extensions directory found in gemini directory${colors.reset}`,
      );
    }

    // Update settings.json for tool discovery
    const settingsPath = join(geminiConfigDir, "settings.json");
    let settings = {};
    try {
      const settingsContent = await Deno.readTextFile(settingsPath);
      settings = JSON.parse(settingsContent);
    } catch (_e) {
      // Ignore if file doesn't exist or is invalid JSON
    }

    const updatedSettings = {
      ...settings,
      toolDiscoveryCommand: "deno run --allow-read --allow-run ~/.gemini/discover_tools.ts",
    };

    try {
      await Deno.writeTextFile(
        settingsPath,
        JSON.stringify(updatedSettings, null, 2),
      );
      printStatus("Updated Gemini settings.json for tool discovery");
    } catch (error) {
      printWarning(
        `Could not update Gemini settings.json: ${
          error instanceof Error ? error.message : String(error)
        }`,
      );
    }

    if (copiedCount > 0) {
      printStatus(
        `Successfully copied ${copiedCount} Gemini configuration items`,
      );
    }
    return true;
  } catch (error) {
    printError(
      `Failed to copy Gemini configuration: ${
        error instanceof Error ? error.message : String(error)
      }`,
    );
    return false;
  }
}

interface McpServer {
  command: string;
  args?: string[];
  type?: string;
  env?: Record<string, string>;
}

interface InstalledServer {
  name: string;
  scope: string;
  command: string;
  args: string[];
}

async function getInstalledUserServers(): Promise<
  Map<string, InstalledServer>
> {
  const servers = new Map<string, InstalledServer>();

  const listResult = await runCommand(["claude", "mcp", "list"]);
  if (!listResult.success) {
    return servers;
  }

  const lines = listResult.output.split("\n").filter((line) => line.trim());

  for (const line of lines) {
    const colonIndex = line.indexOf(":");
    if (colonIndex === -1) continue;

    const serverName = line.substring(0, colonIndex).trim();
    const getResult = await runCommand(["claude", "mcp", "get", serverName]);

    if (getResult.success && getResult.output.includes("Scope: User")) {
      const commandPart = line.substring(colonIndex + 1).trim();
      const parts = commandPart.split(" ");

      servers.set(serverName, {
        name: serverName,
        scope: "User",
        command: parts[0] || "",
        args: parts.slice(1),
      });
    }
  }

  return servers;
}

function areServerConfigsEqual(
  installed: InstalledServer,
  desired: McpServer,
): boolean {
  // Compare command
  if (installed.command !== desired.command) {
    return false;
  }

  // Compare args (normalize by removing -y flags for comparison)
  const normalizeArgs = (args: string[]) => args.filter((arg) => arg !== "-y").join(" ");

  const installedArgs = normalizeArgs(installed.args);
  const desiredArgs = normalizeArgs(desired.args || []);

  return installedArgs === desiredArgs;
}

interface McpDiff {
  missing: string[];
  toUpdate: string[];
  upToDate: string[];
}

function computeMcpDiff(
  desired: Record<string, McpServer>,
  installed: Map<string, InstalledServer>,
): McpDiff {
  const missing: string[] = [];
  const toUpdate: string[] = [];
  const upToDate: string[] = [];

  for (const [serverName, serverConfig] of Object.entries(desired)) {
    const installedServer = installed.get(serverName);

    if (!installedServer) {
      missing.push(serverName);
    } else if (!areServerConfigsEqual(installedServer, serverConfig)) {
      toUpdate.push(serverName);
    } else {
      upToDate.push(serverName);
    }
  }

  return {
    missing,
    toUpdate,
    upToDate,
  };
}

async function configureMcpServers(claudeConfigDir: string): Promise<boolean> {
  printBlue("🔧 Configuring Claude MCP servers...");

  const mcpConfigPath = join(claudeConfigDir, "mcp.json");

  // Check if mcp.json exists
  if (!(await exists(mcpConfigPath))) {
    printWarning("No mcp.json found, skipping MCP server configuration");
    return true;
  }

  try {
    // Read the mcp.json file
    const mcpContent = await Deno.readTextFile(mcpConfigPath);
    const mcpConfig = JSON.parse(mcpContent);

    if (!mcpConfig.mcpServers) {
      printWarning("No MCP servers defined in mcp.json");
      return true;
    }

    // Get currently installed servers
    printStatus("Analyzing currently installed MCP servers...");
    const installedServers = await getInstalledUserServers();

    // Compute what needs to be done using the new diff function
    const diff = computeMcpDiff(mcpConfig.mcpServers, installedServers);

    // Log detailed diff results with clear sections
    console.log();
    printBlue("📊 MCP Server Configuration Analysis:");
    console.log("═".repeat(50));

    // Missing servers section
    if (diff.missing.length > 0) {
      console.log(
        `\n${colors.yellow}❌ Missing servers (${diff.missing.length})${colors.reset}`,
      );
      console.log("─".repeat(30));
      for (const serverName of diff.missing) {
        console.log(`   • ${serverName} - Will be installed`);
      }
    } else {
      console.log(`\n${colors.green}✅ Missing servers: None${colors.reset}`);
    }

    // Servers to update section
    if (diff.toUpdate.length > 0) {
      console.log(
        `\n${colors.blue}🔄 Servers to update (${diff.toUpdate.length})${colors.reset}`,
      );
      console.log("─".repeat(30));
      for (const serverName of diff.toUpdate) {
        const installed = installedServers.get(serverName);
        const desired = mcpConfig.mcpServers[serverName] as McpServer;
        console.log(`   • ${serverName}`);
        if (installed && desired) {
          if (installed.command !== desired.command) {
            console.log(
              `     - Command: ${installed.command} → ${desired.command}`,
            );
          }
          const installedArgs = installed.args.join(" ");
          const desiredArgs = (desired.args || []).join(" ");
          if (installedArgs !== desiredArgs) {
            console.log(`     - Args: "${installedArgs}" → "${desiredArgs}"`);
          }
        }
      }
    } else {
      console.log(`\n${colors.green}✅ Servers to update: None${colors.reset}`);
    }

    // Already configured section
    if (diff.upToDate.length > 0) {
      console.log(
        `\n${colors.green}✅ Already configured (${diff.upToDate.length})${colors.reset}`,
      );
      console.log("─".repeat(30));
      for (const serverName of diff.upToDate) {
        console.log(`   • ${serverName} - Up to date`);
      }
    } else {
      console.log(
        `\n${colors.yellow}ℹ️  Already configured: None${colors.reset}`,
      );
    }

    console.log("\n" + "═".repeat(50));
    console.log();

    const toAdd: string[] = [...diff.missing];
    const toUpdate: string[] = [...diff.toUpdate];
    const alreadyConfigured = diff.upToDate.length;

    // Summary status
    if (alreadyConfigured > 0) {
      printStatus(`${alreadyConfigured} servers already properly configured`);
    }
    if (toAdd.length > 0) {
      printStatus(`${toAdd.length} servers will be installed`);
    }
    if (toUpdate.length > 0) {
      printStatus(`${toUpdate.length} servers will be updated`);
    }

    let configuredCount = 0;
    let failedCount = 0;

    // Update servers that need updating
    for (const serverName of toUpdate) {
      printWarning(`Updating configuration for: ${serverName}`);

      // Remove old configuration
      const removeResult = await runCommand([
        "claude",
        "mcp",
        "remove",
        serverName,
        "-s",
        "user",
      ]);
      if (!removeResult.success) {
        printWarning(
          `Failed to remove old config for ${serverName}: ${removeResult.output}`,
        );
        failedCount++;
        continue;
      }

      // Add to the list of servers to add
      toAdd.push(serverName);
    }

    // Add new servers
    for (const serverName of toAdd) {
      const config = mcpConfig.mcpServers[serverName] as McpServer;

      // Build the claude mcp add command with user scope for global availability
      const args = [
        "claude",
        "mcp",
        "add",
        "-s",
        "user",
        serverName,
        config.command,
      ];

      // Add transport type if specified
      if (config.type && config.type !== "stdio") {
        args.push("-t", config.type);
      }

      // Add arguments with -- separator for complex args
      if (config.args && Array.isArray(config.args) && config.args.length > 0) {
        const hasFlags = config.args.some((arg: string) => arg.startsWith("-"));
        if (hasFlags) {
          args.push("--");
        }
        args.push(...config.args);
      }

      // Run the command
      const result = await runCommand(args);

      if (result.success) {
        printStatus(`Configured MCP server: ${serverName}`);
        configuredCount++;
      } else {
        printWarning(
          `Failed to configure MCP server ${serverName}: ${result.output}`,
        );
        failedCount++;
      }
    }

    // Summary
    if (configuredCount > 0) {
      printStatus(`Successfully configured ${configuredCount} MCP servers`);
    }

    if (failedCount > 0) {
      printWarning(`Failed to configure ${failedCount} MCP servers`);
    }

    if (configuredCount === 0 && failedCount === 0 && alreadyConfigured > 0) {
      printStatus("All MCP servers were already properly configured!");
    }

    return true;
  } catch (error) {
    printWarning(
      `Could not configure MCP servers: ${error instanceof Error ? error.message : String(error)}`,
    );
    return false;
  }
}

async function copyGhosttyConfig(
  dotfilesDir: string,
  homeDir: string,
): Promise<boolean> {
  printBlue("👻 Copying Ghostty configuration file...");
  const ghosttySourceFile = join(dotfilesDir, "ghostty", GHOSTTY_CONFIG_FILE);
  const ghosttyConfigDir = join(
    homeDir,
    "Library",
    "Application Support",
    "com.mitchellh.ghostty",
  );
  const ghosttyDestFile = join(ghosttyConfigDir, GHOSTTY_CONFIG_FILE);

  // Check if Ghostty config exists in dotfiles
  const ghosttyConfigExists = await exists(ghosttySourceFile);
  if (!ghosttyConfigExists) {
    printWarning(
      "No ghostty/config file found in dotfiles, skipping Ghostty configuration",
    );
    return true;
  }

  try {
    // Ensure Ghostty config directory exists
    await ensureDir(ghosttyConfigDir);
    printStatus(`Created Ghostty config directory: ${ghosttyConfigDir}`);

    // Copy the config file
    await copy(ghosttySourceFile, ghosttyDestFile, { overwrite: true });
    printStatus(`Copied Ghostty config to ${ghosttyDestFile}`);

    return true;
  } catch (error) {
    printError(
      `Failed to copy Ghostty configuration: ${
        error instanceof Error ? error.message : String(error)
      }`,
    );
    return false;
  }
}

async function copyPowerShellProfile(
  dotfilesDir: string,
  homeDir: string,
): Promise<boolean> {
  // Only run on Windows
  if (Deno.build.os !== "windows") {
    return true;
  }

  printBlue("💻 Copying PowerShell profile...");
  const psSourcePath = join(dotfilesDir, "shell", "powershell", "profile.ps1");

  // Check if PowerShell profile exists in dotfiles
  if (!(await exists(psSourcePath))) {
    printWarning("No PowerShell profile found in dotfiles, skipping");
    return true;
  }

  try {
    // Get PowerShell profile directory
    const documentsDir = join(homeDir, "Documents");
    const psProfileDir = join(documentsDir, "WindowsPowerShell");
    const psProfilePath = join(
      psProfileDir,
      "Microsoft.PowerShell_profile.ps1",
    );

    // Ensure PowerShell profile directory exists
    await ensureDir(psProfileDir);

    // Copy the profile
    await copy(psSourcePath, psProfilePath, { overwrite: true });
    printStatus(`Copied PowerShell profile to ${psProfilePath}`);

    return true;
  } catch (error) {
    printWarning(
      `Could not copy PowerShell profile: ${
        error instanceof Error ? error.message : String(error)
      }`,
    );
    return false;
  }
}

async function backupScripts(
  homeDir: string,
  backupDir: string,
): Promise<string[]> {
  const scriptsDir = join(homeDir, ".tools");
  const scriptsBackupDir = join(backupDir, ".tools");
  const backedUpFiles: string[] = [];

  const scriptsDirExists = await exists(scriptsDir);
  if (!scriptsDirExists) {
    console.log(
      `   ${colors.yellow}No existing ~/.tools directory found${colors.reset}`,
    );
    return backedUpFiles;
  }

  try {
    await copy(scriptsDir, scriptsBackupDir, { overwrite: true });
    printStatus(`Backed up ~/.tools directory`);
    backedUpFiles.push(".tools");
  } catch (error) {
    printWarning(
      `Could not backup ~/.tools directory: ${
        error instanceof Error ? error.message : String(error)
      }`,
    );
  }

  return backedUpFiles;
}

async function copyScripts(
  dotfilesDir: string,
  homeDir: string,
): Promise<boolean> {
  printBlue("📜 Copying scripts to ~/.tools...");
  const scriptsSourceDir = join(dotfilesDir, SCRIPTS_DIR);
  const scriptsDestDir = join(homeDir, ".tools");

  // Check if tools directory exists in dotfiles
  const scriptsDirExists = await exists(scriptsSourceDir);
  if (!scriptsDirExists) {
    printWarning(
      "No tools directory found in dotfiles, skipping scripts installation",
    );
    return true;
  }

  try {
    // Ensure ~/.tools directory exists
    await ensureDir(scriptsDestDir);
    printStatus(`Created scripts directory: ${scriptsDestDir}`);

    // Get all script files
    let copiedCount = 0;
    for await (const entry of Deno.readDir(scriptsSourceDir)) {
      if (
        entry.isFile &&
        (entry.name.endsWith(".ts") || entry.name.endsWith(".js"))
      ) {
        const sourcePath = join(scriptsSourceDir, entry.name);
        const destPath = join(scriptsDestDir, entry.name);

        try {
          await copy(sourcePath, destPath, { overwrite: true });

          // Make the script executable
          if (Deno.build.os !== "windows") {
            await Deno.chmod(destPath, 0o755);
          }

          printStatus(`Copied and made executable: ${entry.name}`);
          copiedCount++;
        } catch (error) {
          printWarning(
            `Could not copy script ${entry.name}: ${
              error instanceof Error ? error.message : String(error)
            }`,
          );
        }
      }
    }

    if (copiedCount > 0) {
      printStatus(`Successfully copied ${copiedCount} scripts to ~/.tools`);
      console.log();
      console.log(
        `   ${colors.blue}Note:${colors.reset} Add ~/.tools to your PATH to run these scripts from anywhere.`,
      );
      console.log(
        `   ${colors.yellow}export PATH="$HOME/.tools:$PATH"${colors.reset}`,
      );
    }
    return true;
  } catch (error) {
    printError(
      `Failed to copy scripts: ${error instanceof Error ? error.message : String(error)}`,
    );
    return false;
  }
}

async function backupVSCodePrompts(
  homeDir: string,
  backupDir: string,
): Promise<string[]> {
  const vscodePromptsDir = join(
    homeDir,
    "Library",
    "Application Support",
    "Code",
    "User",
    "prompts",
  );
  const vscodePromptsBackupDir = join(
    backupDir,
    "Library",
    "Application Support",
    "Code",
    "User",
    "prompts",
  );
  const backedUpFiles: string[] = [];

  const promptsDirExists = await exists(vscodePromptsDir);
  if (!promptsDirExists) {
    console.log(
      `   ${colors.yellow}No existing VS Code prompts directory found${colors.reset}`,
    );
    return backedUpFiles;
  }

  try {
    await ensureDir(vscodePromptsBackupDir);

    // Backup all .prompt.md files
    for await (const entry of Deno.readDir(vscodePromptsDir)) {
      if (entry.isFile && entry.name.endsWith(".prompt.md")) {
        const sourcePath = join(vscodePromptsDir, entry.name);
        const backupPath = join(vscodePromptsBackupDir, entry.name);

        try {
          await copy(sourcePath, backupPath, { overwrite: true });
          printStatus(`Backed up VS Code prompt: ${entry.name}`);
          backedUpFiles.push(entry.name);
        } catch (error) {
          printWarning(
            `Could not backup VS Code prompt ${entry.name}: ${
              error instanceof Error ? error.message : String(error)
            }`,
          );
        }
      }
    }
  } catch (error) {
    printWarning(
      `Could not backup VS Code prompts: ${error instanceof Error ? error.message : String(error)}`,
    );
  }

  return backedUpFiles;
}

async function copyVSCodePrompts(
  dotfilesDir: string,
  homeDir: string,
): Promise<boolean> {
  printBlue("💬 Copying GitHub prompt files to VS Code global prompts...");
  const promptsSourceDir = join(dotfilesDir, GITHUB_PROMPTS_DIR);
  const vscodePromptsDir = join(
    homeDir,
    "Library",
    "Application Support",
    "Code",
    "User",
    "prompts",
  );

  // Check if github/prompts directory exists in dotfiles
  const promptsDirExists = await exists(promptsSourceDir);
  if (!promptsDirExists) {
    printWarning(
      "No github/prompts directory found in dotfiles, skipping VS Code prompts installation",
    );
    return true;
  }

  try {
    // Ensure VS Code prompts directory exists
    await ensureDir(vscodePromptsDir);
    printStatus(`Created VS Code prompts directory: ${vscodePromptsDir}`);

    let copiedCount = 0;
    for await (const entry of Deno.readDir(promptsSourceDir)) {
      if (entry.isFile && entry.name.endsWith(".prompt.md")) {
        const sourcePath = join(promptsSourceDir, entry.name);
        const destPath = join(vscodePromptsDir, entry.name);

        try {
          await copy(sourcePath, destPath, { overwrite: true });
          printStatus(`Copied VS Code prompt: ${entry.name}`);
          copiedCount++;
        } catch (error) {
          printWarning(
            `Could not copy VS Code prompt ${entry.name}: ${
              error instanceof Error ? error.message : String(error)
            }`,
          );
        }
      }
    }

    if (copiedCount > 0) {
      printStatus(
        `Successfully copied ${copiedCount} prompt files to VS Code global prompts`,
      );
      console.log();
      console.log(
        `   ${colors.blue}Note:${colors.reset} These prompts are now available globally in VS Code across all workspaces.`,
      );
    } else {
      printWarning("No .prompt.md files found in github/prompts directory");
    }
    return true;
  } catch (error) {
    printError(
      `Failed to copy VS Code prompts: ${error instanceof Error ? error.message : String(error)}`,
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
        // Note: This won't affect the parent shell, but we'll provide instructions
        await runCommand(["zsh", "-c", `source ${zshrcPath}`]);
        console.log();
        console.log(
          `   ${colors.blue}Note:${colors.reset} To apply changes in your current shell, run:`,
        );
        console.log(`   ${colors.yellow}source ~/.zshrc${colors.reset}`);
      }
    } else if (shellType === "bash") {
      const bashrcPath = join(homeDir, ".bashrc");
      if (await exists(bashrcPath)) {
        // Note: This won't affect the parent shell, but we'll provide instructions
        await runCommand(["bash", "-c", `source ${bashrcPath}`]);
        console.log();
        console.log(
          `   ${colors.blue}Note:${colors.reset} To apply changes in your current shell, run:`,
        );
        console.log(`   ${colors.yellow}source ~/.bashrc${colors.reset}`);
      }
    }
    printStatus("Shell configuration reloaded in subshell");
  } catch {
    printWarning("Could not reload shell configuration automatically");
    console.log(
      `   ${colors.blue}Note:${colors.reset} Manually reload your shell with:`,
    );
    if (shellType === "zsh") {
      console.log(`   ${colors.yellow}source ~/.zshrc${colors.reset}`);
    } else if (shellType === "bash") {
      console.log(`   ${colors.yellow}source ~/.bashrc${colors.reset}`);
    }
  }
}

async function checkFormatting(): Promise<boolean> {
  printBlue("🔍 Checking code formatting...");

  try {
    const result = await runCommand(["deno", "fmt", "--check"]);
    if (result.success) {
      printStatus("Code formatting check passed");
      return true;
    } else {
      printError("Code formatting check failed!");
      console.log();
      console.log("Please run the following command to fix formatting:");
      console.log(`   ${colors.yellow}deno fmt${colors.reset}`);
      console.log();
      return false;
    }
  } catch (error) {
    printWarning(
      `Could not check formatting: ${error instanceof Error ? error.message : String(error)}`,
    );
    return true; // Continue if check fails
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
  • Check code formatting before installation
  • Auto-detect your shell (zsh/bash)
  • Backup existing dotfiles with timestamp
  • Install new dotfiles from repository
  • Reload shell configuration
  • Provide rollback instructions
    `);
    return;
  }

  try {
    // Check formatting first
    const isFormatted = await checkFormatting();
    if (!isFormatted) {
      printError("Installation aborted due to formatting issues");
      Deno.exit(1);
    }
    console.log();

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

    // Backup existing dotfiles and configurations in parallel
    console.log();
    printBlue("💾 Backing up existing files (running in parallel)...");
    const backedUpFiles: string[] = [];

    try {
      // Create array of backup task promises for parallel execution
      const backupTasks: Promise<{ type: string; files: string[] }>[] = [];

      // Backup regular dotfiles - create individual promises for each file
      for (const file of DOTFILES) {
        backupTasks.push(
          (async () => {
            try {
              printBlue(`💾 Backing up ${file}...`);
              const success = await backupFile(
                file,
                config.homeDir,
                config.backupDir,
              );
              return { type: "dotfiles", files: success ? [file] : [] };
            } catch (error) {
              printWarning(
                `Error backing up ${file}: ${
                  error instanceof Error ? error.message : String(error)
                }`,
              );
              return { type: "dotfiles", files: [] };
            }
          })(),
        );
      }

      // Backup optional files - create individual promises for each file
      for (const file of OPTIONAL_FILES) {
        backupTasks.push(
          (async () => {
            try {
              printBlue(`🔍 Checking for optional file ${file}...`);
              const success = await backupFile(
                file,
                config.homeDir,
                config.backupDir,
              );
              return { type: "optional", files: success ? [file] : [] };
            } catch (error) {
              printWarning(
                `Error backing up optional file ${file}: ${
                  error instanceof Error ? error.message : String(error)
                }`,
              );
              return { type: "optional", files: [] };
            }
          })(),
        );
      }

      // Backup Zed configuration
      backupTasks.push(
        (async () => {
          try {
            printBlue("🎯 Backing up Zed configuration...");
            const files = await backupZedConfig(
              config.homeDir,
              config.backupDir,
            );
            return { type: "zed", files };
          } catch (error) {
            printWarning(
              `Error backing up Zed configuration: ${
                error instanceof Error ? error.message : String(error)
              }`,
            );
            return { type: "zed", files: [] };
          }
        })(),
      );

      // Backup Claude configuration
      backupTasks.push(
        (async () => {
          try {
            printBlue("🤖 Backing up Claude configuration...");
            const files = await backupClaudeConfig(
              config.homeDir,
              config.backupDir,
            );
            return { type: "claude", files };
          } catch (error) {
            printWarning(
              `Error backing up Claude configuration: ${
                error instanceof Error ? error.message : String(error)
              }`,
            );
            return { type: "claude", files: [] };
          }
        })(),
      );

      // Backup Gemini configuration
      backupTasks.push(
        (async () => {
          try {
            printBlue("♊️ Backing up Gemini configuration...");
            const files = await backupGeminiConfig(
              config.homeDir,
              config.backupDir,
            );
            return { type: "gemini", files };
          } catch (error) {
            printWarning(
              `Error backing up Gemini configuration: ${
                error instanceof Error ? error.message : String(error)
              }`,
            );
            return { type: "gemini", files: [] };
          }
        })(),
      );

      // Backup Ghostty configuration (macOS only)
      if (Deno.build.os === "darwin") {
        backupTasks.push(
          (async () => {
            try {
              printBlue("👻 Backing up Ghostty configuration...");
              const files = await backupGhosttyConfig(
                config.homeDir,
                config.backupDir,
              );
              return { type: "ghostty", files };
            } catch (error) {
              printWarning(
                `Error backing up Ghostty configuration: ${
                  error instanceof Error ? error.message : String(error)
                }`,
              );
              return { type: "ghostty", files: [] };
            }
          })(),
        );
      }

      // Backup scripts directory
      backupTasks.push(
        (async () => {
          try {
            printBlue("📜 Backing up scripts directory...");
            const files = await backupScripts(config.homeDir, config.backupDir);
            return { type: "scripts", files };
          } catch (error) {
            printWarning(
              `Error backing up scripts: ${error instanceof Error ? error.message : String(error)}`,
            );
            return { type: "scripts", files: [] };
          }
        })(),
      );

      // Backup VS Code prompts (macOS only)
      if (Deno.build.os === "darwin") {
        backupTasks.push(
          (async () => {
            try {
              printBlue("💬 Backing up VS Code global prompts...");
              const files = await backupVSCodePrompts(
                config.homeDir,
                config.backupDir,
              );
              return { type: "vscode-prompts", files };
            } catch (error) {
              printWarning(
                `Error backing up VS Code prompts: ${
                  error instanceof Error ? error.message : String(error)
                }`,
              );
              return { type: "vscode-prompts", files: [] };
            }
          })(),
        );
      }

      // PARALLEL BACKUP EXECUTION:
      // Using Promise.allSettled to run all backup tasks concurrently while ensuring graceful error handling.
      // Unlike Promise.all, Promise.allSettled never rejects - it waits for all promises to settle
      // (either fulfill or reject) and returns results for each. This allows us to:
      // 1. Maximize performance by running backups in parallel
      // 2. Continue processing even if some backup tasks fail
      // 3. Collect detailed results for each task to make informed decisions
      // 4. Provide comprehensive error reporting while maintaining operation continuity
      const backupResults = await Promise.allSettled(backupTasks);

      // Process results and collect backed up files
      const successfulBackups: { type: string; files: string[] }[] = [];
      let failedBackups = 0;

      for (const result of backupResults) {
        if (result.status === "fulfilled") {
          successfulBackups.push(result.value);
          backedUpFiles.push(...result.value.files);
        } else {
          failedBackups++;
          printWarning(
            `Backup task failed: ${
              result.reason instanceof Error ? result.reason.message : String(result.reason)
            }`,
          );
        }
      }

      // Log summary
      console.log();
      printStatus(`Completed parallel backup of ${backedUpFiles.length} files`);
      if (failedBackups > 0) {
        printWarning(`${failedBackups} backup tasks failed`);
      }

      // Group results by type and log summary
      const backupSummary = new Map<string, number>();
      for (const result of successfulBackups) {
        const currentCount = backupSummary.get(result.type) || 0;
        backupSummary.set(result.type, currentCount + result.files.length);
      }

      for (const [type, count] of backupSummary) {
        if (count > 0) {
          printStatus(`${type}: ${count} files backed up`);
        }
      }

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

      // Install configurations in parallel
      console.log();
      printBlue("📦 Installing configurations (running in parallel)...");

      // Initialize variables outside try block to ensure they're in scope for error handling
      let successfulInstalls = 0;
      let failedInstalls = 0;
      let dotfilesInstallSuccess = false;
      let claudeInstallSuccess = false;

      try {
        // Create array of installation task promises for parallel execution
        const installationTasks: Promise<{
          task: string;
          success: boolean;
          error?: string;
        }>[] = [];

        // Copy dotfiles
        installationTasks.push(
          (async () => {
            try {
              const success = await copyDotfiles(
                config.dotfilesDir,
                config.homeDir,
              );
              return { task: "copyDotfiles", success };
            } catch (error) {
              return {
                task: "copyDotfiles",
                success: false,
                error: error instanceof Error ? error.message : String(error),
              };
            }
          })(),
        );

        // Copy Zed configuration
        installationTasks.push(
          (async () => {
            try {
              const success = await copyZedConfig(
                config.dotfilesDir,
                config.homeDir,
              );
              return { task: "copyZedConfig", success };
            } catch (error) {
              return {
                task: "copyZedConfig",
                success: false,
                error: error instanceof Error ? error.message : String(error),
              };
            }
          })(),
        );

        // Copy Claude configuration
        installationTasks.push(
          (async () => {
            try {
              const success = await copyClaudeConfig(
                config.dotfilesDir,
                config.homeDir,
              );
              return { task: "copyClaudeConfig", success };
            } catch (error) {
              return {
                task: "copyClaudeConfig",
                success: false,
                error: error instanceof Error ? error.message : String(error),
              };
            }
          })(),
        );

        // Copy Gemini configuration
        installationTasks.push(
          (async () => {
            try {
              const success = await copyGeminiConfig(
                config.dotfilesDir,
                config.homeDir,
              );
              return { task: "copyGeminiConfig", success };
            } catch (error) {
              return {
                task: "copyGeminiConfig",
                success: false,
                error: error instanceof Error ? error.message : String(error),
              };
            }
          })(),
        );

        // Copy Ghostty configuration (macOS only)
        if (Deno.build.os === "darwin") {
          installationTasks.push(
            (async () => {
              try {
                const success = await copyGhosttyConfig(
                  config.dotfilesDir,
                  config.homeDir,
                );
                return { task: "copyGhosttyConfig", success };
              } catch (error) {
                return {
                  task: "copyGhosttyConfig",
                  success: false,
                  error: error instanceof Error ? error.message : String(error),
                };
              }
            })(),
          );
        }

        // Copy PowerShell profile (Windows only)
        if (Deno.build.os === "windows") {
          installationTasks.push(
            (async () => {
              try {
                const success = await copyPowerShellProfile(
                  config.dotfilesDir,
                  config.homeDir,
                );
                return { task: "copyPowerShellProfile", success };
              } catch (error) {
                return {
                  task: "copyPowerShellProfile",
                  success: false,
                  error: error instanceof Error ? error.message : String(error),
                };
              }
            })(),
          );
        }

        // Copy scripts to ~/.tools
        installationTasks.push(
          (async () => {
            try {
              const success = await copyScripts(
                config.dotfilesDir,
                config.homeDir,
              );
              return { task: "copyScripts", success };
            } catch (error) {
              return {
                task: "copyScripts",
                success: false,
                error: error instanceof Error ? error.message : String(error),
              };
            }
          })(),
        );

        // Copy VS Code prompts (macOS only)
        if (Deno.build.os === "darwin") {
          installationTasks.push(
            (async () => {
              try {
                const success = await copyVSCodePrompts(
                  config.dotfilesDir,
                  config.homeDir,
                );
                return { task: "copyVSCodePrompts", success };
              } catch (error) {
                return {
                  task: "copyVSCodePrompts",
                  success: false,
                  error: error instanceof Error ? error.message : String(error),
                };
              }
            })(),
          );
        }

        // PARALLEL INSTALLATION EXECUTION:
        // Promise.allSettled is employed here to execute all installation tasks concurrently, enhancing performance
        // and efficiency. By allowing each promise to settle, we can:
        // 1. Freely process successful installations alongside failed ones
        // 2. Gather detailed outcomes for every operation
        // 3. Sustain the script's continuity despite individual errors
        // This method is preferred here to handle partial installations gracefully without affecting the overall flow.
        const installationResults = await Promise.allSettled(installationTasks);

        // Process results and handle errors

        for (const result of installationResults) {
          if (result.status === "fulfilled") {
            const taskResult = result.value;
            if (taskResult.success) {
              printStatus(`${taskResult.task} completed successfully`);
              successfulInstalls++;

              // Track specific installations for post-processing
              if (taskResult.task === "copyDotfiles") {
                dotfilesInstallSuccess = true;
              } else if (taskResult.task === "copyClaudeConfig") {
                claudeInstallSuccess = true;
              }
            } else {
              printWarning(
                `${taskResult.task} failed${
                  taskResult.error ? `: ${taskResult.error}` : ", but continuing..."
                }`,
              );
              failedInstalls++;
            }
          } else {
            printError(
              `Installation task failed: ${
                result.reason instanceof Error ? result.reason.message : String(result.reason)
              }`,
            );
            failedInstalls++;
          }
        }

        // Check if dotfiles installation was successful (critical for continuing)
        if (!dotfilesInstallSuccess) {
          printError("Critical dotfiles installation failed. Aborting.");
          Deno.exit(1);
        }
      } catch (error) {
        printError(
          `Installation phase failed: ${error instanceof Error ? error.message : String(error)}`,
        );
        Deno.exit(1);
      }

      // Log summary
      console.log();
      printStatus(
        `Completed parallel installation: ${successfulInstalls} successful, ${failedInstalls} failed`,
      );

      // Configure MCP servers for Claude (must run after Claude config is installed)
      if (claudeInstallSuccess) {
        console.log();
        const mcpConfigSuccess = await configureMcpServers(
          join(config.homeDir, ".claude"),
        );
        if (!mcpConfigSuccess) {
          printWarning("MCP server configuration failed, but continuing...");
        }
      } else {
        printWarning(
          "Skipping MCP server configuration - copyClaudeConfig did not complete successfully",
        );
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
      console.log("   ✅ Verified code formatting before installation");
      console.log(
        `   ✅ Backed up existing dotfiles to: ${colors.yellow}${config.backupDir}${colors.reset}`,
      );
      console.log("   ✅ Installed new dotfiles from repository");
      console.log("   ✅ Installed Zed configuration files");
      console.log(
        "   ✅ Installed Claude configuration files, custom commands, and agents",
      );
      console.log("   ✅ Configured Claude MCP servers from mcp.json");
      console.log("   ✅ Installed Gemini configuration files");
      console.log("   ✅ Installed tmux configuration");
      console.log("   ✅ Installed scripts to ~/.tools directory");
      if (Deno.build.os === "darwin") {
        console.log("   ✅ Installed VS Code global prompt files");
        console.log("   ✅ Installed Ghostty terminal configuration");
      }
      if (Deno.build.os === "windows") {
        console.log("   ✅ Installed PowerShell profile");
      }
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
      console.log(
        `   • Try: ${colors.yellow}hello.ts${colors.reset} (test script from ~/.tools)`,
      );
      console.log(
        `   • Try: ${colors.yellow}tmux${colors.reset} (terminal multiplexer with new config)`,
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
        `Backup phase failed: ${error instanceof Error ? error.message : String(error)}`,
      );
      Deno.exit(1);
    }
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
