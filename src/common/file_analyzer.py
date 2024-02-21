import logging

from src.counter.java_counter import JavaCounter
from src.counter.python_counter import PythonCounter


def analyze_file(file_path: str):
    try:
        if file_path.endswith(".py"):
            logging.info(f"python file : {file_path}; processing..")
            counter = PythonCounter(file_path)
        elif file_path.endswith(".java"):
            logging.info(f"java file : {file_path}; processing..")
            counter = JavaCounter(file_path)
        else:
            logging.warning(f"Unsupported file type: {file_path}; Skipping..")
            return
        return counter.count_lines().metrics
    except FileNotFoundError:
        logging.error(
            f"File not found: {file_path}. Please check the path and try again."
        )
        raise FileNotFoundError
