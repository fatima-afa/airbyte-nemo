import datetime
from typing import Optional


class MetricCalculator:

    # Calculate Time To Merge Metric
    @staticmethod
    def calculate_ttm(pr_open_at: str, pr_merged_at: str) -> Optional[int]:
        if not pr_open_at or not pr_merged_at:
            return None

        format_str = '%Y-%m-%dT%H:%M:%SZ'
        try:
            datetime_obj1 = datetime.datetime.strptime(pr_open_at, format_str)
            datetime_obj2 = datetime.datetime.strptime(pr_merged_at, format_str)
        except ValueError as e:
            return None

        # Calculate the difference
        time_diff = datetime_obj2 - datetime_obj1

        return int(time_diff.total_seconds())

