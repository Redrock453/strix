# Strix - Z.ai API Integration

## 🦉 Special Z.ai Edition

This is a customized version of **Strix** specifically configured for **Z.ai API** integration with Claude models. This version provides enhanced AI-powered penetration testing capabilities through Z.ai's powerful API infrastructure.

## ✨ What's Included in This Version

### 🔧 Z.ai API Integration
- **Provider**: Anthropic Claude via Z.ai
- **Model**: claude-sonnet-4-20250514
- **Base URL**: https://api.z.ai/api/anthropic
- **Features**: Advanced security testing, vulnerability detection, proof-of-concept generation

### 🛡️ Security Testing Tools
- **HTTP Proxy** - Full request/response manipulation
- **Browser Automation** - Multi-tab testing for XSS, CSRF
- **Terminal Environments** - Interactive shells for exploitation
- **Python Runtime** - Custom exploit development
- **Reconnaissance** - Automated OSINT
- **Code Analysis** - Static and dynamic analysis

### 🕸️ Multi-Agent System
- **Graph of Agents** - Specialized agents for different attacks
- **Distributed Workflows** - Parallel vulnerability scanning
- **Dynamic Coordination** - Agents share discoveries
- **Scalable Testing** - Fast comprehensive coverage

## 📋 System Requirements

- **Python**: 3.12+
- **Docker**: Running (for sandbox environment)
- **Z.ai API Key**: Required for AI functionality
- **Poetry**: For dependency management
- **Playwright**: For browser automation

## 🛠️ Quick Start

### 1. Clone and Configure
```bash
git clone https://github.com/Redrock453/strix.git
cd strix
git checkout zai-integration
```

### 2. Set Up Z.ai API
Run the automated setup script:
```bash
./setup_zai.sh
```

Or manually configure `.env`:
```bash
cp .env.zai .env
```

Edit `.env` with your Z.ai credentials:
```env
ZAI_API_KEY="your_zai_api_key"
ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
ANTHROPIC_API_KEY="${ZAI_API_KEY}"
LLM_API_KEY="${ZAI_API_KEY}"
STRIX_LLM="anthropic/claude-sonnet-4-20250514"
API_TIMEOUT_MS="3000000"
STRIX_SANDBOX_MODE=false
```

### 3. Install Dependencies
```bash
# Install with Poetry
poetry install

# Install Playwright browsers
poetry run playwright install chromium

# Install system dependencies (Linux)
sudo poetry run playwright install-deps
```

### 4. Start Strix

**Interactive Mode (with TUI):**
```bash
poetry run strix --target ./my-app
```

**Non-Interactive Mode (for CI/CD):**
```bash
poetry run strix -n --target https://example.com
```

## 🌍 Usage Examples

### Web Application Testing
```bash
# Black-box web app assessment
poetry run strix --target https://your-app.com

# Grey-box testing with credentials
poetry run strix --target https://your-app.com \
  --instruction "Perform authenticated testing using credentials: user:pass"
```

### Code Repository Analysis
```bash
# GitHub repository
poetry run strix --target https://github.com/org/repo

# Local codebase
poetry run strix --target ./my-project
```

### Multi-Target Testing
```bash
# White-box testing (source + deployed app)
poetry run strix \
  --target https://github.com/org/app \
  --target https://your-app.com
```

### Focused Security Testing
```bash
# Focus on specific vulnerabilities
poetry run strix --target api.example.com \
  --instruction "Focus on business logic flaws and IDOR vulnerabilities"

# Custom run name
poetry run strix --target ./app \
  --instruction "Authentication testing" \
  --run-name "auth-audit-2025"
```

## ⚙️ Configuration

### Z.ai Environment Variables (`.env`)
```env
# Z.ai API Configuration
ZAI_API_KEY="355782d5d21b47cabf29f4cf15393d81.Ez9aXl4hZ3zab2rR"
ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
ANTHROPIC_API_KEY="${ZAI_API_KEY}"
LLM_API_KEY="${ZAI_API_KEY}"

# Model Configuration
STRIX_LLM="anthropic/claude-sonnet-4-20250514"

# API Settings
API_TIMEOUT_MS="3000000"  # 50 minutes

# Strix Settings
STRIX_SANDBOX_MODE=false

# Optional: Search Capabilities
PERPLEXITY_API_KEY="your-perplexity-key"  # For web search
```

