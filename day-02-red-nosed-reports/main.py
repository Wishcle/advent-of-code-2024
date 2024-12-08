
from typing import List, Optional


def get_input_lines() -> List[str]:
    with open("input.txt", "r") as f:
        return f.readlines()


def get_reports() -> List[List[int]]:
    lines = get_input_lines()
    reports = []
    for line in lines:
        report = [int(n) for n in line.split()]
        reports.append(report)
    return reports


def _is_report_safe_return_index(report: List[str]) -> Optional[int]:
    if len(report) <= 1:
        return True

    # Reverse if decreasing to simplify.
    if report[0] > report[-1]:
        report = list(report)
        report.reverse()

    for i in range(len(report) - 1):
        increase = report[i+1] - report[i]
        if increase < 1 or increase > 3:
            return i + 1

    return None


def is_report_safe(report: List[int]) -> bool:
    return _is_report_safe_return_index(report) is None


def is_report_safe_with_dampener(report: List[int]) -> bool:
    # Reverse if decreasing to simplify.
    if report[0] > report[-1]:
        report = list(report)
        report.reverse()

    # Get problematic index. If none, the report is already safe.
    index_to_remove = _is_report_safe_return_index(report)
    if index_to_remove is None:
        return True

    # Try popping that index.
    report_altered = list(report)
    report_altered.pop(index_to_remove)
    if is_report_safe(report_altered):
        return True

    # Try popping the index before that one.
    report_altered = list(report)
    report_altered.pop(index_to_remove - 1)
    if is_report_safe(report_altered):
        return True

    return False


def part1() -> int:
    reports = get_reports()
    num_safe = sum(1 for r in reports if is_report_safe(r))
    return num_safe


def part2() -> int:
    reports = get_reports()
    num_safe = sum(1 for r in reports if is_report_safe_with_dampener(r))
    return num_safe


def main():
    print(f"PART 1 SOLUTION: {part1()}")
    print(f"PART 2 SOLUTION: {part2()}")


if __name__ == "__main__":
    main()
