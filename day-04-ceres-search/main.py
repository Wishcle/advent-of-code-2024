
from typing import List


def get_input_lines() -> List[str]:
    with open("input.txt", "r") as f:
        return f.readlines()


def check_letter(grid: List[str], letter: str, x: int, y: int) -> bool:
    """Return true if the letter is at location (x, y) in the grid."""
    assert len(letter) == 1
    if y < 0 or y >= len(grid):
        return False
    if x < 0 or x >= len(grid[0]):
        return False
    return grid[y][x] == letter


def count_xmas(grid: List[str], x: int, y: int) -> int:
    """Return the number of XMASs found starting at (x, y) in the grid (between 0 and 8)."""
    ranges = []
    ranges.append([(x, y_i) for y_i in range(y, y - 4, -1)])  # N
    ranges.append([(x, y_i) for y_i in range(y, y + 4,  1)])  # S
    ranges.append([(x_i, y) for x_i in range(x, x - 4, -1)])  # W
    ranges.append([(x_i, y) for x_i in range(x, x + 4,  1)])  # E
    ranges.append([(x_i, y_i) for x_i, y_i in zip(range(x, x - 4, -1), range(y, y - 4, -1))])  # NW
    ranges.append([(x_i, y_i) for x_i, y_i in zip(range(x, x + 4,  1), range(y, y - 4, -1))])  # NE
    ranges.append([(x_i, y_i) for x_i, y_i in zip(range(x, x - 4, -1), range(y, y + 4,  1))])  # SW
    ranges.append([(x_i, y_i) for x_i, y_i in zip(range(x, x + 4,  1), range(y, y + 4,  1))])  # SE

    count = 0

    for range_ in ranges:
        results = []
        for (x, y), letter in zip(range_, "XMAS"):
            result = check_letter(grid, letter, x, y)
            results.append(result)

        if all(results):
            count += 1

    return count


def count_x_mas(grid: List[str], x: int, y: int) -> int:
    """Return the number of X-MASs found starting at (x, y) in the grid (0 or 1)."""
    if not check_letter(grid, "A", x, y):
        return 0

    mas_ne_sw = (
        (check_letter(grid, "M", x - 1, y - 1) and check_letter(grid, "S", x + 1, y + 1)) or
        (check_letter(grid, "S", x - 1, y - 1) and check_letter(grid, "M", x + 1, y + 1)))

    mas_nw_se = (
        (check_letter(grid, "M", x + 1, y - 1) and check_letter(grid, "S", x - 1, y + 1)) or
        (check_letter(grid, "S", x + 1, y - 1) and check_letter(grid, "M", x - 1, y + 1)))

    if mas_ne_sw and mas_nw_se:
        return 1

    return 0


def part1() -> int:
    grid = get_input_lines()
    occurrences = 0

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            occurrences += count_xmas(grid, x, y)

    return occurrences


def part2() -> int:
    grid = get_input_lines()
    occurrences = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            occurrences += count_x_mas(grid, x, y)
    return occurrences


def main():
    print(f"PART 1 SOLUTION: {part1()}")
    print(f"PART 2 SOLUTION: {part2()}")


if __name__ == "__main__":
    main()
