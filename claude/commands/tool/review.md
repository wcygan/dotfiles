# /review

Provide comprehensive review of @[target-files] or $ARGUMENT with context-aware analysis. Think about architectural patterns, security implications, and maintainability when reviewing complex codebases.

## Automatic Context Loading

Review with full project context:

- **Project Configuration**: @package.json @deno.json @Cargo.toml @go.mod
- **TypeScript Config**: @tsconfig.json @*.d.ts
- **Documentation**: @README.md @CLAUDE.md @CHANGELOG.md
- **Testing**: @**/_.test._ @**/_.spec._
- **Configuration**: @docker-compose.yml @.env.example

## Review Framework

### Code Quality Analysis

- **Architecture**: Design patterns, separation of concerns, modularity
- **Security**: Input validation, authentication, authorization, data handling
- **Performance**: Algorithms, database queries, caching, memory usage
- **Maintainability**: Code clarity, documentation, testing coverage
- **Dependencies**: Security vulnerabilities, license compatibility, version currency

### Output Format

#### Strengths

- What's working well architecturally and implementation-wise

#### Critical Issues

- Security vulnerabilities, performance bottlenecks, architectural problems

#### Improvement Recommendations

1. **High Priority**: Security and stability fixes
2. **Medium Priority**: Performance and maintainability improvements
3. **Low Priority**: Code style and documentation enhancements

#### Technical Debt Assessment

- **Immediate**: Issues requiring urgent attention
- **Short-term**: Next sprint/iteration improvements
- **Long-term**: Strategic refactoring opportunities

Keep analysis precise and actionable. Focus on high-impact improvements.
