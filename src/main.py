import argparse
import logging
import os

from src.common.config import Config
from src.common.file_analyzer import analyze_file
from src.common.logging import setup_logging
from src.common.metrics import Metric
from src.common.report_generation import generate_report
from src.handlers.directory_handler import DirectoryHandler
from src.handlers.git_handler import GitHandler

# Get environment variables
config = Config()

LOG_LEVEL = config.log_level
REPORT_TEMPLATE_PATH = config.report_template_path


def _calculate_summary_totals(results):
    """Calculates summary totals from the analysis results.

    Args:
        results (dict): The analysis results.

    Returns:
        dict: A dictionary with summary totals for code, comments, blanks, and total lines.
    """
    summary_totals = {metric: 0 for metric in Metric}
    for metrics in results.values():
        for key in summary_totals.keys():
            summary_totals[key] += metrics.get(key, 0)
    return summary_totals


def _print_summary_to_console(data, summary_totals):
    """Prints the individual results and a summary to the console."""
    print("\nLines of Code Counter Report\n============================")
    for file_path, metrics in data.items():
        print(f"File: {file_path}")
        for metric, value in metrics.items():
            print(f"    {metric.label}: {value}")

    # Display a summary of the results
    print("\nSummary of Totals Across All Files\n===================================")
    for metric, total in summary_totals.items():
        print(f"    {metric.label}: {total}")


def main():
    parser = argparse.ArgumentParser(description="Lines of Code Counter Tool")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--directory", type=str, help="Path to the directory to analyze."
    )
    group.add_argument("--file", type=str, help="Path to a single file to analyze.")
    group.add_argument("--git", type=str, help="URL of the git repository to analyze.")
    parser.add_argument(
        "--report",
        type=str,
        help="Path to save the summary report. If not specified, results will be printed to the console.",
    )
    parser.add_argument(
        "--log",
        type=str,
        help="Path to save the log file. If not specified, logs will be printed to the console.",
    )

    args = parser.parse_args()

    # Set up logging
    setup_logging(log_file=args.log)
    try:
        results = None
        if args.directory:
            logging.info(f"Analyzing directory: {args.directory}")
            handler = DirectoryHandler(directory_path=args.directory)
            results = handler.analyze_directory()
        elif args.file:
            logging.info(f"Analyzing file: {args.file}")
            results = {args.file: analyze_file(args.file)}
        elif args.git:
            logging.info(f"Cloning and analyzing Git repository: {args.git}")
            results = GitHandler.clone_and_analyze(repo_url=args.git)
    except Exception as e:
        logging.error(f"Unable to generate the result: {e}")
        raise e

    # Calculate summary totals from the results
    summary_totals = _calculate_summary_totals(results)

    if args.report:
        logging.info(f"Generating report at: {args.report}")
        # Determine the root path of the project dynamically
        project_root = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(project_root, REPORT_TEMPLATE_PATH)
        generate_report(
            data=results, template_path=template_path, output_path=args.report
        )
    else:
        _print_summary_to_console(results, summary_totals)


if __name__ == "__main__":
    main()
