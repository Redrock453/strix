# Z.AI Integration Guide for Strix

## Overview

This guide explains how to configure Strix to use Z.AI's API proxy for accessing Claude Sonnet 4 and other language models.

## Prerequisites

1. Z.AI API Key - Get from [Z.AI API Keys Page](https://z.ai/manage-apikey/apikey-list)
2. Docker running (for Strix sandbox)
3. Poetry installed

## Quick Start

### 1. Configure Environment

Copy the Z.AI configuration template:

```bash
cp .env.zai .env
```

Edit `.env` and replace `YOUR_API_KEY` with your actual Z.AI API key.

### 2. Run Strix

```bash
poetry run strix --target ./your-target
```

## Configuration Details

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ZAI_API_KEY` | Your Z.AI API key | `355782d5d21b47...` |
| `ANTHROPIC_BASE_URL` | Z.AI Anthropic proxy endpoint | `https://api.z.ai/api/anthropic` |
| `STRIX_LLM` | Model to use | `anthropic/claude-sonnet-4-20250514` |
| `LLM_API_KEY` | API key (same as ZAI_API_KEY) | `355782d5d21b47...` |
| `API_TIMEOUT_MS` | Request timeout in milliseconds | `3000000` (50 min) |

### Authentication

Z.AI uses Bearer token authentication. The API key should be provided via:

```bash
Authorization: Bearer YOUR_ZAI_API_KEY
```

Strix automatically handles this when you configure the environment variables.

## Supported Models via Z.AI

### Anthropic Claude Models

- `anthropic/claude-sonnet-4-20250514` - Claude Sonnet 4 (recommended)
- `anthropic/claude-3-5-sonnet-20241022` - Claude 3.5 Sonnet
- `anthropic/claude-3-opus-20240229` - Claude 3 Opus

### Other Models

Z.AI also supports:
- GLM-4.6 and other GLM models
- OpenAI models (via proxy)
- Custom fine-tuned models

## GitHub Codespaces Setup

For persistent configuration in GitHub Codespaces:

1. Go to [GitHub Codespaces Secrets](https://github.com/settings/codespaces)
2. Click "New secret"
3. Add the following secrets:

```
Name: ZAI_API_KEY
Value: your_zai_api_key
Repository: Redrock453/strix
```

```
Name: ANTHROPIC_BASE_URL
Value: https://api.z.ai/api/anthropic
Repository: Redrock453/strix
```

```
Name: STRIX_LLM
Value: anthropic/claude-sonnet-4-20250514
Repository: Redrock453/strix
```

4. Restart your Codespace

## Troubleshooting

### Authentication Error

```
❌ LLM CONNECTION FAILED
AnthropicException - Authorization Failure
```

**Solution:** 
- Verify your Z.AI API key is correct
- Check that `ANTHROPIC_BASE_URL` is set to `https://api.z.ai/api/anthropic`
- Ensure `LLM_API_KEY` matches your `ZAI_API_KEY`

### Timeout Errors

**Solution:** Increase `API_TIMEOUT_MS`:

```bash
export API_TIMEOUT_MS=5000000  # 83 minutes
```

### Model Not Found

**Solution:** Verify the model name matches Z.AI's supported models. Check [Z.AI API Documentation](https://docs.z.ai/api-reference/introduction).

## Example Usage

### Basic Security Scan

```bash
# Local codebase
poetry run strix --target ./my-app

# Remote repository
poetry run strix --target https://github.com/user/repo

# Web application
poetry run strix --target https://example.com
```

### Non-Interactive Mode (CI/CD)

```bash
poetry run strix -n --target ./app --instruction "Focus on authentication vulnerabilities"
```

### Custom Instructions

```bash
poetry run strix --target https://api.example.com \
  --instruction "Perform API security testing focusing on IDOR and broken access control" \
  --run-name "api-security-test"
```

## API Reference

For detailed Z.AI API documentation, visit:
- [API Reference](https://docs.z.ai/api-reference/introduction)
- [Python SDK](https://docs.z.ai/guides/develop/python/introduction)
- [Quick Start Guide](https://docs.z.ai/devpack/quick-start)

## Cost Optimization

Z.AI offers competitive pricing compared to direct Anthropic access. Benefits:

- **3× Usage** - More tokens for your budget
- **1/7 Cost** - Significant cost reduction
- **Built for Developers** - Optimized for coding tasks

See [Z.AI Pricing](https://z.ai/subscribe) for details.

## Support

- **Z.AI Discord**: [Join Community](https://discord.gg/QR7SARHRxK)
- **GitHub Issues**: [Z.AI GitHub](https://github.com/zai-org)
- **Strix Issues**: [Report Issues](https://github.com/usestrix/strix/issues)

## License

This integration guide is part of the Strix project and follows the same Apache 2.0 license.
