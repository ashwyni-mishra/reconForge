import argparse

def parse_arguments():
    """
    Handles Command Line Arguments for ReconForge.
    """
    parser = argparse.ArgumentParser(description="ReconForge - Comprehensive Web Vulnerability Meta Scanner")
    
    parser.add_argument("-t", "--target", required=True, help="Target URL to scan (e.g., https://example.com)")
    parser.add_argument("-o", "--output-dir", default="reports", help="Directory to save scan results (default: reports)")
    parser.add_argument("-S", "--scanners", nargs="+", 
                        choices=["nuclei", "nikto", "wapiti", "zap", "skipfish"], 
                        default=["nuclei", "nikto", "wapiti", "zap", "skipfish"], 
                        help="List of scanners to run (default: all)")
    
    parser.add_argument("-si", "--silent", action="store_true", help="Hide scanner output and show progress bar instead")
    return parser.parse_args()
