# Lines of Code Counter Tool

## Overview
The Lines of Code Counter is a Python tool designed to analyze source code files, counting lines of code, comments, and blank lines. It supports Python and Java out of the box, with the ability to easily extend support to more languages.

## Setup
1. **Clone the repository:**
```
git clone https://github.com/yourusername/lines_of_code_counter.git
```
2. **Navigate to the project directory:**
```
cd lines_of_code_counter
```
3. **Install dependencies:**
```
pip install -r requirements.txt
```


## Usage

### Basic Usage
To analyze all supported files in a directory and print the results:
```
PYTHONPATH=$(pwd) python src/main.py --directory /path/to/source/code
```
### Generating a Report
To generate a detailed report file:
```
PYTHONPATH=$(pwd) python src/main.py --directory /path/to/source/code --report /path/to/report.txt
```
### Logging
To save log output to a file:
```
PYTHONPATH=$(pwd) python src/main.py --directory /path/to/source/code --log /path/to/logfile.log
```


## Dev Usage

### Tests
To run tests locally (prefer containers):
```
PYTHONPATH=$(pwd) pytest tests
```


 ### Code Cleanup
To clean the code with flask8 isort black mypy
```
PYTHONPATH=$(pwd) python dev/clean_code.py
```