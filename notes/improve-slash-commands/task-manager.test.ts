#!/usr/bin/env -S deno test --allow-read --allow-write --allow-run

import { assertEquals, assertExists, assertStringIncludes } from "@std/assert";
import { delay } from "@std/async/delay";

interface TestProgressData {
  version: string;
  totalCommands: number;
  completed: number;
  inProgress: number;
  lastUpdated: string;
  commands: Array<{
    id: string;
    name: string;
    filepath: string;
    namespace: string;
    status: "pending" | "in-progress" | "completed";
    lastModified: string;
    claimedBy?: {
      sessionId: string;
      timestamp: number;
    };
    improvements?: string[];
  }>;
}

async function createTestProgressFile(tempDir: string): Promise<string> {
  const progressFile = `${tempDir}/progress.json`;

  const testData: TestProgressData = {
    version: "1.0",
    totalCommands: 5,
    completed: 0,
    inProgress: 0,
    lastUpdated: new Date().toISOString(),
    commands: [
      {
        id: "001",
        name: "test-command-1",
        filepath: "claude/commands/test/test-command-1.md",
        namespace: "test",
        status: "pending",
        lastModified: new Date().toISOString(),
      },
      {
        id: "002",
        name: "test-command-2",
        filepath: "claude/commands/test/test-command-2.md",
        namespace: "test",
        status: "pending",
        lastModified: new Date().toISOString(),
      },
      {
        id: "003",
        name: "test-command-3",
        filepath: "claude/commands/test/test-command-3.md",
        namespace: "test",
        status: "pending",
        lastModified: new Date().toISOString(),
      },
      {
        id: "004",
        name: "test-command-4",
        filepath: "claude/commands/test/test-command-4.md",
        namespace: "test",
        status: "pending",
        lastModified: new Date().toISOString(),
      },
      {
        id: "005",
        name: "test-command-5",
        filepath: "claude/commands/test/test-command-5.md",
        namespace: "test",
        status: "pending",
        lastModified: new Date().toISOString(),
      },
    ],
  };

  await Deno.writeTextFile(progressFile, JSON.stringify(testData, null, 2));
  return progressFile;
}

async function runTaskManager(args: string[]): Promise<{
  success: boolean;
  stdout: string;
  stderr: string;
}> {
  const cmd = new Deno.Command("deno", {
    args: ["run", "--allow-read", "--allow-write", "task-manager.ts", ...args],
    cwd: Deno.cwd(),
    stdout: "piped",
    stderr: "piped",
  });

  const { code, stdout, stderr } = await cmd.output();

  return {
    success: code === 0,
    stdout: new TextDecoder().decode(stdout),
    stderr: new TextDecoder().decode(stderr),
  };
}

Deno.test("TaskManager - Basic claim and complete workflow", async () => {
  const tempDir = await Deno.makeTempDir();
  const progressFile = await createTestProgressFile(tempDir);

  try {
    // Claim a task
    const claimResult = await runTaskManager([
      "claim",
      "--progress-file",
      progressFile,
    ]);
    assertEquals(claimResult.success, true);
    assertStringIncludes(claimResult.stdout, "Successfully claimed task:");
    assertStringIncludes(claimResult.stdout, "Command ID:");
    assertStringIncludes(claimResult.stdout, "Session ID:");

    // Extract command ID and session ID from output
    const commandIdMatch = claimResult.stdout.match(/🆔 Command ID: (\w+)/);
    const sessionIdMatch = claimResult.stdout.match(/🔗 Session ID: (\w+)/);

    assertExists(commandIdMatch);
    assertExists(sessionIdMatch);

    const commandId = commandIdMatch[1];
    const sessionId = sessionIdMatch[1];

    // Complete the task
    const completeResult = await runTaskManager([
      "complete",
      "--progress-file",
      progressFile,
      "--command-id",
      commandId,
      "--session-id",
      sessionId,
      "--improvement",
      "frontMatterAdded",
      "--improvement",
      "dynamicContextAdded",
    ]);

    assertEquals(completeResult.success, true);
    assertStringIncludes(completeResult.stdout, "Successfully completed task:");
    assertStringIncludes(completeResult.stdout, "(1/5)");

    // Verify progress file was updated
    const progressData = JSON.parse(await Deno.readTextFile(progressFile));
    assertEquals(progressData.completed, 1);
    assertEquals(progressData.inProgress, 0);

    const completedCommand = progressData.commands.find((cmd) => cmd.id === commandId);
    assertEquals(completedCommand.status, "completed");
    assertEquals(completedCommand.improvements, [
      "frontMatterAdded",
      "dynamicContextAdded",
    ]);
    assertEquals(completedCommand.claimedBy, undefined);
  } finally {
    await Deno.remove(tempDir, { recursive: true });
  }
});

