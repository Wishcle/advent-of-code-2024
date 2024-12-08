
from typing import List


def read_input() -> List[str]:
    with open("input.txt", "r") as f:
        return f.readlines()


def main():
    pair_strings = read_input()

    pairs = [ps.split() for ps in pair_strings]
    list1 = [int(p[0]) for p in pairs]
    list2 = [int(p[1]) for p in pairs]
    list1.sort()
    list2.sort()

    distances = [abs(e1 - e2) for e1, e2 in zip(list1, list2)]
    solution = sum(distances)
    print(f"SOLUTION: {solution}")


if __name__ == "__main__":
    main()
