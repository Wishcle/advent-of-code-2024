
from typing import List


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


def is_report_safe(report: List[int]) -> bool:
    if len(report) <= 1:
        return True

    # Reverse if decreasing to simplify.
    if report[0] > report[-1]:
        report = list(report)
        report.reverse()

    for i in range(len(report) - 1):
        increase = report[i+1] - report[i]
        if increase < 1 or increase > 3:
            return False

    return True


def part1() -> int:
    reports = get_reports()
    num_safe = sum(1 for r in reports if is_report_safe(r))
    return num_safe


def main():
    print(f"PART 1 SOLUTION: {part1()}")


if __name__ == "__main__":
    main()
