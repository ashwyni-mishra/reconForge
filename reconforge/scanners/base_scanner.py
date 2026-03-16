import subprocess
import os
import shutil
import sys
from abc import ABC, abstractmethod
from reconforge.utils.logger import setup_logger

class BaseScanner(ABC):
    """
    Abstract Base Class for vulnerability scanners.
    """

    def __init__(self, target, output_dir="reports"):
        self.target = target
        self.output_dir = output_dir
        self.logger = setup_logger(self.__class__.__name__)
        self.verbose = False  # To be set by core.py
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def parse_results(self, raw_output_path):
        pass

    @abstractmethod
    def install_tool(self):
        pass

    def check_tool_installed(self, tool_name):
        path = shutil.which(tool_name)
        return bool(path)

    def ensure_dependency(self, tool_name):
        if self.check_tool_installed(tool_name):
            return True
        self.logger.info(f"Attempting to auto-install {tool_name}...")
        return self.install_tool()

    def execute_command(self, cmd, check=False):
        """
        Executes a command. If verbose, shows output; otherwise captures it.
        """
        try:
            if self.verbose:
                # In verbose mode, pipe output to terminal while still allowing capture if needed
                result = subprocess.run(cmd, check=check)
                return result
            else:
                # In silent mode, capture everything
                result = subprocess.run(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True, 
                    check=check
                )
                return result
        except Exception as e:
            self.logger.error(f"Error executing command: {e}")
            return None
