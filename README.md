# ReconForge – Web Vulnerability Meta Scanner

ReconForge is a Python-based web vulnerability meta scanner designed to automate Dynamic Application Security Testing (DAST). It orchestrates multiple industry-standard security scanners and aggregates their findings into a single, unified vulnerability report.

Developed by: **syn9** | [GitHub Profile](https://github.com/ashwyni-mishra)

## 1. Project Description
ReconForge simplifies the web security assessment process by providing a centralized interface to run multiple scanners simultaneously. Instead of manually executing different tools and correlating their outputs, security researchers and penetration testers can use ReconForge to gain a comprehensive overview of a target's security posture in one go.

## 2. Features
- **Automated Web Vulnerability Scanning**: Sequential execution of multiple DAST tools with a single command.
- **Integration with Multiple DAST Scanners**: Supports Nuclei, Nikto, Wapiti, OWASP ZAP, and Skipfish.
- **Aggregated Vulnerability Reports**: Combines findings from all scanners into a normalized format.
- **CLI Interface**: Supports short flags (e.g., `-t`, `-s`, `-o`) and a global `reconforge` command.
- **Modular Scanner Architecture**: Flexible design that allows for easy addition of new scanner modules.
- **JSON & CLI Reporting**: Generates detailed JSON reports for automation and clean CLI summaries for quick review.
- **Auto-Installation**: Built-in logic to detect and attempt installation of missing scanner dependencies.

## 3. Quick Install
To install ReconForge and all its dependencies in one step:
```bash
curl -sSL https://raw.githubusercontent.com/ashwyni-mishra/reconForge/main/setup.sh | bash
```

## 4. Documentation
For detailed information on how to install and use ReconForge, please refer to the following guides:

- [**Installation Guide**](INSTALLATION.md) – Step-by-step setup instructions.
- [**Commands Guide**](COMMANDS.md) – Detailed list of CLI options and example usage.

## 5. Disclaimer
This tool is for **educational and ethical security testing only**. Do not use ReconForge against targets you do not have explicit, written permission to test. The developers are not responsible for any misuse or damage caused by this tool.

---
© 2026 ReconForge Project | Developed by [syn9](https://github.com/ashwyni-mishra)
