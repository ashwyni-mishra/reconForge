import subprocess
import os
import shutil
from reconforge.scanners.base_scanner import BaseScanner

class SkipfishScanner(BaseScanner):
    """
    Skipfish Scanner Integration.
    """

    def __init__(self, target, output_dir="reports"):
        super().__init__(target, output_dir)
        self.tool_name = "skipfish"
        self.output_file = os.path.join(self.output_dir, "skipfish_report")

    def install_tool(self):
        self.logger.info("For Skipfish auto-install, use: 'sudo apt install skipfish' on Kali Linux.")
        return False

    def run(self):
        if not self.ensure_dependency(self.tool_name):
            return None

        self.logger.info(f"Starting Skipfish scan on target: {self.target}")
        
        if os.path.exists(self.output_file):
            shutil.rmtree(self.output_file)
            
        # -L (ignore learning), -S (skip brute forcing), -u (be quiet)
        # Note: Skipfish is highly interactive, which is difficult for a silent meta-scanner.
        # We try to run it as non-interactively as possible.
        cmd = [self.tool_name, "-o", self.output_file, "-S", "dictionaries/complete.wl", self.target]
        
        try:
            self.execute_command(cmd)
            self.logger.info("Skipfish scan completed.")
            return self.parse_results(self.output_file)
        except Exception as e:
            self.logger.error(f"Skipfish scan encountered an issue: {e}")
            return None

    def parse_results(self, raw_output_path):
        vulnerabilities = []
        # Skipfish report parsing logic here (usually requires parsing index.html or samples.js)
        return vulnerabilities
