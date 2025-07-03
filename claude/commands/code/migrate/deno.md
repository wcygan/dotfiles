Convert existing shell scripts to Deno TypeScript scripts.

Search the repository for shell scripts (.sh, .bash files) and convert them to modern Deno TypeScript scripts. Place the converted scripts in a /scripts directory and properly configure them in deno.json.

## Steps:

1. Find all shell scripts in the repository (*.sh, *.bash files)
2. Analyze each script to understand its purpose and functionality
3. Convert shell commands to Deno TypeScript equivalents using Dax and Deno APIs
4. Create TypeScript files in /scripts directory with descriptive names
5. Add corresponding tasks to deno.json for easy execution
6. Preserve original functionality while improving cross-platform compatibility, type safety, and error handling

## Translation Guide

### Basic Command Execution

```bash
# Shell
echo "Hello World"
ls -la
```

```typescript
// Deno with Dax
import $ from "jsr:@david/dax@0.42.0";
await $`echo "Hello World"`;
await $`ls -la`;
```

### Environment Variables

```bash
# Shell
export VAR1=value1
export VAR2=value2
echo $VAR1 $VAR2
```

```typescript
// Deno
await $`echo $VAR1 $VAR2`
  .env("VAR1", "value1")
  .env({ VAR2: "value2" });

// Or export to current process
await $`export MY_VALUE=5`.exportEnv();
```

### File Operations

```bash
# Shell
mkdir -p src/components
cp config.json config.backup.json
rm -rf temp/
```

```typescript
// Deno
await $`mkdir -p src/components`;
await $`cp config.json config.backup.json`;
await $`rm -rf temp/`;

// Or use Deno APIs for better cross-platform support
import { ensureDir } from "jsr:@std/fs";
await ensureDir("src/components");
await Deno.copyFile("config.json", "config.backup.json");
await Deno.remove("temp/", { recursive: true });
```

### Piping and Redirects

```bash
# Shell
cat file.txt | grep "pattern" > output.txt
ps aux | grep node
```

```typescript
// Deno
await $`cat file.txt | grep "pattern" > output.txt`;
const nodeProcesses = await $`ps aux | grep node`.text();
```

### Error Handling

```bash
# Shell
command1 || echo "Command failed"
set -e  # Exit on error
```

```typescript
// Deno - Default throws on error
try {
  await $`command1`;
} catch (error) {
  console.log("Command failed");
}

// Or disable throwing
const result = await $`command1`.noThrow();
if (result.code !== 0) {
  console.log("Command failed");
}

// Shell-style fallback
await $`command1 || echo "Command failed"`;
```

### Conditional Logic

```bash
# Shell
if [ -f "config.json" ]; then
  echo "Config exists"
fi
```

```typescript
// Deno
import { exists } from "jsr:@std/fs";
if (await exists("config.json")) {
  await $`echo "Config exists"`;
}
```

### Working with Arguments

```bash
# Shell
#!/bin/bash
FILE=$1
OPTION=$2
./process.sh "$FILE" --option "$OPTION"
```

```typescript
// Deno
import { parseArgs } from "jsr:@std/cli/parse-args";

const args = parseArgs(Deno.args);
const file = args._[0];
const option = args.option;
await $`./process.sh ${file} --option ${option}`;
```

### Common Patterns

#### Multiple Commands

```bash
# Shell
cd src && npm install && npm test
```

```typescript
// Deno
await $`cd src && npm install && npm test`;
```

#### Parallel Execution

```bash
# Shell (complex with wait)
command1 &
command2 &
wait
```

```typescript
// Deno
await Promise.all([
  $`command1`,
  $`command2`,
]);
```

#### Getting Command Output

```bash
# Shell
RESULT=$(echo "hello" | tr '[:lower:]' '[:upper:]')
```

```typescript
// Deno
const result = await $`echo "hello" | tr '[:lower:]' '[:upper:]'`.text();
```

Focus on creating idiomatic Deno code that follows the project's conventions and leverages Deno's built-in APIs where appropriate for better cross-platform support.