Deno.test("TaskManager - Concurrent claims prevent double booking", async () => {
  const tempDir = await Deno.makeTempDir();
  const progressFile = await createTestProgressFile(tempDir);

  try {
    // Start multiple concurrent claim attempts
    const claimPromises = Array.from(
      { length: 10 },
      () => runTaskManager(["claim", "--progress-file", progressFile]),
    );

    const results = await Promise.all(claimPromises);

    // Count successful claims
    const successfulClaims = results.filter((r) => r.success);
    const failedClaims = results.filter((r) => !r.success);

    // With high concurrency and file locking, we expect fewer successful claims
    // due to lock conflicts, but we should get some claims through
    assertEquals(
      successfulClaims.length >= 1,
      true,
      `Should claim at least 1 task, got ${successfulClaims.length}`,
    );
    assertEquals(
      successfulClaims.length <= 5,
      true,
      `Should not claim more than 5 tasks, got ${successfulClaims.length}`,
    );

    // All failed claims should indicate no available commands or lock conflicts
    for (const failed of failedClaims) {
      const hasExpectedMessage = failed.stdout.includes("No claimable commands available") ||
        failed.stdout.includes(
          "Another task manager instance is already running",
        );
      assertEquals(
        hasExpectedMessage,
        true,
        `Unexpected failure message: ${failed.stdout} ${failed.stderr}`,
      );
    }

    // Verify all successful claims have unique command IDs
    const claimedCommandIds = new Set();
    const claimedSessionIds = new Set();

    for (const claim of successfulClaims) {
      const commandIdMatch = claim.stdout.match(/🆔 Command ID: (\w+)/);
      const sessionIdMatch = claim.stdout.match(/🔗 Session ID: (\w+)/);

      if (commandIdMatch && sessionIdMatch) {
        const commandId = commandIdMatch[1];
        const sessionId = sessionIdMatch[1];

        assertEquals(
          claimedCommandIds.has(commandId),
          false,
          `Command ${commandId} was claimed multiple times`,
        );
        assertEquals(
          claimedSessionIds.has(sessionId),
          false,
          `Session ${sessionId} claimed multiple commands`,
        );

        claimedCommandIds.add(commandId);
        claimedSessionIds.add(sessionId);
      }
    }

    // Verify progress file shows claimed commands as in-progress
    const progressData = JSON.parse(await Deno.readTextFile(progressFile));
    assertEquals(progressData.inProgress, successfulClaims.length);
    assertEquals(progressData.completed, 0);
  } finally {
    await Deno.remove(tempDir, { recursive: true });
  }
});

