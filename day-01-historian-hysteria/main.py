
from collections import Counter
from typing import List, Tuple


def get_input_lines() -> List[str]:
    with open("input.txt", "r") as f:
        return f.readlines()


def get_input_lists() -> Tuple[List[str], List[str]]:
    pair_strings = get_input_lines()
    pairs = [ps.split() for ps in pair_strings]
    list1 = [int(p[0]) for p in pairs]
    list2 = [int(p[1]) for p in pairs]
    return list1, list2


def part1() -> int:
    list1, list2 = get_input_lists()
    distances = [abs(e1 - e2) for e1, e2 in zip(list1, list2)]
    solution = sum(distances)
    return solution


def part2() -> int:
    list1, list2 = get_input_lists()
    list1_counts = Counter(list1)
    list2_counts = Counter(list2)

    total_similarity_score = 0
    for k, v in list1_counts.items():
        score = k * v * (list2_counts.get(k, 0))
        total_similarity_score += score

    return total_similarity_score


def main():
    print(f"PART 1 SOLUTION: {part1()}")
    print(f"PART 2 SOLUTION: {part2()}")


if __name__ == "__main__":
    main()
