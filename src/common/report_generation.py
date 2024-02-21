import logging
import os
import traceback
from typing import Dict

from jinja2 import Environment, FileSystemLoader

from src.common.metrics import Metric


def _accumulate_summary_totals(data):
    """Accumulates summary totals from the metrics of multiple files."""
    summary_totals = {metric: 0 for metric in Metric}
    for metrics in data.values():
        for metric, value in metrics.items():
            summary_totals[metric] += value
    return summary_totals


def generate_report(
    data: Dict[str, Dict[str, int]], template_path: str, output_path: str
):
    """Generates a report from the analysis data using a Jinja2 template.

    Args:
    data (Dict[str, Dict[str, int]]): The analysis results.
    template_path (str): Path to the Jinja2 template file.
    output_path (str): Path where the report should be saved.
    """
    try:

        # Setup Jinja2 environment
        env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
        template = env.get_template(os.path.basename(template_path))

        # Convert Enum members to their names for template keys
        processed_data = {
            fp: {metric.name: val for metric, val in metrics.items()}
            for fp, metrics in data.items()
        }
        summary_totals = _accumulate_summary_totals(data)
        processed_summary_totals = {
            metric.name: value for metric, value in summary_totals.items()
        }

        # Render and write the report
        rendered_content = template.render(
            data=processed_data, summary_totals=processed_summary_totals, Metric=Metric
        )
        with open(output_path, "w") as f:
            f.write(rendered_content)

        logging.info(f"Report successfully generated at {output_path}")
    except FileNotFoundError:
        logging.error(
            f"Template file not found at {template_path}. Please check the path and try again."
        )
    except Exception as e:
        traceback.print_exc()
        logging.error(f"Failed to generate report: {e}")
