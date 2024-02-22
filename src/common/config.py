import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        """Initializes the configuration by loading environment variables."""
        load_dotenv()

    @property
    def log_level(self) -> str:
        """Retrieves the logging level from environment variables."""
        return os.getenv("LOG_LEVEL", "INFO")

    @property
    def report_template_path(self) -> str:
        """Retrieves the report template path from environment variables."""
        return os.getenv(
            "REPORT_TEMPLATE_PATH",
            "src/templates/report_template.txt",
            # Assuming the template path is fixed and part of project structure
        )

    @property
    def app_name(self) -> str:
        """Retrieves the application name from environment variables."""
        return os.getenv("APP", "CodeAnalysisTool")

    def get(key: str, default=None):
        """Retrieves the value of an environment variable or returns a default."""
        return os.getenv(key, default)
