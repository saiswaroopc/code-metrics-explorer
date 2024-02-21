from enum import Enum, auto


class Metric(Enum):
    CODE_LINES = (auto(), "Code Lines")
    SINGLE_LINE_COMMENTS = (auto(), "Single Line Comments")
    MULTI_LINE_COMMENTS = (auto(), "Multi-Line Comments")
    CODE_LINE_COMMENTS = (auto(), "Code and Comments")
    BLANK_LINES = (auto(), "Blank Lines")
    TOTAL = (auto(), "Total")

    def __init__(self, _, label):
        self._label = label

    @property
    def label(self):
        return self._label
