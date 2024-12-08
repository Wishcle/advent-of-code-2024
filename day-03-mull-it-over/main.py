
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


def process_instructions(instructions: List[str]) -> int:
    result = 0
    muls_enabled = True

    for instruction in instructions:
        match instruction:
            case "do()":
                muls_enabled = True
            case "don't()":
                muls_enabled = False
                pass
            case _:
                assert "mul" in instruction, f"{instruction=}"
                if muls_enabled:
                    result += process_mul(instruction)

    return result


def part1() -> int:
    corrupt_data = ''.join(get_input_lines())
    muls = re.findall(r"mul\(\d{1,3},\d{1,3}\)", corrupt_data)
    result = sum(process_mul(mul) for mul in muls)
    return result


def part2() -> int:
    corrupt_data = ''.join(get_input_lines())

    pattern = (
        r"(mul\(\d{1,3},\d{1,3}\))"
        r"|(do\(\))"
        r"|(don't\(\))"
    )

    instruction_tuples = re.findall(pattern, corrupt_data)
    instructions = [''.join(t) for t in instruction_tuples]
    result = process_instructions(instructions)
    return result


def main():
    print(f"PART 1 SOLUTION: {part1()}")
    print(f"PART 2 SOLUTION: {part2()}")


if __name__ == "__main__":
    main()
