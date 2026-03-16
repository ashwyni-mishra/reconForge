import time
import os
from zapv2 import ZAPv2
from reconforge.scanners.base_scanner import BaseScanner

class ZapScanner(BaseScanner):
    """
    OWASP ZAP Scanner Integration.
    """

    def __init__(self, target, output_dir="reports"):
        super().__init__(target, output_dir)
        self.tool_name = "zaproxy"
        self.output_file = os.path.join(self.output_dir, "zap_raw.json")
        self.zap = ZAPv2()

    def install_tool(self):
        """
        Instructions for ZAP installation.
        """
        self.logger.info("For ZAP auto-install, use: 'sudo apt install zaproxy' on Kali Linux.")
        return False

    def run(self):
        """
        Runs ZAP scan using the API.
        """
        self.logger.info(f"Starting ZAP scan on target: {self.target}")
        
        try:
            # Open URL
            self.zap.urlopen(self.target)
            
            # Active Scan
            scan_id = self.zap.ascan.scan(self.target)
            while int(self.zap.ascan.status(scan_id)) < 100:
                time.sleep(5)
            
            self.logger.info("ZAP scan completed.")
            return self.parse_results(None)
        except Exception as e:
            self.logger.error(f"ZAP scan failed: {e}")
            return None

    def parse_results(self, _):
        """
        Parses ZAP results from the API.
        """
        vulnerabilities = []
        try:
            alerts = self.zap.core.alerts(baseurl=self.target)
            for alert in alerts:
                vulnerabilities.append({
                    "scanner": "zap",
                    "severity": alert.get("risk", "info").lower(),
                    "issue": alert.get("alert", "unknown"),
                    "description": alert.get("description", "No description provided.")
                })
        except Exception as e:
            self.logger.error(f"Error parsing ZAP results: {e}")

        return vulnerabilities
