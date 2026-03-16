import sys
import os
import time
import subprocess
from rich.console import Console
from rich.prompt import Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from reconforge.cli import parse_arguments
from reconforge.utils.logger import setup_logger
from reconforge.scanners.nuclei_scanner import NucleiScanner
from reconforge.scanners.nikto_scanner import NiktoScanner
from reconforge.scanners.wapiti_scanner import WapitiScanner
from reconforge.scanners.zap_scanner import ZapScanner
from reconforge.scanners.skipfish_scanner import SkipfishScanner
from reconforge.parsers.report_parser import ReportParser

console = Console()

SCANNER_ESTIMATES = {
    "nuclei": 180, "nikto": 300, "wapiti": 420, "zap": 600, "skipfish": 300
}

def auto_update():
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if os.path.exists(os.path.join(base_dir, ".git")):
            subprocess.run(["git", "-C", base_dir, "fetch"], capture_output=True, check=False)
            local_hash = subprocess.run(["git", "-C", base_dir, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
            remote_hash = subprocess.run(["git", "-C", base_dir, "rev-parse", "origin/main"], capture_output=True, text=True).stdout.strip()
            if local_hash != remote_hash:
                console.print("\n[bold yellow][!] A new version of ReconForge is available![/bold yellow]")
                if Confirm.ask("Would you like to update now?"):
                    console.print("[bold blue][*] Updating ReconForge...[/bold blue]")
                    subprocess.run(["git", "-C", base_dir, "reset", "--hard", "origin/main"], capture_output=True, check=False)
                    venv_pip = os.path.join(base_dir, "venv", "bin", "pip")
                    req_file = os.path.join(base_dir, "requirements.txt")
                    if os.path.exists(venv_pip) and os.path.exists(req_file):
                        subprocess.run([venv_pip, "install", "-r", req_file], capture_output=True, check=False)
                    console.print("[bold green][+] Update complete! Restarting...[/bold green]\n")
                    os.execv(sys.argv[0], sys.argv)
    except Exception: pass

def print_banner():
    banner = r"""
    __________                            ___________                      
    \______   \ ____   ____  ____   ____  \_   _____/___________  ____   ____  
     |       _// __ \_/ ___\/  _ \ /    \  |    __) \_  __ \__  \ / ___\_/ __ \ 
     |    |   \  ___/\  \__(  <_> )   |  \ |     \   |  | \// __ \\  \___\  ___/ 
     |____|_  /\___  >\___  >____/|___|  / \___  /   |__|  (____  /\___  >\___  >
            \/     \/     \/           \/      \/               \/     \/     \/ 
    
    [ ReconForge - Comprehensive Web Vulnerability Meta Scanner ]
    [ Developed by: syn9 | https://github.com/ashwyni-mishra    ]
    """
    console.print(banner, style="bold blue")

def main():
    auto_update()
    print_banner()
    args = parse_arguments()
    logger = setup_logger("ReconForge-Main")
    logger.info(f"ReconForge Meta Scanner started for target: {args.target}")

    scanners_mapping = {
        "nuclei": NucleiScanner, "nikto": NiktoScanner, "wapiti": WapitiScanner,
        "zap": ZapScanner, "skipfish": SkipfishScanner
    }

    scanners_to_run = []
    total_est_seconds = 0
    for s_name in args.scanners:
        if s_name in scanners_mapping:
            scanner_instance = scanners_mapping[s_name](args.target, args.output_dir)
            scanner_instance.verbose = not args.silent # Set verbose mode here by default
            scanners_to_run.append(scanner_instance)
            total_est_seconds += SCANNER_ESTIMATES.get(s_name, 300)

    all_results = []
    
    if not args.silent:
        # In verbose mode (default), don't use the Progress bar context for scanners
        for scanner in scanners_to_run:
            scanner_name = scanner.__class__.__name__.replace("Scanner", "")
            console.print(f"[bold yellow][*] Running {scanner_name} Scanner...[/bold yellow]")
            try:
                results = scanner.run()
                if results: all_results.append(results)
            except Exception as e: logger.error(f"Error running {scanner_name}: {e}")
    else:
        # In silent mode, show the clean progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            TextColumn("[blue]({task.fields[est]})"),
            console=console,
        ) as progress:
            overall_task = progress.add_task(
                "[cyan]Scanning...", total=len(scanners_to_run),
                est=f"Est. Total: {total_est_seconds // 60}m"
            )
            for scanner in scanners_to_run:
                scanner_id = scanner.__class__.__name__.replace("Scanner", "").lower()
                scanner_name = scanner.__class__.__name__.replace("Scanner", "")
                est_m = SCANNER_ESTIMATES.get(scanner_id, 300) // 60
                progress.update(overall_task, description=f"[bold yellow]Running {scanner_name}...", est=f"Est: {est_m}m")
                try:
                    results = scanner.run()
                    if results: all_results.append(results)
                except Exception as e: logger.error(f"Error running {scanner_name}: {e}")
                progress.advance(overall_task)

    parser = ReportParser(args.target, args.output_dir)
    parser.aggregate_results(all_results)
    parser.normalize_severities()

    html_report = parser.generate_html_report()
    json_report = parser.generate_json_report()
    
    logger.info(f"Consolidated HTML report generated at: {html_report}")
    logger.info(f"Consolidated JSON report generated at: {json_report}")
    parser.print_cli_summary()

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Interrupted.[/bold red]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
        sys.exit(1)