Deno.test("TaskManager - Stale claim recovery", async () => {
  const tempDir = await Deno.makeTempDir();
  const progressFile = await createTestProgressFile(tempDir);

  try {
    // Create a stale claim by manually editing the progress file
    const progressData = JSON.parse(await Deno.readTextFile(progressFile));
    progressData.commands[0].status = "in-progress";
    progressData.commands[0].claimedBy = {
      sessionId: "stale-session-123",
      timestamp: Math.floor(Date.now() / 1000) - 700, // 700 seconds ago (> 10 minutes)
    };
    progressData.inProgress = 1;

    await Deno.writeTextFile(
      progressFile,
      JSON.stringify(progressData, null, 2),
    );

    // Attempt to claim - should recover the stale claim
    const claimResult = await runTaskManager([
      "claim",
      "--progress-file",
      progressFile,
    ]);
    assertEquals(claimResult.success, true);
    assertStringIncludes(
      claimResult.stdout,
      "Successfully claimed task: test-command-1",
    );

    // Verify the stale claim was recovered
    const updatedData = JSON.parse(await Deno.readTextFile(progressFile));
    const reclaimedCommand = updatedData.commands[0];
    assertEquals(reclaimedCommand.status, "in-progress");
    assertEquals(
      reclaimedCommand.claimedBy.sessionId !== "stale-session-123",
      true,
    );
  } finally {
    await Deno.remove(tempDir, { recursive: true });
  }
});

Deno.test("TaskManager - Cleanup command removes stale claims", async () => {
  const tempDir = await Deno.makeTempDir();
  const progressFile = await createTestProgressFile(tempDir);

  try {
    // Create multiple stale claims
    const progressData = JSON.parse(await Deno.readTextFile(progressFile));
    const staleTimestamp = Math.floor(Date.now() / 1000) - 700; // 700 seconds ago

    progressData.commands[0].status = "in-progress";
    progressData.commands[0].claimedBy = {
      sessionId: "stale-1",
      timestamp: staleTimestamp,
    };

    progressData.commands[1].status = "in-progress";
    progressData.commands[1].claimedBy = {
      sessionId: "stale-2",
      timestamp: staleTimestamp,
    };

    progressData.commands[2].status = "in-progress";
    progressData.commands[2].claimedBy = {
      sessionId: "fresh",
      timestamp: Math.floor(Date.now() / 1000) - 60,
    }; // 1 minute ago (not stale)

    progressData.inProgress = 3;

    await Deno.writeTextFile(
      progressFile,
      JSON.stringify(progressData, null, 2),
    );

    // Run cleanup
    const cleanupResult = await runTaskManager([
      "cleanup",
      "--progress-file",
      progressFile,
    ]);
    assertEquals(cleanupResult.success, true);
    assertStringIncludes(
      cleanupResult.stdout,
      "Cleanup completed. Recovered 2 stale claims.",
    );

    // Verify cleanup results
    const cleanedData = JSON.parse(await Deno.readTextFile(progressFile));
    assertEquals(cleanedData.inProgress, 1); // Only the fresh claim remains

    // Check that stale claims were released
    assertEquals(cleanedData.commands[0].status, "pending");
    assertEquals(cleanedData.commands[0].claimedBy, undefined);

    assertEquals(cleanedData.commands[1].status, "pending");
    assertEquals(cleanedData.commands[1].claimedBy, undefined);

    // Fresh claim should remain
    assertEquals(cleanedData.commands[2].status, "in-progress");
    assertEquals(cleanedData.commands[2].claimedBy.sessionId, "fresh");
  } finally {
    await Deno.remove(tempDir, { recursive: true });
  }
});

Deno.test("TaskManager - Status command shows accurate counts", async () => {
  const tempDir = await Deno.makeTempDir();
  const progressFile = await createTestProgressFile(tempDir);

  try {
    // Set up mixed state
    const progressData = JSON.parse(await Deno.readTextFile(progressFile));

    // 1 completed
    progressData.commands[0].status = "completed";

    // 1 in-progress (fresh)
    progressData.commands[1].status = "in-progress";
    progressData.commands[1].claimedBy = {
      sessionId: "fresh",
      timestamp: Math.floor(Date.now() / 1000) - 60,
    };

    // 1 in-progress (stale)
    progressData.commands[2].status = "in-progress";
    progressData.commands[2].claimedBy = {
      sessionId: "stale",
      timestamp: Math.floor(Date.now() / 1000) - 700,
    };

    // 2 pending (commands[3] and commands[4])

    progressData.completed = 1;
    progressData.inProgress = 2;

    await Deno.writeTextFile(
      progressFile,
      JSON.stringify(progressData, null, 2),
    );

    // Get status
    const statusResult = await runTaskManager([
      "status",
      "--progress-file",
      progressFile,
    ]);
    assertEquals(statusResult.success, true);

    assertStringIncludes(statusResult.stdout, "Total Commands: 5");
    assertStringIncludes(statusResult.stdout, "Completed: 1");
    assertStringIncludes(statusResult.stdout, "In Progress: 2");
    assertStringIncludes(statusResult.stdout, "Available: 3"); // 2 pending + 1 stale
    assertStringIncludes(statusResult.stdout, "Stale Claims: 1");
  } finally {
    await Deno.remove(tempDir, { recursive: true });
  }
});

