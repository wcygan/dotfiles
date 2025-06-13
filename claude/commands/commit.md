Generate a conventional commit message following https://www.conventionalcommits.org/en/v1.0.0/ specification and create the commit automatically.

Steps:

1. Analyze the current git changes using `git status` and `git diff --staged`
2. Determine the appropriate commit type (feat, fix, docs, style, refactor, test, chore, etc.)
3. Identify the scope if applicable (component, module, or area affected)
4. Write a concise description in imperative mood (50 chars or less)
5. Add a detailed body if the change is complex (wrap at 72 chars)
6. Include breaking change footer if applicable
7. Format as: `type(scope): description`
8. Create the commit with the generated message

Example formats:

- `feat(auth): add OAuth2 login support`
- `fix(api): resolve null pointer in user endpoint`
- `docs: update installation instructions`
- `chore(deps): bump lodash to 4.17.21`

Generate the most appropriate commit message based on the changes and commit automatically.
