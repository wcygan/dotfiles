---
name: TODO-skill-name
description: >
  TODO one-sentence summary. Requires TODO-API credentials; Hermes prompts
  for them on first use.
version: 0.1.0
metadata:
  hermes:
    category: TODO-category
    tags: [TODO]
required_environment_variables:
  - name: TODO_API_KEY
    prompt: Enter your TODO API key
    help: https://TODO.example.com/settings/api-keys
    required_for: Authenticating against the TODO API
---

# TODO Skill Title

## When to Use

TODO: 2-4 sentences on trigger scenarios. Mention the service by name
(TODO) so the agent matches it against user requests.

## Procedure

1. Ensure `TODO_API_KEY` is present in the environment. Hermes will prompt
   interactively on first use if it isn't.
2. TODO: make the API call / perform the operation.
3. TODO: format and return results.

## Pitfalls

- Never echo `TODO_API_KEY` in logs or error messages.
- TODO: rate-limit or quota considerations.
- TODO: service-specific error handling.

## Verification

- API call returns a 2xx response.
- TODO: user-visible signal of success.