Deno.test("TaskManager - Release task functionality", async () => {
  const tempDir = await Deno.makeTempDir();
  const progressFile = await createTestProgressFile(tempDir);

  try {
    // Claim a task first
    const claimResult = await runTaskManager([
      "claim",
      "--progress-file",
      progressFile,
    ]);
    assertEquals(claimResult.success, true);

    const commandIdMatch = claimResult.stdout.match(/🆔 Command ID: (\w+)/);
    const sessionIdMatch = claimResult.stdout.match(/🔗 Session ID: (\w+)/);

    assertExists(commandIdMatch);
    assertExists(sessionIdMatch);

    const commandId = commandIdMatch[1];
    const sessionId = sessionIdMatch[1];

    // Release the task
    const releaseResult = await runTaskManager([
      "release",
      "--progress-file",
      progressFile,
      "--command-id",
      commandId,
      "--session-id",
      sessionId,
    ]);

    assertEquals(releaseResult.success, true);
    assertStringIncludes(releaseResult.stdout, "Successfully released task:");

    // Verify task is back to pending
    const progressData = JSON.parse(await Deno.readTextFile(progressFile));
    const releasedCommand = progressData.commands.find((cmd) => cmd.id === commandId);
    assertEquals(releasedCommand.status, "pending");
    assertEquals(releasedCommand.claimedBy, undefined);
    assertEquals(progressData.inProgress, 0);
  } finally {
    await Deno.remove(tempDir, { recursive: true });
  }
});

Deno.test("TaskManager - Concurrent lock handling", async () => {
  const tempDir = await Deno.makeTempDir();
  const progressFile = await createTestProgressFile(tempDir);

  try {
    // Start many operations concurrently to test lock handling
    const operations = [
      () => runTaskManager(["claim", "--progress-file", progressFile]),
      () => runTaskManager(["claim", "--progress-file", progressFile]),
      () => runTaskManager(["status", "--progress-file", progressFile]),
      () => runTaskManager(["cleanup", "--progress-file", progressFile]),
      () => runTaskManager(["claim", "--progress-file", progressFile]),
    ];

    // Add small delays to increase chances of overlap
    const delayedOperations = operations.map((op, i) => delay(i * 10).then(() => op()));

    const results = await Promise.all(delayedOperations);

    // At least some operations should succeed (not all fail due to lock conflicts)
    const successCount = results.filter((r) => r.success).length;
    assertEquals(
      successCount >= 3,
      true,
      "Expected at least 3 operations to succeed despite concurrent access",
    );

    // Verify progress file is in valid state
    const progressData = JSON.parse(await Deno.readTextFile(progressFile));
    assertEquals(typeof progressData.totalCommands, "number");
    assertEquals(typeof progressData.completed, "number");
    assertEquals(typeof progressData.inProgress, "number");
    assertEquals(Array.isArray(progressData.commands), true);
  } finally {
    await Deno.remove(tempDir, { recursive: true });
  }
});

