import json
import subprocess
import os
import shutil
from reconforge.scanners.base_scanner import BaseScanner

class NiktoScanner(BaseScanner):
    """
    Nikto Scanner Integration with auto-installation.
    """

    def __init__(self, target, output_dir="reports"):
        super().__init__(target, output_dir)
        self.tool_name = "nikto"
        self.output_file = os.path.join(self.output_dir, "nikto_raw.json")

    def install_tool(self):
        """
        Attempts to install Nikto via Git clone. Requires Perl and Git.
        """
        if not shutil.which("git"):
            self.logger.error("Git is required to install Nikto.")
            return False
            
        target_dir = os.path.join(os.getcwd(), "tools", "nikto")
        if not os.path.exists("tools"):
            os.makedirs("tools")

        cmd = ["git", "clone", "https://github.com/sullo/nikto.git", target_dir]
        try:
            self.logger.info(f"Cloning Nikto to {target_dir}...")
            subprocess.run(cmd, check=True)
            self.logger.info("Nikto installation complete.")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install Nikto: {e}")
            return False

    def check_tool_installed(self, tool_name):
        """
        Check for nikto in PATH or in our local tools directory.
        """
        if shutil.which(tool_name):
            self.tool_executable = tool_name
            return True
            
        local_path = os.path.join(os.getcwd(), "tools", "nikto", "program", "nikto.pl")
        if os.path.exists(local_path):
            self.tool_executable = local_path
            return True
            
        return False

    def run(self):
        """
        Runs Nikto scanner using subprocess.
        """
        if not self.ensure_dependency("nikto"):
            self.logger.error("Nikto is required to continue.")
            return None

        self.logger.info(f"Starting Nikto scan on target: {self.target}")
        
        # Decide how to run nikto
        if self.tool_executable.endswith(".pl"):
            cmd = ["perl", self.tool_executable, "-h", self.target, "-Format", "json", "-o", self.output_file]
        else:
            cmd = [self.tool_executable, "-h", self.target, "-Format", "json", "-o", self.output_file]
        
        try:
            self.execute_command(cmd)
            self.logger.info("Nikto scan completed.")
            return self.parse_results(self.output_file)
        except Exception as e:
            self.logger.error(f"Nikto scan encountered an issue: {e}")
            return None

    def parse_results(self, raw_output_path):
        """
        Parses Nikto JSON output.
        """
        vulnerabilities = []
        if not os.path.exists(raw_output_path):
            return vulnerabilities

        try:
            with open(raw_output_path, 'r') as f:
                data = json.load(f)
                vulnerabilities_data = data.get("vulnerabilities", [])
                for vuln in vulnerabilities_data:
                    vulnerabilities.append({
                        "scanner": "nikto",
                        "severity": "info", 
                        "issue": vuln.get("msg", "Unknown Nikto issue"),
                        "description": vuln.get("msg", "No description provided.")
                    })
        except Exception as e:
            self.logger.error(f"Error parsing Nikto results: {e}")

        return vulnerabilities
