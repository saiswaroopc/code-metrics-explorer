import tempfile
from pathlib import Path

import pytest

from src.common.metrics import Metric
from src.counter.java_counter import JavaCounter


@pytest.fixture
def java_file(tmp_path):
    def _create_java_file(content: str):
        file_path = tmp_path / "test_file.java"
        file_path.write_text(content)
        return file_path

    return _create_java_file


# Test for counting single-line comments in Java
def test_java_counter_single_line_comments(java_file):
    content = """
// This is a single line comment
public class HelloWorld {
    public static void main(String[] args) {
        // This is an inline comment
        System.out.println("Hello, world!");
    }
}
"""
    file_path = java_file(content)
    counter = JavaCounter(str(file_path))
    result = counter.count_lines()
    assert result.metrics[Metric.SINGLE_LINE_COMMENTS] == 2


# Test for counting multi-line comments in Java
def test_java_counter_multi_line_comments(java_file):
    content = """
/* This is a multi-line
   comment */
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
}
"""
    file_path = java_file(content)
    counter = JavaCounter(str(file_path))
    result = counter.count_lines()
    assert result.metrics[Metric.MULTI_LINE_COMMENTS] == 1


# Test for inline comments mixed with code in Java
def test_java_counter_inline_comments(java_file):
    content = """
public class HelloWorld {
    public static void main(String[] args) { // Main method start
        System.out.println("Hello, world!"); // Print statement
    }
}
"""
    file_path = java_file(content)
    counter = JavaCounter(str(file_path))
    result = counter.count_lines()
    assert result.metrics[Metric.SINGLE_LINE_COMMENTS] == 0
    assert result.metrics[Metric.CODE_LINE_COMMENTS] == 2


# Test for handling block comments (multi-line) and inline comments together in Java
def test_java_counter_block_and_inline_comments(java_file):
    content = """
/* Block comment about the class */
public class HelloWorld { // Class start
    /* Main method description */
    public static void main(String[] args) {
        System.out.println("Hello, world!"); // Print hello
    }
    // End of class
}
"""
    file_path = java_file(content)
    counter = JavaCounter(str(file_path))
    result = counter.count_lines()
    assert result.metrics[Metric.MULTI_LINE_COMMENTS] == 2
    assert result.metrics[Metric.SINGLE_LINE_COMMENTS] == 1
    assert result.metrics[Metric.CODE_LINE_COMMENTS] == 2
