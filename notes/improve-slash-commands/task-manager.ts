#!/usr/bin/env -S deno run --allow-read --allow-write

import { parseArgs as parse } from "@std/cli/parse-args";
import { cyan, green, red, yellow } from "@std/fmt/colors";

interface CommandMetrics {
  hadFrontMatter: boolean;
  hadDynamicContext: boolean;
  hadProgrammaticStructure: boolean;
  hadStateManagement: boolean;
}

interface ClaimInfo {
  sessionId: string;
  timestamp: number;
}

interface Command {
  id: string;
  name: string;
  filepath: string;
  namespace: string;
  status: "pending" | "in-progress" | "completed";
  lastModified: string;
  claimedBy?: ClaimInfo;
  improvements?: string[];
  metrics?: CommandMetrics;
}

interface ProgressData {
  version: string;
  totalCommands: number;
  completed: number;
  inProgress: number;
  lastUpdated: string;
  commands: Command[];
}

class TaskManager {
  private progressFile: string;
  private lockFile: string;
  private staleTimeoutMs: number = 10 * 60 * 1000; // 10 minutes

  constructor(progressFile: string) {
    this.progressFile = progressFile;
    this.lockFile = `${progressFile}.lock`;
  }

  private async acquireLock(): Promise<Deno.FsFile> {
    try {
      // Create exclusive lock file
      const lockFile = await Deno.open(this.lockFile, {
        create: true,
        write: true,
        createNew: true, // Fails if file exists
      });
      return lockFile;
    } catch (error) {
      if (error instanceof Deno.errors.AlreadyExists) {
        throw new Error("Another task manager instance is already running");
      }
      throw error;
    }
  }

  private async releaseLock(lockFile: Deno.FsFile): Promise<void> {
    try {
      lockFile.close();
      await Deno.remove(this.lockFile);
    } catch (error) {
      // Enhanced error handling for lock cleanup
      if (error instanceof Deno.errors.NotFound) {
        // Lock file already removed, that's fine
        return;
      }
      console.error(`Warning: Failed to release lock: ${error.message}`);

      // Try to force cleanup with a small delay
      try {
        await new Promise((resolve) => setTimeout(resolve, 100));
        await Deno.remove(this.lockFile);
      } catch {
        // If it still fails, log but don't throw - we did our best
        console.error(
          `Warning: Could not force cleanup lock file: ${this.lockFile}`,
        );
      }
    }
  }

  private async loadProgress(): Promise<ProgressData> {
    try {
      const data = await Deno.readTextFile(this.progressFile);
      const parsed = JSON.parse(data);

      // Basic validation of progress file structure
      if (!parsed || typeof parsed !== "object") {
        throw new Error("Invalid progress file format: not an object");
      }

      if (!Array.isArray(parsed.commands)) {
        throw new Error(
          "Invalid progress file format: commands is not an array",
        );
      }

      if (
        typeof parsed.totalCommands !== "number" ||
        typeof parsed.completed !== "number" ||
        typeof parsed.inProgress !== "number"
      ) {
        throw new Error(
          "Invalid progress file format: missing or invalid counters",
        );
      }

      return parsed;
    } catch (error) {
      if (error instanceof Deno.errors.NotFound) {
        throw new Error(`Progress file not found: ${this.progressFile}`);
      }
      if (error instanceof SyntaxError) {
        throw new Error(
          `Progress file contains invalid JSON: ${error.message}`,
        );
      }
      throw new Error(`Failed to load progress: ${error.message}`);
    }
  }

  private async saveProgress(data: ProgressData): Promise<void> {
    // Atomic write using temp file to prevent corruption
    const tempFile = `${this.progressFile}.tmp.${Date.now()}`;
    const json = JSON.stringify(data, null, 2);

    try {
      await Deno.writeTextFile(tempFile, json);
      await Deno.rename(tempFile, this.progressFile);
    } catch (error) {
      // Clean up temp file if rename failed
      try {
        await Deno.remove(tempFile);
      } catch {
        // Ignore cleanup errors
      }
      throw error;
    }
  }

  private getCurrentTimestamp(): number {
    return Math.floor(Date.now() / 1000);
  }

  private getCurrentISOTimestamp(): string {
    return new Date().toISOString();
  }

  private generateSessionId(): string {
    // Enhanced session ID with better entropy and collision avoidance
    const timestamp = Date.now();
    const randomPart = Math.random().toString(36).substring(2, 9);
    const processId = Deno.pid?.toString(36) ||
      Math.random().toString(36).substring(2, 4);
    return `${timestamp}${randomPart}${processId}`;
  }

  private isStale(claimedBy: ClaimInfo): boolean {
    const now = this.getCurrentTimestamp();
    const staleTimeoutSeconds = this.staleTimeoutMs / 1000;
    return (now - claimedBy.timestamp) > staleTimeoutSeconds;
  }