Deno.test("TaskManager - Error handling for invalid operations", async () => {
  const tempDir = await Deno.makeTempDir();
  const progressFile = await createTestProgressFile(tempDir);

  try {
    // Try to complete a task that doesn't exist
    const invalidCompleteResult = await runTaskManager([
      "complete",
      "--progress-file",
      progressFile,
      "--command-id",
      "999",
      "--session-id",
      "fake-session",
    ]);

    assertEquals(invalidCompleteResult.success, false);
    assertStringIncludes(
      invalidCompleteResult.stderr,
      "Command with ID 999 not found",
    );

    // Try to complete a task with wrong session ID
    const claimResult = await runTaskManager([
      "claim",
      "--progress-file",
      progressFile,
    ]);
    assertEquals(claimResult.success, true);

    const commandIdMatch = claimResult.stdout.match(/🆔 Command ID: (\w+)/);
    assertExists(commandIdMatch);
    const commandId = commandIdMatch[1];

    const wrongSessionResult = await runTaskManager([
      "complete",
      "--progress-file",
      progressFile,
      "--command-id",
      commandId,
      "--session-id",
      "wrong-session",
    ]);

    assertEquals(wrongSessionResult.success, false);
    assertStringIncludes(
      wrongSessionResult.stderr,
      "not claimed by this session",
    );
  } finally {
    await Deno.remove(tempDir, { recursive: true });
  }
});

Deno.test("TaskManager - Corrupted progress file handling", async () => {
  const tempDir = await Deno.makeTempDir();
  const progressFile = `${tempDir}/progress.json`;

  try {
    // Create a corrupted JSON file
    await Deno.writeTextFile(progressFile, '{"invalid": json syntax}');

    const result = await runTaskManager([
      "status",
      "--progress-file",
      progressFile,
    ]);

    assertEquals(result.success, false);
    assertStringIncludes(result.stderr, "Progress file contains invalid JSON");
  } finally {
    await Deno.remove(tempDir, { recursive: true });
  }
});

Deno.test("TaskManager - Missing progress file handling", async () => {
  const tempDir = await Deno.makeTempDir();
  const progressFile = `${tempDir}/nonexistent.json`;

  try {
    const result = await runTaskManager([
      "claim",
      "--progress-file",
      progressFile,
    ]);

    assertEquals(result.success, false);
    assertStringIncludes(result.stdout, "Progress file not found");
  } finally {
    await Deno.remove(tempDir, { recursive: true });
  }
});

Deno.test("TaskManager - Rapid successive operations", async () => {
  const tempDir = await Deno.makeTempDir();
  const progressFile = await createTestProgressFile(tempDir);

  try {
    // Rapidly claim and release tasks to test timing issues
    const operations = [];

    for (let i = 0; i < 20; i++) {
      operations.push(
        (async () => {
          const claimResult = await runTaskManager([
            "claim",
            "--progress-file",
            progressFile,
          ]);

          if (claimResult.success) {
            const commandIdMatch = claimResult.stdout.match(
              /🆔 Command ID: (\w+)/,
            );
            const sessionIdMatch = claimResult.stdout.match(
              /🔗 Session ID: (\w+)/,
            );

            if (commandIdMatch && sessionIdMatch) {
              // Small delay to simulate work
              await delay(Math.random() * 10);

              // Release the task
              const releaseResult = await runTaskManager([
                "release",
                "--progress-file",
                progressFile,
                "--command-id",
                commandIdMatch[1],
                "--session-id",
                sessionIdMatch[1],
              ]);

              // Only count as successful if both claim and release worked
              return releaseResult.success;
            }
          }

          return claimResult.success;
        })(),
      );
    }

    const results = await Promise.all(operations);
    const successCount = results.filter(Boolean).length;

    // Should have some successful operations without corruption
    // Allow for fewer successes due to lock conflicts in rapid operations
    assertEquals(
      successCount >= 1,
      true,
      "Expected at least 1 successful rapid operation",
    );

    // Verify progress file is still valid
    const finalData = JSON.parse(await Deno.readTextFile(progressFile));
    // In rapid operations with potential failures, allow for some tasks to still be in progress
    assertEquals(
      finalData.inProgress <= 5,
      true,
      "No more than 5 tasks should be in progress",
    );
    assertEquals(Array.isArray(finalData.commands), true);
  } finally {
    await Deno.remove(tempDir, { recursive: true });
  }
});