### GitHub Codespaces Secrets

For persistent configuration in GitHub Codespaces:

1. Go to [GitHub Codespaces Secrets](https://github.com/settings/codespaces)
2. Click "New secret"
3. Add the following secrets:

| Name | Value | Repository |
|------|-------|------------|
| `ZAI_API_KEY` | Your Z.ai API key | `Redrock453/strix` |
| `ANTHROPIC_BASE_URL` | `https://api.z.ai/api/anthropic` | `Redrock453/strix` |
| `STRIX_LLM` | `anthropic/claude-sonnet-4-20250514` | `Redrock453/strix` |

4. Restart your Codespace

### Supported Models via Z.ai

#### Anthropic Claude Models
- `anthropic/claude-sonnet-4-20250514` - Claude Sonnet 4 (recommended)
- `anthropic/claude-3-5-sonnet-20241022` - Claude 3.5 Sonnet
- `anthropic/claude-3-opus-20240229` - Claude 3 Opus

#### Other Z.ai Models
- GLM-4.6 and other GLM models
- OpenAI models (via proxy)
- Custom fine-tuned models

## 📡 API Integration Details

### Authentication
Z.ai uses Bearer token authentication:
```bash
Authorization: Bearer YOUR_ZAI_API_KEY
```

Strix automatically handles this when you configure the environment variables.

### Base URLs
- **Anthropic Proxy**: `https://api.z.ai/api/anthropic`
- **Direct Z.ai API**: `https://api.z.ai/api/paas/v4`

### Timeout Configuration
```env
API_TIMEOUT_MS=3000000  # 50 minutes (default)
API_TIMEOUT_MS=5000000  # 83 minutes (for complex scans)
```

## 🐳 CI/CD Integration

### GitHub Actions Workflow
```yaml
name: strix-security-scan

on:
  pull_request:
  push:
    branches: [main, develop]

jobs:
  security-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH
      
      - name: Install Strix
        run: poetry install
      
      - name: Run Security Scan
        env:
          ZAI_API_KEY: ${{ secrets.ZAI_API_KEY }}
          ANTHROPIC_BASE_URL: https://api.z.ai/api/anthropic
          ANTHROPIC_API_KEY: ${{ secrets.ZAI_API_KEY }}
          LLM_API_KEY: ${{ secrets.ZAI_API_KEY }}
          STRIX_LLM: anthropic/claude-sonnet-4-20250514
        run: |
          poetry run strix -n --target ./ \
            --instruction "Focus on critical security vulnerabilities"
      
      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: security-report
          path: agent_runs/*/
```

## 🔒 Security & Privacy

### Z.ai API Security
- **Token Authentication**: Secure API token handling via environment variables
- **HTTPS Communication**: Encrypted communication with Z.ai endpoints
- **Timeout Protection**: Configurable request timeouts to prevent hanging
- **Error Handling**: Comprehensive error management and retry logic

### Sandbox Security
- **Docker Isolation**: All tests run in isolated Docker containers
- **Resource Limits**: CPU and memory limits prevent resource exhaustion
- **Network Control**: Controlled network access from sandbox
- **File System Isolation**: Restricted file system access

### Data Protection
- **No Data Leakage**: Test results stored locally only
- **API Key Protection**: Keys never logged or transmitted insecurely
- **Session Management**: Secure session handling
- **Clean Cleanup**: Automatic cleanup of temporary files

## 📊 Performance Optimization

### Z.ai Specific Optimizations
- **Model Selection**: Optimized for claude-sonnet-4 performance/cost balance
- **Extended Timeouts**: 50-minute timeouts for complex penetration tests
- **Smart Retries**: Automatic retry with exponential backoff
- **Response Streaming**: Efficient streaming for real-time updates

### Scanning Performance
- **Parallel Agents**: Multiple specialized agents work in parallel
- **Smart Caching**: Avoid redundant API calls
- **Progressive Results**: See findings as they're discovered
- **Resource Management**: Efficient CPU and memory usage

## 🚨 Troubleshooting

### Common Issues

#### 1. Z.ai API Connection Failed
```
❌ LLM CONNECTION FAILED
AnthropicException - Authorization Failure
```

**Solutions:**
- Verify `ZAI_API_KEY` is correct in `.env`
- Check `ANTHROPIC_BASE_URL` is `https://api.z.ai/api/anthropic`
- Ensure `LLM_API_KEY` matches your `ZAI_API_KEY`
- Verify API key is active at [Z.ai Dashboard](https://z.ai/manage-apikey/apikey-list)

#### 2. Docker Not Running
```
Error: Docker daemon is not running
```

**Solutions:**
```bash
# Linux
sudo systemctl start docker

# macOS
open -a Docker

# Windows
Start Docker Desktop
```

#### 3. Playwright Browser Issues
```
Exception: Failed to initialize browser
```

**Solutions:**
```bash
# Reinstall browsers
poetry run playwright install chromium

# Install system dependencies
sudo poetry run playwright install-deps
```

#### 4. Timeout Errors
```
Error: Request timeout after 3000000ms
```

**Solution:** Increase timeout:
```bash
export API_TIMEOUT_MS=5000000  # 83 minutes
```

### Debug Mode

Enable verbose logging:
```bash
# Set environment variable
export STRIX_DEBUG=1

# Run with debug output
poetry run strix --target ./app
```

Check logs:
```bash
# View recent scan logs
ls -lrt agent_runs/
cat agent_runs/latest-run/penetration_test_report.md
```

## 📈 Results & Reporting

### Output Structure
```
agent_runs/
└── run-name-123/
    ├── penetration_test_report.md   # Main findings report
    ├── vulnerabilities.csv           # CSV export
    └── vulnerabilities/
        ├── vuln-0001.md             # Detailed vulnerability #1
        ├── vuln-0002.md             # Detailed vulnerability #2
        └── ...
```

### Report Formats

#### Markdown Report
- Executive summary
- Vulnerability details with severity ratings
- Proof-of-concept code
- Remediation recommendations

#### CSV Export
- Structured data for analysis
- Import into spreadsheets or ticketing systems
- Filter and sort by severity

### Viewing Results

```bash
# View main report
cat agent_runs/*/penetration_test_report.md

# View specific vulnerability
cat agent_runs/*/vulnerabilities/vuln-0001.md

# Open in browser (if available)
mdcat agent_runs/*/penetration_test_report.md
```

## 🎯 Advanced Usage

### Custom Vulnerability Focus
```bash
# OWASP Top 10 focused scan
poetry run strix --target https://app.com \
  --instruction "Focus on OWASP Top 10 vulnerabilities: Injection, Broken Authentication, XSS"

# API security testing
poetry run strix --target https://api.example.com \
  --instruction "Test REST API for: IDOR, Mass Assignment, Rate Limiting, JWT vulnerabilities"

# Business logic testing
poetry run strix --target ./app \
  --instruction "Focus on business logic flaws and race conditions"
```

### Integration with Other Tools

#### Burp Suite Integration
```bash
# Export findings and import to Burp
python scripts/convert_to_burp.py agent_runs/latest/
```

#### JIRA Integration
```bash
# Create JIRA tickets from findings
python scripts/export_to_jira.py agent_runs/latest/ --project SEC
```

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone https://github.com/Redrock453/strix.git
cd strix
git checkout zai-integration

# Install development dependencies
poetry install --with dev

# Setup pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest

# Check code quality
make check-all
```

### Available Make Commands
```bash
make help          # Show all commands
make format        # Format code with ruff
make lint          # Lint code
make type-check    # Run type checking
make test          # Run tests
make test-cov      # Run tests with coverage
make check-all     # Run all quality checks
```

### Contribution Guidelines
1. Fork the repository
2. Create feature branch: `git checkout -b feature/zai-enhancement`
3. Make changes and test thoroughly
4. Run quality checks: `make check-all`
5. Commit changes: `git commit -m "Add Z.ai enhancement"`
6. Push to branch: `git push origin feature/zai-enhancement`
7. Create pull request

## 📄 License

Apache License 2.0 - Same as the original Strix project.

See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

### Original Project
- **Strix**: Open-source AI hackers for security testing
- **usestrix**: Original project creators and maintainers
- **Community**: Contributors and security researchers

### Z.ai Integration
- **Z.ai**: API provider for Claude models with 3× usage at 1/7 cost
- **Anthropic**: Claude AI model creators
- **Integration Contributors**: Developers who helped integrate Z.ai

### Special Thanks
- Z.ai team for excellent API documentation and support
- Open-source security community for feedback
- Beta testers for valuable vulnerability reports

## 📞 Support

### Getting Help

1. **Documentation**: 
   - This README
   - [Z.ai Integration Guide](docs/ZAI_INTEGRATION.md)
   - [Original Strix Docs](README.md)

2. **Issues**: 
   - GitHub Issues: [Create Issue](https://github.com/Redrock453/strix/issues)
   - Z.ai API Issues: [Z.ai Support](https://discord.gg/QR7SARHRxK)

3. **Community**:
   - Strix Discord: [Join](https://discord.gg/YjKFvEZSdZ)
   - Z.ai Discord: [Join](https://discord.gg/QR7SARHRxK)

### Issue Reporting

When reporting issues, include:
- **System Info**: OS, Python version, Docker version
- **Configuration**: Sanitized `.env` (remove API keys!)
- **Error Messages**: Full error logs
- **Steps to Reproduce**: Detailed reproduction steps
- **Expected vs Actual**: What should happen vs what happens

## 🎉 Ready to Use!

Your Strix system with Z.ai integration is now ready for security testing!

**Quick Start Checklist:**
- [ ] Z.ai API key configured in `.env` or GitHub Secrets
- [ ] Dependencies installed via Poetry
- [ ] Docker running
- [ ] Playwright browsers installed
- [ ] Test scan working
- [ ] Results directory created

**Next Steps:**
1. Run your first security scan
2. Review the vulnerability reports
3. Customize agent prompts for your testing methodology
4. Set up CI/CD integration
5. Join the community for updates and support

---

## 💰 Cost Optimization with Z.ai

### Why Z.ai?

- **3× More Usage**: Get triple the tokens for your budget
- **1/7 the Cost**: Significantly cheaper than direct Anthropic access
- **Built for Developers**: Optimized for security and coding tasks
- **Same Quality**: Full Claude Sonnet 4 capabilities

### Cost Comparison

| Provider | Cost per 1M Tokens | Effective Rate with Z.ai |
|----------|-------------------|--------------------------|
| Direct Anthropic | $15 | $2.14 (85% savings) |
| OpenAI GPT-4 | $30 | $4.29 (85% savings) |
| Z.ai Proxy | $2.14 | Best value |

### Monitoring Usage

Check your Z.ai usage:
```bash
# View API usage dashboard
open https://z.ai/manage-apikey/usage
```

---

## 📚 Additional Resources

### Documentation
- [Z.ai API Reference](https://docs.z.ai/api-reference/introduction)
- [Z.ai Quick Start](https://docs.z.ai/devpack/quick-start)
- [Strix Main Documentation](README.md)
- [Contributing Guide](CONTRIBUTING.md)

### Tutorials
- [Setting up Z.ai for Strix](docs/ZAI_INTEGRATION.md)
- [Writing Custom Security Tests](docs/CUSTOM_TESTS.md)
- [CI/CD Integration Guide](docs/CICD.md)

### Community
- [Strix GitHub](https://github.com/usestrix/strix)
- [Z.ai GitHub](https://github.com/zai-org)
- [Security Research Blog](https://usestrix.com/blog)

---

**🦉 Powered by Strix + Z.ai**  
**🤖 AI-Driven Security Testing**  
**🔒 Making Applications Secure**

---

**Generated and Maintained with Claude Code via Z.ai**  
**Co-Authored-By: Claude <noreply@anthropic.com>**  
**Z.ai Integration Edition - 2025**