  private findClaimableCommand(data: ProgressData): Command | null {
    return data.commands.find((cmd) =>
      cmd.status === "pending" ||
      (cmd.status === "in-progress" && cmd.claimedBy &&
        this.isStale(cmd.claimedBy))
    ) || null;
  }

  private updateProgressCounters(data: ProgressData): void {
    data.completed = data.commands.filter((cmd) => cmd.status === "completed").length;
    data.inProgress = data.commands.filter((cmd) => cmd.status === "in-progress").length;
    data.lastUpdated = this.getCurrentISOTimestamp();
  }

  async claimTask(): Promise<
    { success: boolean; command?: Command; message: string }
  > {
    let lockFile: Deno.FsFile | null = null;

    try {
      lockFile = await this.acquireLock();
      const data = await this.loadProgress();

      const claimableCommand = this.findClaimableCommand(data);

      if (!claimableCommand) {
        return {
          success: false,
          message: "No claimable commands available",
        };
      }

      // Claim the command
      const sessionId = this.generateSessionId();
      const timestamp = this.getCurrentTimestamp();

      claimableCommand.status = "in-progress";
      claimableCommand.claimedBy = { sessionId, timestamp };
      claimableCommand.lastModified = this.getCurrentISOTimestamp();

      this.updateProgressCounters(data);
      await this.saveProgress(data);

      return {
        success: true,
        command: claimableCommand,
        message: `Successfully claimed task: ${claimableCommand.name}`,
      };
    } catch (error) {
      return {
        success: false,
        message: `Failed to claim task: ${error.message}`,
      };
    } finally {
      if (lockFile) {
        await this.releaseLock(lockFile);
      }
    }
  }

  async completeTask(
    commandId: string,
    sessionId: string,
    improvements: string[] = [],
  ): Promise<{ success: boolean; message: string }> {
    let lockFile: Deno.FsFile | null = null;

    try {
      lockFile = await this.acquireLock();
      const data = await this.loadProgress();

      const command = data.commands.find((cmd) => cmd.id === commandId);

      if (!command) {
        return {
          success: false,
          message: `Command with ID ${commandId} not found`,
        };
      }

      if (command.status !== "in-progress") {
        return {
          success: false,
          message: `Command ${command.name} is not in progress`,
        };
      }

      if (!command.claimedBy || command.claimedBy.sessionId !== sessionId) {
        return {
          success: false,
          message: `Command ${command.name} is not claimed by this session`,
        };
      }

      // Mark as completed
      command.status = "completed";
      command.lastModified = this.getCurrentISOTimestamp();
      command.improvements = improvements;
      delete command.claimedBy;

      this.updateProgressCounters(data);
      await this.saveProgress(data);

      return {
        success: true,
        message:
          `Successfully completed task: ${command.name} (${data.completed}/${data.totalCommands})`,
      };
    } catch (error) {
      return {
        success: false,
        message: `Failed to complete task: ${error.message}`,
      };
    } finally {
      if (lockFile) {
        await this.releaseLock(lockFile);
      }
    }
  }

  async releaseTask(
    commandId: string,
    sessionId: string,
  ): Promise<{ success: boolean; message: string }> {
    let lockFile: Deno.FsFile | null = null;

    try {
      lockFile = await this.acquireLock();
      const data = await this.loadProgress();

      const command = data.commands.find((cmd) => cmd.id === commandId);

      if (!command) {
        return {
          success: false,
          message: `Command with ID ${commandId} not found`,
        };
      }

      if (command.status !== "in-progress") {
        return {
          success: false,
          message: `Command ${command.name} is not in progress`,
        };
      }

      if (!command.claimedBy || command.claimedBy.sessionId !== sessionId) {
        return {
          success: false,
          message: `Command ${command.name} is not claimed by this session`,
        };
      }

      // Release the command
      command.status = "pending";
      command.lastModified = this.getCurrentISOTimestamp();
      delete command.claimedBy;

      this.updateProgressCounters(data);
      await this.saveProgress(data);

      return {
        success: true,
        message: `Successfully released task: ${command.name}`,
      };
    } catch (error) {
      return {
        success: false,
        message: `Failed to release task: ${error.message}`,
      };
    } finally {
      if (lockFile) {
        await this.releaseLock(lockFile);
      }
    }
  }

  async getStatus(): Promise<{
    totalCommands: number;
    completed: number;
    inProgress: number;
    available: number;
    stale: number;
  }> {
    // Status operation doesn't need locking since it's read-only
    const data = await this.loadProgress();

    let available = 0;
    let stale = 0;

    for (const cmd of data.commands) {
      if (cmd.status === "pending") {
        available++;
      } else if (
        cmd.status === "in-progress" && cmd.claimedBy &&
        this.isStale(cmd.claimedBy)
      ) {
        stale++;
        available++;
      }
    }

    return {
      totalCommands: data.totalCommands,
      completed: data.completed,
      inProgress: data.inProgress,
      available,
      stale,
    };
  }

