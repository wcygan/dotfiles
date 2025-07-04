#!/usr/bin/env -S deno run --allow-env

/**
 * Simple hello world script to test ~/.tools installation
 */

console.log("Hello from ~/.tools! 👋");
console.log(`Current time: ${new Date().toLocaleString()}`);
console.log(`Running as: ${Deno.env.get("USER") || "unknown user"}`);
