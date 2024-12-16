from typing import List, Set, Tuple

Position = Tuple[int, int]


class Guard:
    position: Position
    direction_index: int = 0
    directions: List[Tuple[int, int]] = [
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0),
    ]

    distinct_positions: Set[Position] = None

    def __init__(self, pos: Position):
        self.position = pos
        self.distinct_positions = {pos}

    def next_pos(self) -> Position:
        x, y = self.position
        dx, dy = self.directions[self.direction_index]
        return x + dx, y + dy

    def move(self) -> None:
        next_pos = self.next_pos()
        self.position = next_pos
        self.distinct_positions.add(next_pos)

    def rotate(self) -> None:
        self.direction_index = (self.direction_index + 1) % len(self.directions)

    def get_distinct_positions(self) -> int:
        return len(self.distinct_positions)


class Map:
    obstacles = Set[Tuple[int, int]]
    guard: Guard = None
    h: int
    w: int

    def __init__(self, text: List[str]):
        self._init_from_text(text)

    def _init_from_text(self, text: List[str]) -> None:
        h = len(text)
        w = len(text[0])
        obstacles = set()
        guard = None

        for y in range(h):
            for x in range(w):
                c = text[y][x]
                match c:
                    case "^":
                        assert self.guard is None, "multiple guards found"
                        guard = Guard((x, y))
                    case "#":
                        obstacles.add((x, y))
                    case _:
                        pass

        self.h = h
        self.w = w
        self.obstacles = obstacles
        self.guard = guard
        assert guard is not None

    def simulate_guard(self) -> int:
        """Return distinct positions of the guard."""

        # if next pos is off the map, we are done. return distinct positions
        # if next pos is an obstacle, rotate guard
        # otherwise, move guard

        def _off_the_map(x, y) -> bool:
            return x < 0 or x > self.w - 1 or y < 0 or y > self.h - 1

        while True:
            match self.guard.next_pos():
                case (x, y) if _off_the_map(x, y):
                    return self.guard.get_distinct_positions()
                case (x, y) if (x, y) in self.obstacles:
                    self.guard.rotate()
                case _:
                    self.guard.move()


def get_input_lines() -> List[str]:
    with open("input.txt", "r") as f:
        return f.readlines()


def part1() -> int:
    text = get_input_lines()
    map = Map(text)
    return map.simulate_guard()


def main():
    print(f"PART 1 SOLUTION: {part1()}")


if __name__ == "__main__":
    main()
