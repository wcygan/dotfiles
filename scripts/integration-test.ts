#!/usr/bin/env -S deno test --allow-all

/**
 * Integration Tests for Dotfiles Installation and Rollback
 * Tests both install-safely.ts and rollback.ts in isolated environments
 * Compatible with Linux and macOS
 */

import { assert, assertExists } from "@std/assert";
import { join } from "@std/path";
import { exists } from "@std/fs/exists";
import { ensureDir } from "@std/fs/ensure-dir";
import { copy } from "@std/fs/copy";

interface TestEnvironment {
  tempDir: string;
  homeDir: string;
  dotfilesDir: string;
  originalEnv: Record<string, string | undefined>;
}

class DotfilesTestRunner {
  private testEnv: TestEnvironment | null = null;

  async setupTestEnvironment(): Promise<TestEnvironment> {
    // Create temporary test directory
    const tempDir = await Deno.makeTempDir({ prefix: "dotfiles_test_" });
    const homeDir = join(tempDir, "home");
    const dotfilesDir = join(tempDir, "dotfiles");

    // Store original environment
    const originalEnv = {
      HOME: Deno.env.get("HOME"),
      USER: Deno.env.get("USER"),
      SHELL: Deno.env.get("SHELL"),
    };

    // Create test directories
    await ensureDir(homeDir);
    await ensureDir(dotfilesDir);

    // Copy current dotfiles to test directory
    await this.copyDotfilesToTest(dotfilesDir);

    // Create some existing dotfiles in fake home
    await this.createExistingDotfiles(homeDir);

    this.testEnv = {
      tempDir,
      homeDir,
      dotfilesDir,
      originalEnv,
    };

    return this.testEnv;
  }

  private async copyDotfilesToTest(dotfilesDir: string): Promise<void> {
    // Copy the entire shell directory structure
    const shellDir = "shell";
    if (await exists(shellDir)) {
      await copy(shellDir, join(dotfilesDir, shellDir));
    }

    // Copy the scripts directory
    const scriptsDir = "scripts";
    if (await exists(scriptsDir)) {
      await copy(scriptsDir, join(dotfilesDir, scriptsDir));
    }

    // Copy other essential files
    const rootFiles = [
      "deno.json",
      "deno.lock",
    ];

    for (const file of rootFiles) {
      if (await exists(file)) {
        await copy(file, join(dotfilesDir, file));
      }
    }
  }

  private async createExistingDotfiles(homeDir: string): Promise<void> {
    // Create some existing dotfiles to test backup functionality
    const existingFiles = {
      ".zshrc": "# Existing zshrc\nexport EXISTING=true\n",
      ".bash_profile": "# Existing bash profile\nexport OLD_CONFIG=true\n",
      ".aliases.sh": "# Old aliases\nalias old_command='echo old'\n",
      ".vimrc": '" Old vimrc\nset number\n',
    };

    for (const [file, content] of Object.entries(existingFiles)) {
      await Deno.writeTextFile(join(homeDir, file), content);
    }
  }