Deno.test("TaskManager - Session ID uniqueness under rapid operations", async () => {
  const tempDir = await Deno.makeTempDir();
  const progressFile = await createTestProgressFile(tempDir);

  try {
    // Rapidly claim multiple tasks and check session ID uniqueness
    const claimPromises = Array.from(
      { length: 5 },
      () => runTaskManager(["claim", "--progress-file", progressFile]),
    );

    const results = await Promise.all(claimPromises);
    const successfulClaims = results.filter((r) => r.success);

    // In high concurrency, expect fewer successful claims due to lock conflicts
    assertEquals(
      successfulClaims.length >= 1,
      true,
      "At least 1 task should be claimed",
    );
    assertEquals(
      successfulClaims.length <= 5,
      true,
      "No more than 5 tasks should be claimed",
    );

    const sessionIds = new Set();
    for (const claim of successfulClaims) {
      const sessionIdMatch = claim.stdout.match(/🔗 Session ID: (\w+)/);
      if (sessionIdMatch) {
        const sessionId = sessionIdMatch[1];

        assertEquals(
          sessionIds.has(sessionId),
          false,
          `Session ID ${sessionId} was generated multiple times`,
        );
        sessionIds.add(sessionId);
      }
    }

    assertEquals(
      sessionIds.size,
      successfulClaims.length,
      "All session IDs should be unique",
    );
  } finally {
    await Deno.remove(tempDir, { recursive: true });
  }
});

Deno.test("TaskManager - Higher concurrency stress test", async () => {
  const tempDir = await Deno.makeTempDir();

  // Create larger test dataset for stress testing
  const testData: TestProgressData = {
    version: "1.0",
    totalCommands: 50,
    completed: 0,
    inProgress: 0,
    lastUpdated: new Date().toISOString(),
    commands: Array.from({ length: 50 }, (_, i) => ({
      id: String(i + 1).padStart(3, "0"),
      name: `stress-test-command-${i + 1}`,
      filepath: `claude/commands/stress/command-${i + 1}.md`,
      namespace: "stress",
      status: "pending" as const,
      lastModified: new Date().toISOString(),
    })),
  };

  const progressFile = `${tempDir}/progress.json`;
  await Deno.writeTextFile(progressFile, JSON.stringify(testData, null, 2));

  try {
    // Launch 100 concurrent operations (mix of claims, status, cleanup)
    const operations = [];

    // 60 claim attempts
    for (let i = 0; i < 60; i++) {
      operations.push(() => runTaskManager(["claim", "--progress-file", progressFile]));
    }

    // 20 status checks
    for (let i = 0; i < 20; i++) {
      operations.push(() => runTaskManager(["status", "--progress-file", progressFile]));
    }

    // 20 cleanup operations
    for (let i = 0; i < 20; i++) {
      operations.push(() => runTaskManager(["cleanup", "--progress-file", progressFile]));
    }

    // Execute all with small random delays
    const delayedOperations = operations.map((op, _i) =>
      delay(Math.random() * 50).then(() => op())
    );

    const results = await Promise.all(delayedOperations);

    // Verify results
    const claimResults = results.slice(0, 60);
    const statusResults = results.slice(60, 80);
    const cleanupResults = results.slice(80, 100);

    const successfulClaims = claimResults.filter((r) => r.success);
    const successfulStatuses = statusResults.filter((r) => r.success);
    const successfulCleanups = cleanupResults.filter((r) => r.success);

    // In very high concurrency (100 operations), expect significant lock conflicts
    // but should still get some successful claims through
    assertEquals(
      successfulClaims.length >= 5,
      true,
      `Should claim at least 5 of 50 tasks, but got ${successfulClaims.length}. Failed claims: ${
        claimResults.filter((r) => !r.success).length
      }`,
    );
    assertEquals(
      successfulClaims.length <= 50,
      true,
      `Should not claim more than 50 tasks, got ${successfulClaims.length}`,
    );

    // Status operations should mostly succeed (read-only so less affected by locks)
    assertEquals(
      successfulStatuses.length >= 5,
      true,
      "Some status operations should succeed",
    );

    // Cleanup operations may fail frequently due to lock conflicts
    assertEquals(
      successfulCleanups.length >= 1,
      true,
      "At least some cleanup operations should succeed",
    );

    // Verify progress file integrity
    const finalData = JSON.parse(await Deno.readTextFile(progressFile));
    assertEquals(
      finalData.inProgress,
      successfulClaims.length,
      `In-progress count should match successful claims`,
    );
    assertEquals(finalData.completed, 0, "No tasks completed in this test");
    assertEquals(Array.isArray(finalData.commands), true);
    assertEquals(finalData.commands.length, 50);

    // Verify all claimed tasks have unique session IDs
    const claimedTasks = finalData.commands.filter((cmd) => cmd.status === "in-progress");
    const sessionIds = new Set(
      claimedTasks.map((cmd) => cmd.claimedBy?.sessionId),
    );
    assertEquals(
      sessionIds.size,
      claimedTasks.length,
      "All session IDs should be unique",
    );
  } finally {
    await Deno.remove(tempDir, { recursive: true });
  }
});

