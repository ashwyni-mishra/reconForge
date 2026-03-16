# ReconForge Commands Guide

ReconForge provides a flexible Command Line Interface (CLI) to automate and customize your web security scans.

## Command Syntax
```bash
reconforge [options]
```

## Available Options

| Short Flag | Long Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| `-t` | `--target` | **Required.** The target URL to scan. | - |
| `-S` | `--scanners` | List of scanners to run (nuclei, nikto, wapiti, zap, skipfish). | all |
| `-o` | `--output-dir` | Directory to save scan reports. | `reports/` |
| `-si` | `--silent` | Hide scanner output and show progress bar instead. | - |
| `-h` | `--help` | Display the help message and exit. | - |

## Example Usage

### 1. Basic Scan (Verbose by Default)
Run all available scanners against a target, showing detailed output:
```bash
reconforge -t https://example.com
```

### 2. Silent Scan with Progress Bar
Run a scan cleanly, using the dynamic progress bar:
```bash
reconforge -t https://example.com -si
```

### 3. Specific Scanners
Run only Nuclei and ZAP against a target:
```bash
reconforge -t https://example.com -S nuclei zap
```

### 3. Custom Output Directory
Specify where to save the consolidated JSON reports:
```bash
reconforge -t https://example.com -o my_security_scans/
```

### 4. Detailed Help
For a full list of commands and options:
```bash
reconforge --help
```
