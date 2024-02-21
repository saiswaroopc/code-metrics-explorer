import logging
import os
from typing import Dict

from src.common.file_analyzer import analyze_file


class DirectoryHandler:
    """Handles recursive analysis of directories for supported file types."""

    def __init__(self, directory_path: str):
        self.directory_path = directory_path

    def analyze_directory(self) -> Dict[str, Dict[str, int]]:
        """Recursively analyzes all supported files in the specified directory.

        Returns:
                Dict[str, Dict[str, int]]: A dictionary containing analysis results, keyed by file paths.
        """
        results = {}
        for root, _, files in os.walk(self.directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                analysis_result = analyze_file(file_path)
                if analysis_result:
                    results[file_path] = analysis_result

        return results
