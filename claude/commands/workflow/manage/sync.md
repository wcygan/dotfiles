Synchronize configurations across editors:

1. Analyze existing configurations:
   - Read keybindings from cursor/keybindings.json
   - Read keybindings from vscode/keybindings.json
   - Read keybindings from zed/keymap.json
   - Compare settings across all editors

2. Identify patterns and inconsistencies:
   - Find common keybindings across editors
   - Detect conflicting assignments
   - List editor-specific bindings
   - Identify missing mappings

3. Generate synchronization report:
   ```
   Common Keybindings:
   - cmd+k cmd+t: Run tests (all editors)
   - cmd+shift+p: Command palette (all editors)

   Inconsistencies:
   - Toggle terminal: cmd+` (vscode) vs ctrl+` (cursor)
   - Format document: different across editors

   Missing in specific editors:
   - Zed: Missing test runner keybinding
   ```

4. Suggest harmonization:
   - Propose unified keybinding scheme
   - Respect editor-specific conventions
   - Maintain muscle memory where possible
   - Account for platform differences

5. Create Deno sync script:
   ```typescript
   // scripts/sync-editor-configs.ts
   import { parse, stringify } from "@std/json";

   // Read all config files
   // Extract common patterns
   // Apply consistent mappings
   // Write updated configs
   ```

6. Add to deno.json:
   ```json
   {
     "tasks": {
       "sync:editors": "deno run --allow-all scripts/sync-editor-configs.ts"
     }
   }
   ```

7. Provide manual sync instructions:
   - Which settings should remain editor-specific
   - How to test synchronized configs
   - Rollback procedure if needed
