import logging
import subprocess
import tempfile
from typing import Dict

from src.handlers.directory_handler import DirectoryHandler


class GitHandler:
    """Facilitates cloning of Git repositories and analysis of their contents."""

    @staticmethod
    def clone_and_analyze(repo_url: str) -> Dict[str, Dict[str, int]]:
        """Clones the given Git repository and analyzes its contents.

        Args:
            repo_url (str): URL of the Git repository to clone.

        Returns:
            Dict[str, Dict[str, int]]: The analysis results of the cloned repository's contents.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            try:
                logging.info(f"Cloning repository from {repo_url}...")
                subprocess.check_call(
                    ["git", "clone", repo_url, tmp_dir], stderr=subprocess.STDOUT
                )
                logging.info("Repository cloned successfully. Analyzing contents...")
                directory_handler = DirectoryHandler(directory_path=tmp_dir)
                return directory_handler.analyze_directory()
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to clone repository: {e.output}")
                return {}
            except Exception as e:
                logging.error(f"Error analyzing repository: {e}")
                return {}
