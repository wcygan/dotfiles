# Zed LLM Provider Configuration

All provider settings live under `"language_models"` in `settings.json`. API keys are stored in the OS keychain, not in settings files. Configure via `agent: open settings` in the command palette.

## Anthropic

- **API key**: console.anthropic.com (needs credits, separate from Claude Pro)
- **Environment variable**: `ANTHROPIC_API_KEY`

```json
{
  "language_models": {
    "anthropic": {
      "available_models": [
        {
          "name": "claude-3-5-sonnet-20240620",
          "display_name": "Sonnet 2024-June",
          "max_tokens": 128000,
          "max_output_tokens": 2560,
          "cache_configuration": {
            "max_cache_anchors": 10,
            "min_total_token": 10000
          }
        }
      ]
    }
  }
}
```

**Extended thinking**: `"mode": {"type": "thinking", "budget_tokens": 4096}`

## OpenAI

- **API key**: platform.openai.com (needs credits)
- **Environment variable**: `OPENAI_API_KEY`

```json
{
  "language_models": {
    "openai": {
      "available_models": [
        {
          "name": "gpt-5.2",
          "display_name": "gpt-5.2 high",
          "reasoning_effort": "high",
          "max_tokens": 272000,
          "max_completion_tokens": 20000
        }
      ]
    }
  }
}
```

## Google AI (Gemini)

- **API key**: aistudio.google.com
- **Environment variable**: `GEMINI_API_KEY`

```json
{
  "language_models": {
    "google": {
      "available_models": [
        {
          "name": "gemini-3.1-pro-preview",
          "display_name": "Gemini 3.1 Pro",
          "max_tokens": 1000000,
          "mode": { "type": "thinking", "budget_tokens": 24000 }
        }
      ]
    }
  }
}
```

## Amazon Bedrock

Three authentication methods:

**Named Profile (recommended)**:
```json
{
  "language_models": {
    "bedrock": {
      "authentication_method": "named_profile",
      "region": "your-aws-region",
      "profile": "your-profile-name"
    }
  }
}
```

**Required IAM permissions**: `bedrock:InvokeModel`, `bedrock:InvokeModelWithResponseStream`

**Cross-region inference**: `"allow_global": true`
**Extended context (1M tokens for Claude)**: `"allow_extended_context": true`

## DeepSeek

- **API key**: platform.deepseek.com
- **Environment variable**: `DEEPSEEK_API_KEY`

```json
{
  "language_models": {
    "deepseek": {
      "api_url": "https://api.deepseek.com",
      "available_models": [
        { "name": "deepseek-chat", "display_name": "DeepSeek Chat", "max_tokens": 64000 },
        { "name": "deepseek-reasoner", "display_name": "DeepSeek Reasoner", "max_tokens": 64000, "max_output_tokens": 4096 }
      ]
    }
  }
}
```

## GitHub Copilot Chat

- Sign in via Agent Panel settings modal
- Alternative: `GH_COPILOT_TOKEN` environment variable
- Enterprise: configure custom endpoint

## Mistral

- **API key**: console.mistral.ai
- **Environment variable**: `MISTRAL_API_KEY`
- **Pre-configured**: codestral-latest, mistral-large-latest, mistral-medium-latest, mistral-small-latest, open-mistral-nemo, open-codestral-mamba

```json
{
  "language_models": {
    "mistral": {
      "api_url": "https://api.mistral.ai/v1",
      "available_models": [
        {
          "name": "mistral-tiny-latest",
          "display_name": "Mistral Tiny",
          "max_tokens": 32000,
          "max_output_tokens": 4096,
          "supports_tools": true,
          "supports_images": false
        }
      ]
    }
  }
}
```

## Ollama

- **Download**: ollama.com/download, then `ollama serve`
- **Environment variable**: `OLLAMA_API_KEY` (for remote instances)

```json
{
  "language_models": {
    "ollama": {
      "api_url": "http://localhost:11434",
      "auto_discover": false,
      "context_window": 8192,
      "available_models": [
        {
          "name": "qwen2.5-coder",
          "display_name": "qwen 2.5 coder",
          "max_tokens": 32768,
          "supports_tools": true,
          "supports_thinking": true,
          "supports_images": true,
          "keep_alive": "5m"
        }
      ]
    }
  }
}
```

## OpenRouter

- **API key**: openrouter.ai/settings/keys
- **Environment variable**: `OPENROUTER_API_KEY`

```json
{
  "language_models": {
    "open_router": {
      "api_url": "https://openrouter.ai/api/v1",
      "available_models": [
        {
          "name": "google/gemini-2.0-flash-thinking-exp",
          "display_name": "Gemini 2.0 Flash (Thinking)",
          "max_tokens": 200000,
          "supports_tools": true,
          "supports_images": true,
          "mode": { "type": "thinking", "budget_tokens": 8000 }
        }
      ]
    }
  }
}
```

**Provider routing**:
```json
{
  "provider": {
    "order": ["anthropic", "openai"],
    "allow_fallbacks": true,
    "only": ["anthropic", "openai", "google"]
  }
}
```

## xAI (Grok)

- **API key**: console.x.ai
- **Environment variable**: `XAI_API_KEY`

```json
{
  "language_models": {
    "x_ai": {
      "api_url": "https://api.x.ai/v1",
      "available_models": [
        { "name": "grok-1.5", "display_name": "Grok 1.5", "max_tokens": 131072, "max_output_tokens": 8192 }
      ]
    }
  }
}
```

## Vercel AI Gateway

- **API key**: vercel.com AI Gateway keys
- **Environment variable**: `VERCEL_AI_GATEWAY_API_KEY`

## LM Studio

- Download from lmstudio.ai, run `lms server start`
- Model download: `lms get qwen2.5-coder-7b`

## OpenAI-Compatible (Together AI, Anyscale, etc.)

```json
{
  "language_models": {
    "openai_compatible": {
      "Together AI": {
        "api_url": "https://api.together.xyz/v1",
        "available_models": [
          {
            "name": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "display_name": "Together Mixtral 8x7B",
            "max_tokens": 32768,
            "capabilities": {
              "tools": true,
              "images": false,
              "parallel_tool_calls": false,
              "prompt_cache_key": false
            }
          }
        ]
      }
    }
  }
}
```

API key env var: `<PROVIDER_NAME>_API_KEY` (e.g., `TOGETHER_AI_API_KEY`)

## Custom Provider Endpoints

Override API URL for compatible providers (`anthropic`, `google`, `ollama`, `openai`):

```json
{
  "language_models": {
    "anthropic": {
      "api_url": "http://custom-endpoint.com"
    }
  }
}
```