  async cleanup(): Promise<
    { success: boolean; message: string; recovered: number }
  > {
    let lockFile: Deno.FsFile | null = null;

    try {
      lockFile = await this.acquireLock();
      const data = await this.loadProgress();

      let recovered = 0;

      for (const command of data.commands) {
        if (
          command.status === "in-progress" && command.claimedBy &&
          this.isStale(command.claimedBy)
        ) {
          command.status = "pending";
          delete command.claimedBy;
          command.lastModified = this.getCurrentISOTimestamp();
          recovered++;
        }
      }

      if (recovered > 0) {
        this.updateProgressCounters(data);
        await this.saveProgress(data);
      }

      return {
        success: true,
        message: `Cleanup completed. Recovered ${recovered} stale claims.`,
        recovered,
      };
    } catch (error) {
      return {
        success: false,
        message: `Cleanup failed: ${error.message}`,
        recovered: 0,
      };
    } finally {
      if (lockFile) {
        await this.releaseLock(lockFile);
      }
    }
  }
}

async function main() {
  const args = parse(Deno.args, {
    string: ["command-id", "session-id", "progress-file"],
    collect: ["improvement"],
    default: {
      "progress-file": "notes/improve-slash-commands/progress.json",
    },
  });

  const [command] = args._;
  const progressFile = args["progress-file"];

  if (!command) {
    console.error(red("Usage: task-manager.ts <command> [options]"));
    console.error("Commands:");
    console.error("  claim              - Claim next available task");
    console.error("  complete           - Complete claimed task");
    console.error("  release            - Release claimed task");
    console.error("  status             - Show current status");
    console.error("  cleanup            - Clean up stale claims");
    console.error("");
    console.error("Options:");
    console.error("  --command-id <id>  - Command ID for complete/release");
    console.error("  --session-id <id>  - Session ID for complete/release");
    console.error("  --improvement <imp> - Improvement made (can be repeated)");
    console.error("  --progress-file <f> - Path to progress.json file");
    Deno.exit(1);
  }

  const taskManager = new TaskManager(progressFile);

  try {
    switch (command) {
      case "claim": {
        const result = await taskManager.claimTask();
        if (result.success) {
          console.log(green(`✅ ${result.message}`));
          if (result.command) {
            console.log(cyan(`📁 File: ${result.command.filepath}`));
            console.log(cyan(`🆔 Command ID: ${result.command.id}`));
            console.log(
              cyan(`🔗 Session ID: ${result.command.claimedBy?.sessionId}`),
            );
          }
        } else {
          console.log(yellow(`⚠️  ${result.message}`));
          Deno.exit(1);
        }
        break;
      }

      case "complete": {
        const commandId = args["command-id"];
        const sessionId = args["session-id"];
        const improvements = args.improvement || [];

        if (!commandId || !sessionId) {
          console.error(
            red("❌ complete requires --command-id and --session-id"),
          );
          Deno.exit(1);
        }

        const result = await taskManager.completeTask(
          commandId,
          sessionId,
          improvements,
        );
        if (result.success) {
          console.log(green(`✅ ${result.message}`));
        } else {
          console.error(red(`❌ ${result.message}`));
          Deno.exit(1);
        }
        break;
      }

      case "release": {
        const commandId = args["command-id"];
        const sessionId = args["session-id"];

        if (!commandId || !sessionId) {
          console.error(
            red("❌ release requires --command-id and --session-id"),
          );
          Deno.exit(1);
        }

        const result = await taskManager.releaseTask(commandId, sessionId);
        if (result.success) {
          console.log(green(`✅ ${result.message}`));
        } else {
          console.error(red(`❌ ${result.message}`));
          Deno.exit(1);
        }
        break;
      }

      case "status": {
        const status = await taskManager.getStatus();
        console.log(cyan("📊 Task Status:"));
        console.log(`   Total Commands: ${status.totalCommands}`);
        console.log(`   Completed: ${status.completed}`);
        console.log(`   In Progress: ${status.inProgress}`);
        console.log(`   Available: ${status.available}`);
        console.log(`   Stale Claims: ${status.stale}`);
        break;
      }

      case "cleanup": {
        const result = await taskManager.cleanup();
        if (result.success) {
          console.log(green(`✅ ${result.message}`));
        } else {
          console.error(red(`❌ ${result.message}`));
          Deno.exit(1);
        }
        break;
      }

      default:
        console.error(red(`❌ Unknown command: ${command}`));
        Deno.exit(1);
    }
  } catch (error) {
    console.error(red(`❌ Fatal error: ${error.message}`));
    Deno.exit(1);
  }
}

if (import.meta.main) {
  await main();
}
