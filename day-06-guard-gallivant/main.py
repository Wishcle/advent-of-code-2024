from tqdm import tqdm
from typing import List, Set, Tuple

Position = Tuple[int, int]
Direction = Tuple[int, int]


class Guard:
    position: Position
    direction_index: int
    directions: List[Direction] = [
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0),
    ]

    distinct_positions: Set[Position] = None
    distinct_positions_with_direction: Set[Tuple[Position, Direction]] = None
    original_position: Position

    def __init__(self, pos: Position):
        self.original_position = pos
        self.reset()

    def next_pos(self) -> Position:
        x, y = self.position
        dx, dy = self.get_direction()
        return x + dx, y + dy

    def get_direction(self) -> Direction:
        return self.directions[self.direction_index]

    def move(self) -> None:
        self.distinct_positions_with_direction.add((self.position, self.get_direction()))

        next_pos = self.next_pos()
        self.position = next_pos
        self.distinct_positions.add(next_pos)

    def rotate(self) -> None:
        self.distinct_positions_with_direction.add((self.position, self.get_direction()))
        self.direction_index = (self.direction_index + 1) % len(self.directions)

    def get_distinct_positions(self) -> int:
        return len(self.distinct_positions)

    def has_been_here_before(self) -> bool:
        return (self.position, self.get_direction()) in self.distinct_positions_with_direction

    def reset(self) -> None:
        pos = self.original_position
        self.position = pos
        self.direction_index = 0
        self.distinct_positions = {pos}
        self.distinct_positions_with_direction = set()


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

    def simulate_guard(self, obstacle_to_add: List[Position] = None) -> int:
        """Return distinct positions of the guard. If loop, return 0."""
        self.guard.reset()
        obstacle_to_add = obstacle_to_add or []
        obstacles = list(self.obstacles) + obstacle_to_add

        # if next pos is off the map, we are done. return distinct positions
        # if next pos is an obstacle, rotate guard
        # otherwise, move guard

        def _off_the_map(x, y) -> bool:
            return x < 0 or x > self.w - 1 or y < 0 or y > self.h - 1

        while True:
            match self.guard.next_pos():
                case (x, y) if _off_the_map(x, y):
                    return self.guard.get_distinct_positions()
                case (x, y) if (x, y) in obstacles:
                    self.guard.rotate()
                    if self.guard.has_been_here_before():
                        return -1
                case _:
                    self.guard.move()
                    if self.guard.has_been_here_before():
                        return -1

    def simulate_all_obstacle_placements(self) -> int:
        """Return the number of obstacle placements that create loops."""
        loops = 0

        # First, get all unique locations of the guard. Any single new obstacle
        # that would create a loop would have to be reachable by the guard.
        self.simulate_guard()
        potential_loop_obstacles = set(self.guard.distinct_positions)

        with tqdm(total=(self.h * self.w)) as progress:
            for y in range(self.h):
                for x in range(self.w):
                    progress.update()
                    if (x, y) not in potential_loop_obstacles:
                        continue
                    if self.simulate_guard([(x, y)]) == -1:
                        loops += 1

        return loops


def get_input_lines() -> List[str]:
    with open("input.txt", "r") as f:
        return f.readlines()


def part1() -> int:
    text = get_input_lines()
    map = Map(text)
    return map.simulate_guard()


def part2() -> int:
    text = get_input_lines()
    map = Map(text)
    return map.simulate_all_obstacle_placements()


def main():
    print(f"PART 1 SOLUTION: {part1()}")
    print(f"PART 2 SOLUTION: {part2()}")


if __name__ == "__main__":
    main()
