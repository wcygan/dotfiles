#!/usr/bin/env -S deno run --allow-env

/**
 * Simple hello world script to test ~/.scripts installation
 */

console.log("Hello from ~/.scripts! 👋");
console.log(`Current time: ${new Date().toLocaleString()}`);
console.log(`Running as: ${Deno.env.get("USER") || "unknown user"}`);
