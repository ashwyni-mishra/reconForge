#!/bin/bash

# ReconForge Automated Setup Script
# Developed by: syn9

REPO_URL="https://github.com/ashwyni-mishra/reconForge.git"
INSTALL_DIR="/opt/reconforge"

echo "================================================="
echo "       ReconForge - Installation Script          "
echo "================================================="

echo "[*] Updating system packages..."
sudo apt-get update -y

echo "[*] Installing required system dependencies..."
sudo apt-get install -y python3 python3-pip python3-setuptools python3-venv git
sudo apt-get install -y zaproxy wapiti skipfish nikto nuclei golang perl man-db

# 1. Setup Installation Directory in /opt
if [ ! -d "$INSTALL_DIR" ]; then
    echo "[*] Installing ReconForge to $INSTALL_DIR..."
    sudo git clone "$REPO_URL" "$INSTALL_DIR"
else
    echo "[*] ReconForge already exists in $INSTALL_DIR. Updating..."
    cd "$INSTALL_DIR" && sudo git pull origin main
fi

cd "$INSTALL_DIR" || exit

echo "[*] Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    sudo python3 -m venv venv
fi

echo "[*] Installing Python dependencies..."
sudo ./venv/bin/pip install --upgrade pip
sudo ./venv/bin/pip install -r requirements.txt

echo "[*] Configuring global 'reconforge' command..."
sudo chmod +x reconforge_cli

# Create a permanent symlink in /usr/local/bin (standard PATH)
sudo ln -sf "$INSTALL_DIR/reconforge_cli" /usr/local/bin/reconforge

echo "[*] Installing 'reconforge' manual page..."
sudo mkdir -p /usr/local/share/man/man1
sudo cp reconforge.1 /usr/local/share/man/man1/
sudo mandb > /dev/null 2>&1

echo "================================================="
echo "[+] Setup complete!"
echo "[+] ReconForge is now installed in $INSTALL_DIR"
echo "[+] You can now run the tool globally using:"
echo "    reconforge -t https://example.com"
echo "[+] To view the manual page, use:"
echo "    man reconforge"
echo "================================================="