Deno.test("TaskManager - Real-world scenario with agent interruption", async () => {
  const tempDir = await Deno.makeTempDir();
  const progressFile = await createTestProgressFile(tempDir);

  try {
    // Simulate agent claiming a task
    const claimResult = await runTaskManager([
      "claim",
      "--progress-file",
      progressFile,
    ]);
    assertEquals(claimResult.success, true);

    const commandIdMatch = claimResult.stdout.match(/🆔 Command ID: (\w+)/);
    const sessionIdMatch = claimResult.stdout.match(/🔗 Session ID: (\w+)/);
    assertExists(commandIdMatch);
    assertExists(sessionIdMatch);

    const commandId = commandIdMatch[1];
    const sessionId = sessionIdMatch[1];

    // Verify task is claimed
    const statusResult = await runTaskManager([
      "status",
      "--progress-file",
      progressFile,
    ]);
    assertEquals(statusResult.success, true);
    assertStringIncludes(statusResult.stdout, "In Progress: 1");

    // Simulate agent crash by manually setting stale timestamp
    const progressData = JSON.parse(await Deno.readTextFile(progressFile));
    const claimedCommand = progressData.commands.find((cmd) => cmd.id === commandId);
    claimedCommand.claimedBy.timestamp = Math.floor(Date.now() / 1000) - 700; // 700 seconds ago
    await Deno.writeTextFile(
      progressFile,
      JSON.stringify(progressData, null, 2),
    );

    // Another agent should be able to claim the stale task
    const reclaimResult = await runTaskManager([
      "claim",
      "--progress-file",
      progressFile,
    ]);
    assertEquals(reclaimResult.success, true);
    assertStringIncludes(reclaimResult.stdout, "Successfully claimed task:");

    // Verify the stale task was reclaimed
    const newSessionIdMatch = reclaimResult.stdout.match(
      /🔗 Session ID: (\w+)/,
    );
    assertExists(newSessionIdMatch);
    const newSessionId = newSessionIdMatch[1];

    // Should be a different session ID
    assertEquals(
      sessionId !== newSessionId,
      true,
      "New session should have different ID",
    );

    // Original session should not be able to complete the task
    const invalidCompleteResult = await runTaskManager([
      "complete",
      "--progress-file",
      progressFile,
      "--command-id",
      commandId,
      "--session-id",
      sessionId,
    ]);
    assertEquals(invalidCompleteResult.success, false);
    assertStringIncludes(
      invalidCompleteResult.stderr,
      "not claimed by this session",
    );
  } finally {
    await Deno.remove(tempDir, { recursive: true });
  }
});
