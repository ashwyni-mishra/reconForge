import json
import os
from datetime import datetime
from jinja2 import Template
from reconforge.utils.html_template import HTML_TEMPLATE

class ReportParser:
    """
    Parser module to collect, normalize and aggregate scanner results.
    """

    def __init__(self, target, output_dir="reports"):
        self.target = target
        self.output_dir = output_dir
        self.all_vulnerabilities = []
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def aggregate_results(self, scan_results):
        if not scan_results:
            return []
        for results in scan_results:
            if results:
                self.all_vulnerabilities.extend(results)
        return self.all_vulnerabilities

    def normalize_severities(self):
        severity_mapping = {
            "critical": "high", "high": "high", "medium": "medium",
            "low": "low", "info": "info", "unknown": "info"
        }
        for vuln in self.all_vulnerabilities:
            current_severity = vuln.get("severity", "info").lower()
            vuln["severity"] = severity_mapping.get(current_severity, "info")

    def generate_json_report(self):
        report_path = os.path.join(self.output_dir, f"reconforge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        report_data = {
            "target": self.target,
            "timestamp": datetime.now().isoformat(),
            "vulnerabilities": self.all_vulnerabilities
        }
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=4)
        return report_path

    def generate_html_report(self):
        """
        Generates a modern HTML report using Jinja2.
        """
        report_path = os.path.join(self.output_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        
        counts = {"high": 0, "medium": 0, "low": 0, "info": 0}
        for v in self.all_vulnerabilities:
            counts[v["severity"]] += 1

        template = Template(HTML_TEMPLATE)
        html_content = template.render(
            target=self.target,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            counts=counts,
            vulnerabilities=self.all_vulnerabilities
        )

        with open(report_path, 'w') as f:
            f.write(html_content)
        
        return report_path

    def print_cli_summary(self):
        severity_counts = {"high": 0, "medium": 0, "low": 0, "info": 0}
        for vuln in self.all_vulnerabilities:
            sev = vuln.get("severity", "info")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        print("\n" + "="*50)
        print(f"RECONFORGE SCAN SUMMARY: {self.target}")
        print("="*50)
        print(f"High:    {severity_counts['high']}")
        print(f"Medium:  {severity_counts['medium']}")
        print(f"Low:     {severity_counts['low']}")
        print(f"Info:    {severity_counts['info']}")
        print("-" * 50)
        print(f"Total findings: {len(self.all_vulnerabilities)}")
        print("="*50 + "\n")
