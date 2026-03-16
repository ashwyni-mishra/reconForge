# Installation Guide

ReconForge is designed to be easily set up on Debian-based systems (like Kali Linux), but it can be manually configured for other operating systems.

## One-Line Installation (Recommended)
You can install ReconForge, its dependencies, and configure the global command with a single `curl` one-liner:
```bash
curl -sSL https://raw.githubusercontent.com/ashwyni-mishra/reconForge/main/setup.sh | bash
```

## Manual Setup
If you prefer a manual setup, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/ashwyni-mishra/reconForge.git
cd ReconForge
```

### 2. Run the Setup Script
The script will install system tools, set up a virtual environment, and configure the global `reconforge` command:
```bash
chmod +x setup.sh
./setup.sh
```

### 3. Verification
Verify the installation by running:
```bash
reconforge --help
```
