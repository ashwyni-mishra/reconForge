import json
import subprocess
import os
import shutil
from reconforge.scanners.base_scanner import BaseScanner

class WapitiScanner(BaseScanner):
    """
    Wapiti Scanner Integration with auto-installation.
    """

    def __init__(self, target, output_dir="reports"):
        super().__init__(target, output_dir)
        self.tool_name = "wapiti"
        self.output_file = os.path.join(self.output_dir, "wapiti_raw.json")

    def install_tool(self):
        """
        Attempts to install Wapiti via pip.
        """
        cmd = ["pip", "install", "wapiti3"]
        try:
            self.logger.info("Installing Wapiti via 'pip install wapiti3'...")
            subprocess.run(cmd, check=True)
            self.logger.info("Wapiti installation complete.")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install Wapiti: {e}")
            return False

    def run(self):
        """
        Runs Wapiti scanner using subprocess.
        """
        if not self.ensure_dependency(self.tool_name):
            self.logger.error(f"{self.tool_name} is required to continue.")
            return None

        self.logger.info(f"Starting Wapiti scan on target: {self.target}")
        
        cmd = [self.tool_name, "-u", self.target, "-f", "json", "-o", self.output_file]
        
        try:
            self.execute_command(cmd)
            self.logger.info("Wapiti scan completed.")
            return self.parse_results(self.output_file)
        except Exception as e:
            self.logger.error(f"Wapiti scan encountered an issue: {e}")
            return None

    def parse_results(self, raw_output_path):
        """
        Parses Wapiti JSON output.
        """
        vulnerabilities = []
        if not os.path.exists(raw_output_path):
            return vulnerabilities

        try:
            with open(raw_output_path, 'r') as f:
                data = json.load(f)
                vulnerabilities_data = data.get("vulnerabilities", {})
                for category, vulns in vulnerabilities_data.items():
                    for vuln in vulns:
                        severity_map = {0: "info", 1: "low", 2: "medium", 3: "high"}
                        severity = severity_map.get(vuln.get("level", 0), "info")
                        vulnerabilities.append({
                            "scanner": "wapiti",
                            "severity": severity,
                            "issue": category,
                            "description": vuln.get("info", "No description provided.")
                        })
        except Exception as e:
            self.logger.error(f"Error parsing Wapiti results: {e}")

        return vulnerabilities
