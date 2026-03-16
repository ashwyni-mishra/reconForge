import json
import subprocess
import os
import shutil
from reconforge.scanners.base_scanner import BaseScanner

class NucleiScanner(BaseScanner):
    """
    Nuclei Scanner Integration with auto-installation.
    """

    def __init__(self, target, output_dir="reports"):
        super().__init__(target, output_dir)
        self.tool_name = "nuclei"
        self.output_file = os.path.join(self.output_dir, "nuclei_raw.json")

    def install_tool(self):
        """
        Installs Nuclei using 'go install'. Requires Go.
        """
        if not shutil.which("go"):
            self.logger.error("Go is required for auto-installing Nuclei. Please install Go (https://golang.org/doc/install).")
            return False
            
        cmd = ["go", "install", "-v", "github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest"]
        try:
            self.logger.info("Installing Nuclei via 'go install'...")
            subprocess.run(cmd, check=True)
            self.logger.info("Nuclei installation complete.")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install Nuclei: {e}")
            return False

    def run(self):
        """
        Runs Nuclei scanner using subprocess.
        """
        if not self.ensure_dependency(self.tool_name):
            self.logger.error(f"{self.tool_name} is required to continue.")
            return None

        self.logger.info(f"Starting Nuclei scan on target: {self.target}")
        
        cmd = [self.tool_name, "-u", self.target, "-j", "-o", self.output_file]
        
        try:
            self.execute_command(cmd)
            self.logger.info("Nuclei scan completed.")
            return self.parse_results(self.output_file)
        except Exception as e:
            self.logger.error(f"Nuclei scan encountered an issue: {e}")
            return None

    def parse_results(self, raw_output_path):
        """
        Parses Nuclei JSON output.
        """
        vulnerabilities = []
        if not os.path.exists(raw_output_path):
            return vulnerabilities

        try:
            with open(raw_output_path, 'r') as f:
                for line in f:
                    if not line.strip(): continue
                    data = json.loads(line)
                    vulnerabilities.append({
                        "scanner": "nuclei",
                        "severity": data.get("info", {}).get("severity", "unknown").lower(),
                        "issue": data.get("info", {}).get("name", "unknown"),
                        "description": data.get("info", {}).get("description", "No description provided.")
                    })
        except Exception as e:
            self.logger.error(f"Error parsing Nuclei results: {e}")

        return vulnerabilities
