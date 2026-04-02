#!/usr/bin/env bun
/**
 * buddy-reroll.mjs — Brute-force a Claude Code buddy with desired rarity/species.
 *
 * MUST be run with `bun` (not node) to match Claude Code's Bun.hash().
 *
 * Usage:
 *   bun buddy-reroll.mjs                          # find any legendary
 *   bun buddy-reroll.mjs --rarity legendary        # find any legendary
 *   bun buddy-reroll.mjs --species cat             # find any cat
 *   bun buddy-reroll.mjs --rarity legendary --species cat  # legendary cat
 *   bun buddy-reroll.mjs --rarity epic --species dragon --shiny  # shiny epic dragon
 *   bun buddy-reroll.mjs --list                    # show all species
 *
 * Working example (Legendary Dragon "Rustquill"):
 *   $ bun buddy-reroll.mjs --rarity legendary --species dragon
 *   ✅ Found after 1,579 attempts (0.0s)
 *     userID:  108d8f4c0980f7656a0717503f726116742151a351dc4776d2ecb27d9e7e73d2
 *     rarity:  LEGENDARY
 *     species: dragon
 *     eye:     ✦
 *     hat:     tophat
 *     stats:
 *       DEBUGGING  █████░░░░░  50
 *       PATIENCE   █████░░░░░  53
 *       CHAOS      ██████░░░░  63
 *       WISDOM     ██████████  100
 *       SNARK      ████████░░  80
 */

import { randomBytes } from "crypto";

// ── Constants (exact match to Claude Code source) ────────────────────

const SALT = "friend-2026-401";

const RARITIES = ["common", "uncommon", "rare", "epic", "legendary"];
const RARITY_WEIGHTS = { common: 60, uncommon: 25, rare: 10, epic: 4, legendary: 1 };
const RARITY_TOTAL = Object.values(RARITY_WEIGHTS).reduce((a, b) => a + b, 0);

const SPECIES = [
  "duck", "goose", "blob", "cat", "dragon", "octopus", "owl", "penguin",
  "turtle", "snail", "ghost", "axolotl", "capybara", "cactus", "robot",
  "rabbit", "mushroom", "chonk",
];

const EYES = ["·", "✦", "×", "◉", "@", "°"];
const HATS = ["none", "crown", "tophat", "propeller", "halo", "wizard", "beanie", "tinyduck"];
const STAT_NAMES = ["DEBUGGING", "PATIENCE", "CHAOS", "WISDOM", "SNARK"];
const RARITY_FLOOR = { common: 5, uncommon: 15, rare: 25, epic: 35, legendary: 50 };

// ── Algorithms (exact match to Claude Code source) ───────────────────