  async runInstallation(force = false): Promise<{ success: boolean; output: string }> {
    if (!this.testEnv) throw new Error("Test environment not setup");

    // Set test environment variables
    Deno.env.set("HOME", this.testEnv.homeDir);
    Deno.env.set("USER", "testuser");
    Deno.env.set("SHELL", "/bin/zsh");

    try {
      const args = ["run", "--allow-all", join(this.testEnv.dotfilesDir, "scripts", "install-safely.ts")];
      if (force) args.push("--force");

      const command = new Deno.Command("deno", {
        args,
        cwd: this.testEnv.dotfilesDir,
        stdout: "piped",
        stderr: "piped",
        stdin: force ? undefined : "piped",
      });

      const process = command.spawn();

      // If not force mode, automatically answer "yes" to prompts
      if (!force && process.stdin) {
        const writer = process.stdin.getWriter();
        await writer.write(new TextEncoder().encode("y\n"));
        await writer.close();
      }

      const result = await process.output();
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

  async runRollback(backupDir: string): Promise<{ success: boolean; output: string }> {
    if (!this.testEnv) throw new Error("Test environment not setup");

    try {
      const command = new Deno.Command("deno", {
        args: [
          "run",
          "--allow-all",
          join(this.testEnv.dotfilesDir, "scripts", "rollback.ts"),
          backupDir,
          "--force",
        ],
        cwd: this.testEnv.dotfilesDir,
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

  async findBackupDirectory(): Promise<string | null> {
    if (!this.testEnv) return null;

    try {
      for await (const dirEntry of Deno.readDir(this.testEnv.homeDir)) {
        if (dirEntry.isDirectory && dirEntry.name.startsWith(".dotfiles-backup-")) {
          return join(this.testEnv.homeDir, dirEntry.name);
        }
      }
    } catch {
      // Directory might not exist or be readable
    }

    return null;
  }

  async readFile(filePath: string): Promise<string | null> {
    try {
      return await Deno.readTextFile(filePath);
    } catch {
      return null;
    }
  }

  async cleanup(): Promise<void> {
    if (!this.testEnv) return;

    // Restore original environment
    for (const [key, value] of Object.entries(this.testEnv.originalEnv)) {
      if (value === undefined) {
        Deno.env.delete(key);
      } else {
        Deno.env.set(key, value);
      }
    }

    // Clean up temporary directory
    try {
      await Deno.remove(this.testEnv.tempDir, { recursive: true });
    } catch {
      // Ignore cleanup errors
    }

    this.testEnv = null;
  }
}

// Integration Tests

Deno.test("Fresh Installation - No Existing Dotfiles", async () => {
  const runner = new DotfilesTestRunner();

  try {
    const testEnv = await runner.setupTestEnvironment();

    // Remove existing files to simulate fresh install
    const filesToRemove = [".zshrc", ".bash_profile", ".aliases.sh", ".vimrc"];
    for (const file of filesToRemove) {
      try {
        await Deno.remove(join(testEnv.homeDir, file));
      } catch {
        // File might not exist
      }
    }

    // Run installation with force flag
    const result = await runner.runInstallation(true);

    assert(result.success, `Installation failed: ${result.output}`);
    assert(
      result.output.includes("Installation completed successfully"),
      "Success message not found",
    );

    // Verify dotfiles were copied
    const installedFiles = [".zshrc", ".bash_profile", ".aliases.sh", ".vimrc"];
    for (const file of installedFiles) {
      const filePath = join(testEnv.homeDir, file);
      assertExists(await runner.readFile(filePath), `${file} was not installed`);
    }
  } finally {
    await runner.cleanup();
  }
});

Deno.test("Installation with Existing Dotfiles - Backup Creation", async () => {
  const runner = new DotfilesTestRunner();

  try {
    const testEnv = await runner.setupTestEnvironment();

    // Run installation with force flag
    const result = await runner.runInstallation(true);

    assert(result.success, `Installation failed: ${result.output}`);
    assert(
      result.output.includes("Installation completed successfully"),
      "Success message not found",
    );

    // Verify backup was created
    const backupDir = await runner.findBackupDirectory();
    assertExists(backupDir, "Backup directory was not created");

    // Verify backup contains original files
    const originalZshrc = await runner.readFile(join(backupDir!, ".zshrc"));
    assertExists(originalZshrc, "Original .zshrc not backed up");
    assert(originalZshrc!.includes("EXISTING=true"), "Backup doesn't contain original content");

    // Verify new files were installed
    const newZshrc = await runner.readFile(join(testEnv.homeDir, ".zshrc"));
    assertExists(newZshrc, "New .zshrc not installed");
  } finally {
    await runner.cleanup();
  }
});

Deno.test("Rollback Functionality", async () => {
  const runner = new DotfilesTestRunner();

  try {
    const testEnv = await runner.setupTestEnvironment();

    // First, install dotfiles
    const installResult = await runner.runInstallation(true);
    assert(installResult.success, `Installation failed: ${installResult.output}`);

    // Find the backup directory
    const backupDir = await runner.findBackupDirectory();
    assertExists(backupDir, "Backup directory not found");

    // Modify an installed file to verify rollback
    const modifiedContent = "# Modified after installation\nexport MODIFIED=true\n";
    await Deno.writeTextFile(join(testEnv.homeDir, ".zshrc"), modifiedContent);

    // Run rollback
    const rollbackResult = await runner.runRollback(backupDir!);
    assert(rollbackResult.success, `Rollback failed: ${rollbackResult.output}`);
    assert(
      rollbackResult.output.includes("Rollback completed successfully"),
      "Rollback success message not found",
    );

    // Verify original content was restored
    const restoredZshrc = await runner.readFile(join(testEnv.homeDir, ".zshrc"));
    assertExists(restoredZshrc, "Restored .zshrc not found");
    assert(restoredZshrc!.includes("EXISTING=true"), "Original content not restored");
    assert(!restoredZshrc!.includes("MODIFIED=true"), "Modified content still present");
  } finally {
    await runner.cleanup();
  }
});

Deno.test("Cross-Platform Path Handling", async () => {
  const runner = new DotfilesTestRunner();

  try {
    const _testEnv = await runner.setupTestEnvironment();

    // Test with different path formats
    const result = await runner.runInstallation(true);
    assert(result.success, `Installation failed: ${result.output}`);

    // Verify paths work correctly on current platform
    const platform = Deno.build.os;
    assert(["linux", "darwin", "windows"].includes(platform), "Unsupported platform");

    // Verify backup directory path format
    const backupDir = await runner.findBackupDirectory();
    assertExists(backupDir, "Backup directory not found");

    // Verify backup directory follows expected naming pattern
    const backupName = backupDir!.split(/[/\\]/).pop();
    assert(backupName?.startsWith(".dotfiles-backup-"), "Backup directory naming incorrect");
  } finally {
    await runner.cleanup();
  }
});

Deno.test("Error Handling - Invalid Rollback Directory", async () => {
  const runner = new DotfilesTestRunner();

  try {
    const testEnv = await runner.setupTestEnvironment();

    // Try to rollback from non-existent directory
    const invalidDir = join(testEnv.homeDir, ".invalid-backup");
    const result = await runner.runRollback(invalidDir);

    assert(!result.success, "Rollback should fail with invalid directory");
    assert(
      result.output.includes("does not exist"),
      "Error message should mention non-existent directory",
    );
  } finally {
    await runner.cleanup();
  }
});

Deno.test("Help Command Functionality", async () => {
  const runner = new DotfilesTestRunner();

  try {
    const _testEnv = await runner.setupTestEnvironment();

    // Test help command
    const command = new Deno.Command("deno", {
      args: [
        "run",
        "--allow-all",
        join(_testEnv.dotfilesDir, "install-safely.ts"),
        "--help",
      ],
      cwd: _testEnv.dotfilesDir,
      stdout: "piped",
      stderr: "piped",
    });

    const result = await command.output();
    const output = new TextDecoder().decode(result.stdout);

    assert(result.success, "Help command should succeed");
    assert(output.includes("Safe Dotfiles Installation Script"), "Help text should be displayed");
    assert(output.includes("--force"), "Help should mention force option");
  } finally {
    await runner.cleanup();
  }
});

// Platform-specific tests

if (Deno.build.os === "darwin") {
  Deno.test("macOS Specific - Shell Detection", async () => {
    const runner = new DotfilesTestRunner();

    try {
      const _testEnv = await runner.setupTestEnvironment();

      // Set macOS typical shell
      Deno.env.set("SHELL", "/bin/zsh");

      const result = await runner.runInstallation(true);
      assert(result.success, `Installation failed: ${result.output}`);
      assert(result.output.includes("zsh"), "Should detect zsh shell on macOS");
    } finally {
      await runner.cleanup();
    }
  });
}

if (Deno.build.os === "linux") {
  Deno.test("Linux Specific - Shell Detection", async () => {
    const runner = new DotfilesTestRunner();

    try {
      const _testEnv = await runner.setupTestEnvironment();

      // Set Linux typical shell
      Deno.env.set("SHELL", "/bin/bash");

      const result = await runner.runInstallation(true);
      assert(result.success, `Installation failed: ${result.output}`);
      assert(result.output.includes("bash"), "Should detect bash shell on Linux");
    } finally {
      await runner.cleanup();
    }
  });
}

console.log(`Running integration tests on ${Deno.build.os}...`);
