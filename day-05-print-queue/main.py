from typing import List, Set, Dict, Tuple


class Validator:
    pages: Set[int]
    deps: Dict[int, Set[int]]  # rules[i] => <set-of-deps>

    def __init__(self):
        self.pages = set()
        self.deps = {}

    def add_rule(self, rule: str):
        [p1, p2] = [p for p in rule.split("|")]

        self.pages.add(p1)
        self.pages.add(p2)

        p2_deps: Set[int] = self.deps.get(p2, set())
        p2_deps.add(p1)
        self.deps[p2] = p2_deps
        self.deps.setdefault(p1, set())

    def get_update_value(self, update: str) -> Tuple[int, int]:
        """Return the middle number if the update is valid. Else, 0."""
        update_list = update.split(",")
        all_pages = set(self.pages)
        all_deps = {k: set(v) for k, v in self.deps.items()}

        for p in update_list:
            assert p in all_deps
            assert p in all_pages

        # Find pages not in the update...
        for p in update_list:
            all_pages.remove(p)

        # ... And remove them from deps.
        for p in all_pages:
            all_deps = self._remove_page_from_deps(all_deps, p)

        topo_deps = {k: set(v) for k, v in all_deps.items()}
        topo_list = self._calculate_topo_ordering(topo_deps)
        assert len(topo_list) == len(all_deps), f"{len(topo_list)=} != {len(all_deps)=}"

        # For each update page, check that it has no deps.
        # Then remove that page from other deps.
        for p in update_list:
            if len(all_deps[p]) > 0:
                return 0, self._middle_to_int(topo_list)
            all_deps = self._remove_page_from_deps(all_deps, p)

        return (self._middle_to_int(update_list), 0)

    def _middle_to_int(self, list_: List[str]) -> int:
        middle_index = len(list_) // 2
        middle_item = int(list_[middle_index])
        return middle_item

    def _calculate_topo_ordering(self, deps: Dict[int, Set[int]]) -> List[str]:
        ordering = []
        while len(deps) > 0:
            batch = [k for k, v in deps.items() if len(v) == 0]
            assert len(batch) > 0, "impossible to satisfy constraints"
            for p in batch:
                deps = self._remove_page_from_deps(deps, p)
            ordering.extend(batch)
        return ordering

    def _remove_page_from_deps(
        self,
        deps: Dict[int, Set[int]],
        page: int,
    ) -> Dict[int, Set[int]]:
        assert page in deps
        del deps[page]

        for k in list(deps.keys()):
            s = deps[k]
            if page in s:
                s.remove(page)
            deps[k] = s

        return deps


def get_input_lines() -> List[str]:
    with open("input.txt", "r") as f:
        return f.readlines()


def get_rules_and_updates() -> Tuple[List[str], List[str]]:
    lines = get_input_lines()
    lines = [line.strip() for line in lines]
    rules = []
    updates = []

    for i in range(len(lines)):
        if lines[i] == "":
            updates.extend(lines[i + 1 :])
            break
        rules.append(lines[i])

    return rules, updates


def part1() -> int:
    rules, updates = get_rules_and_updates()
    validator = Validator()

    for rule in rules:
        validator.add_rule(rule)

    result = sum(validator.get_update_value(u)[0] for u in updates)
    return result


def part2() -> int:
    rules, updates = get_rules_and_updates()
    validator = Validator()

    for rule in rules:
        validator.add_rule(rule)

    result = sum(validator.get_update_value(u)[1] for u in updates)
    return result


def main():
    print(f"PART 1 SOLUTION: {part1()}")
    print(f"PART 2 SOLUTION: {part2()}")


if __name__ == "__main__":
    main()
