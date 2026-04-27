#!/usr/bin/env python3
import random
from typing import List, Set

POSSIBLE_ACHIEVEMENTS = {
    "Crafting Genius",
    "World Savior",
    "Master Explorer",
    "Collector Supreme",
    "Untouchable",
    "Boss Slayer",
    "Strategist",
    "Speed Runner",
    "Survivor",
    "Treasure Hunter",
    "First Steps",
    "Unstoppable",
    "Sharp Mind",
    "Hidden Path Finder"
}

PLAYER_NAMES = ["Alice", "Bob", "Charlie", "Dylan"]


def gen_player_achievements() -> Set[str]:
    count = random.randint(5, 8)
    return set(random.sample(list(POSSIBLE_ACHIEVEMENTS), count))


def main() -> None:
    print("=== Achievement Tracker System ===\n")

    players: List[Set[str]] = []
    for name in PLAYER_NAMES:
        achievements = gen_player_achievements()
        players.append(achievements)
        print(f"Player {name}: {achievements}")
    print()

    all_achievements = set().union(*players)
    print(f"All distinct achievements: {all_achievements}")

    common = set.intersection(*players)
    print(f"Common achievements: {common}")

    for i, name in enumerate(PLAYER_NAMES):
        others = set().union(*(players[:i] + players[i + 1:]))
        unique = players[i].difference(others)
        print(f"Only {name} has: {unique}")

    print()
    for i, name in enumerate(PLAYER_NAMES):
        missing = all_achievements.difference(players[i])
        print(f"{name} is missing: {missing}")


if __name__ == "__main__":
    main()
