from src.common.metrics import Metric

from .base_counter import AnalysisResult, BaseCounter


class PythonCounter(BaseCounter):
    """Distinguishes between various species of code and comments."""

    def __init__(self, file_path: str):
        super().__init__(file_path)

    def count_lines(self) -> AnalysisResult:
        result = AnalysisResult()
        in_multiline_comment = False

        with open(self.file_path, "r") as file:
            for line in file:
                stripped_line = line.strip()

                result.add_metric(Metric.TOTAL, 1)

                if (
                    stripped_line.startswith('"""') or stripped_line.startswith("'''")
                ) or (stripped_line.endswith('"""') or stripped_line.endswith("'''")):
                    if not in_multiline_comment:
                        in_multiline_comment = True
                        continue
                    else:
                        result.add_metric(Metric.MULTI_LINE_COMMENTS, 1)
                        in_multiline_comment = False
                        continue

                if in_multiline_comment:
                    # to count the lines of multiline comments
                    # result.add_metric(Metric.MULTI_LINE_COMMENTS, 1)
                    continue
                else:
                    if stripped_line.startswith("#"):
                        result.add_metric(Metric.SINGLE_LINE_COMMENTS, 1)
                    elif stripped_line == "":
                        result.add_metric(Metric.BLANK_LINES, 1)
                    else:
                        result.add_metric(Metric.CODE_LINES, 1)
                        if "#" in stripped_line:
                            result.add_metric(Metric.CODE_LINE_COMMENTS, 1)

        return result
