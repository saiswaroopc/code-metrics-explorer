from abc import ABC, abstractmethod
from typing import Dict

from src.common.metrics import Metric


class AnalysisResult:
    """Encapsulates the results of a code analysis."""

    def __init__(self):
        self.metrics: Dict[Metric, int] = {metric: 0 for metric in Metric}

    def add_metric(self, metric_name: Metric, value: int) -> None:
        """Safely adds to an existing count of a measure for sum."""
        if metric_name in self.metrics:
            self.metrics[metric_name] += value
            # self.metrics["Total"] += value
            if not isinstance(value, int):
                raise TypeError(
                    f"Value for {metric_name} must be an int, got {type(value).__name__}"
                )
        else:
            raise ValueError(f"Metric {metric_name} not found in the report scheme.")


class BaseCounter(ABC):
    """Abstract base class for counters of different programming languages."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def count_lines(self) -> AnalysisResult:
        """Counts lines in a file, differentiating between code, comments, and blanks."""
        pass