function hashString(s) {
  // Claude Code runs on Bun and uses Bun.hash (Wyhash).
  // The FNV-1a fallback only runs in non-Bun environments.
  if (typeof Bun !== "undefined") {
    return Number(BigInt(Bun.hash(s)) & 0xffffffffn);
  }
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function pick(rng, arr) {
  return arr[Math.floor(rng() * arr.length)];
}

function rollRarity(rng) {
  let roll = rng() * RARITY_TOTAL;
  for (const rarity of RARITIES) {
    roll -= RARITY_WEIGHTS[rarity];
    if (roll < 0) return rarity;
  }
  return "common";
}

function rollStats(rng, rarity) {
  const floor = RARITY_FLOOR[rarity];
  const peak = pick(rng, STAT_NAMES);
  // Must use pick() (not filter+pick) to advance the RNG identically to Claude Code
  let dump = pick(rng, STAT_NAMES);
  while (dump === peak) dump = pick(rng, STAT_NAMES);

  const stats = {};
  for (const name of STAT_NAMES) {
    if (name === peak) {
      stats[name] = Math.min(100, floor + 50 + Math.floor(rng() * 30));
    } else if (name === dump) {
      stats[name] = Math.max(1, floor - 10 + Math.floor(rng() * 15));
    } else {
      stats[name] = floor + Math.floor(rng() * 40);
    }
  }
  return stats;
}

function rollFull(rng) {
  const rarity = rollRarity(rng);
  return {
    rarity,
    species: pick(rng, SPECIES),
    eye: pick(rng, EYES),
    hat: rarity === "common" ? "none" : pick(rng, HATS),
    shiny: rng() < 0.01,
    stats: rollStats(rng, rarity),
  };
}

function rollForId(userId) {
  const rng = mulberry32(hashString(userId + SALT));
  return rollFull(rng);
}

// ── Output ───────────────────────────────────────────────────────────

function statBar(val) {
  const filled = Math.round(val / 10);
  return "\u2588".repeat(filled) + "\u2591".repeat(10 - filled);
}

function printResult(userId, r) {
  const stats = Object.entries(r.stats)
    .map(([name, val]) => `    ${name.padEnd(10)} ${statBar(val)}  ${val}`)
    .join("\n");

  console.log([
    `  userID:  ${userId}`,
    `  rarity:  ${r.rarity.toUpperCase()}${r.shiny ? " \u2728 SHINY" : ""}`,
    `  species: ${r.species}`,
    `  eye:     ${r.eye}`,
    `  hat:     ${r.hat}`,
    `  stats:`,
    stats,
  ].join("\n"));
}

function printInstructions() {
  console.log(`
\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510
\u2502  HOW TO APPLY                                   \u2502
\u251c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2524
\u2502  1. Close Claude Code                           \u2502
\u2502  2. Edit ~/.claude.json:                        \u2502
\u2502     - Set "userID" to the value above           \u2502
\u2502     - Remove "accountUuid" from oauthAccount    \u2502
\u2502     - Delete the entire "companion" object      \u2502
\u2502  3. Restart Claude Code and run /buddy          \u2502
\u2502                                                 \u2502
\u2502  \u26a0  If Anthropic forces a re-login, it may     \u2502
\u2502     restore accountUuid. Just remove it again.  \u2502
\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518`);
}

// ── CLI ──────────────────────────────────────────────────────────────

const args = process.argv.slice(2);

if (args.includes("--list")) {
  console.log("Species:", SPECIES.join(", "));
  console.log("Rarities:", RARITIES.join(", "));
  process.exit(0);
}

const checkIdx = args.indexOf("--check");
if (checkIdx !== -1) {
  const id = args[checkIdx + 1];
  if (!id) { console.error("Usage: --check <userId>"); process.exit(1); }
  printResult(id, rollForId(id));
  process.exit(0);
}

// Parse search filters
let wantRarity = null;
let wantSpecies = null;
let wantShiny = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--rarity" && args[i + 1]) wantRarity = args[++i];
  if (args[i] === "--species" && args[i + 1]) wantSpecies = args[++i];
  if (args[i] === "--shiny") wantShiny = true;
}

if (!wantRarity && !wantSpecies && !wantShiny) wantRarity = "legendary";

if (wantRarity && !RARITIES.includes(wantRarity)) {
  console.error(`Invalid rarity: ${wantRarity}. Options: ${RARITIES.join(", ")}`);
  process.exit(1);
}
if (wantSpecies && !SPECIES.includes(wantSpecies)) {
  console.error(`Invalid species: ${wantSpecies}. Options: ${SPECIES.join(", ")}`);
  process.exit(1);
}

const target = [wantRarity, wantSpecies, wantShiny && "shiny"].filter(Boolean).join(" ");
const startTime = Date.now();
const elapsed = () => ((Date.now() - startTime) / 1000).toFixed(1);

console.log(`Searching for: ${target}`);
console.log("Press Ctrl+C to stop.\n");

// Brute-force loop with early exit — skip full stat rolls when rarity/species already fail
let attempts = 0;
while (true) {
  const userId = String(attempts++);
  const rng = mulberry32(hashString(userId + SALT));

  const rarity = rollRarity(rng);
  if (wantRarity && rarity !== wantRarity) continue;

  const species = pick(rng, SPECIES);
  if (wantSpecies && species !== wantSpecies) continue;

  // Rarity + species match — build the full result
  const eye = pick(rng, EYES);
  const hat = rarity === "common" ? "none" : pick(rng, HATS);
  const shiny = rng() < 0.01;
  if (wantShiny && !shiny) continue;

  const result = { rarity, species, eye, hat, shiny, stats: rollStats(rng, rarity) };
  console.log(`\n✅ Found after ${attempts.toLocaleString()} attempts (${elapsed()}s)\n`);
  printResult(userId, result);
  printInstructions();
  process.exit(0);
}
