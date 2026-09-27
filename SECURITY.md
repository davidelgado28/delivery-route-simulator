# Security Policy

## Supported Versions

The following versions of the Statistical Delivery Route Optimizer are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

---

## Reporting a Vulnerability

We take the security of this application seriously. If you discover a security vulnerability, please follow these guidelines:

1. **Do NOT open a public GitHub issue** for security-related bugs.
2. Email your findings directly to the repository maintainer at `your-email@example.com`.
3. Provide detailed steps to reproduce the issue, including:
   - Operating system and Python version.
   - Input payloads or commands that caused unexpected behavior.
   - Potential impact of the vulnerability.

### Response Timeline
- **Initial Response**: Within 48 hours.
- **Status Update / Triage**: Within 5 business days.
- **Fix / Disclosure**: Fixes will be committed directly to `main` upon verification.

---

## Local Security Practices & Data Privacy

- **Local Storage**: All historical data is stored locally in an `SQLite` database (`delivery_history.db`). No telemetry or personal data is transmitted to external servers.
- **SQL Injection Prevention**: Database operations utilize parameterized queries through standard Python `sqlite3` driver bindings.
- **Dependencies**: Keep your local environment secure by regularly updating dependencies via `pip`:
  ```bash
  pip list --outdated
