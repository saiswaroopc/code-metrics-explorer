import pytest

from src.common.metrics import Metric
from src.counter.python_counter import PythonCounter


@pytest.fixture
def python_file(tmp_path):
    def _create_python_file(content: str):
        file_path = tmp_path / "test_file.py"
        file_path.write_text(content)
        return file_path

    return _create_python_file


# Test for counting single-line comments in Python
def test_python_counter_single_line_comments(python_file):
    content = """
# This is a single line comment
def foo():
    pass  # Inline comment
"""
    file_path = python_file(content)
    counter = PythonCounter(str(file_path))
    result = counter.count_lines()
    assert result.metrics[Metric.SINGLE_LINE_COMMENTS] == 1
    assert result.metrics[Metric.CODE_LINE_COMMENTS] == 1


# Test for handling multiline strings used as block comments in Python
def test_python_counter_multiline_string_as_comment(python_file):
    content = '''
"""
This is a multiline string used as a block comment
"""
def foo():
    pass
'''
    file_path = python_file(content)
    counter = PythonCounter(str(file_path))
    result = counter.count_lines()
    assert result.metrics[Metric.MULTI_LINE_COMMENTS] == 1


# Test for mixed content in Python files
def test_python_counter_mixed_content(python_file):
    content = """
# A comment line
def foo():
    print("Hello")  # Inline comment
    '''
    Multiline
    string
    content
    '''
# Another comment
"""
    file_path = python_file(content)
    counter = PythonCounter(str(file_path))
    result = counter.count_lines()
    assert result.metrics[Metric.SINGLE_LINE_COMMENTS] == 2
    assert result.metrics[Metric.CODE_LINE_COMMENTS] == 1
    assert result.metrics[Metric.MULTI_LINE_COMMENTS] == 1
    assert (
        result.metrics[Metric.CODE_LINES] == 2
    )  # Adjust based on how multiline strings are counted


# Test for handling shebang and encoding in Python files
def test_python_counter_shebang_and_encoding(python_file):
    content = "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\ndef foo():\n    pass"
    file_path = python_file(content)
    counter = PythonCounter(str(file_path))
    result = counter.count_lines()
    assert result.metrics[Metric.CODE_LINES] == 2
    assert result.metrics[Metric.SINGLE_LINE_COMMENTS] == 2
