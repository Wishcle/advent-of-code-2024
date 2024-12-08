
import re
from typing import List


def get_input_lines() -> List[str]:
    with open("input.txt", "r") as f:
        return f.readlines()


def process_mul(statement: str) -> int:
    result = re.match(r"mul\((\d{1,3}),(\d{1,3})\)", statement)
    a = int(result.group(1))
    b = int(result.group(2))
    return a * b


def part1() -> int:
    corrupt_data = ''.join(get_input_lines())
    muls = re.findall(r"mul\(\d{1,3},\d{1,3}\)", corrupt_data)
    result = sum(process_mul(mul) for mul in muls)
    return result


def main():
    print(f"PART 1 SOLUTION: {part1()}")


if __name__ == "__main__":
    main()
