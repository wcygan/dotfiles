Analyze code in $ARGUMENTS for refactoring opportunities.

Steps:
1. Read and understand the code structure in the specified file/directory
2. Identify code smells and anti-patterns:
   - Long methods/functions (>20 lines)
   - Duplicate code blocks
   - Complex conditionals
   - Large classes/modules
   - Inappropriate intimacy between modules
   - Feature envy
   - Data clumps

3. Suggest specific refactoring techniques:
   - Extract Method/Function
   - Inline Variable/Method
   - Replace Conditional with Polymorphism
   - Extract Class/Module
   - Move Method/Field
   - Rename for clarity
   - Replace Magic Numbers with Constants

4. Verify existing test coverage before refactoring
5. Apply refactoring incrementally:
   - Make one change at a time
   - Run tests after each change
   - Commit working states

6. Document the refactoring rationale in commit messages

Prioritize refactorings by:
- Impact on readability
- Risk of introducing bugs
- Performance improvements
- Future maintainability