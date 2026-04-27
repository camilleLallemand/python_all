======= ex0/ft_command_quest.py =======
import sys

def process_arg() -> None:
    if len(sys.argv) < 1:
        print("No program name found")
        return
    print(f"Program name: {sys.argv[0]}")
    if len(sys.argv) > 1:
        print(f"Arguments received: {len(sys.argv) - 1}")
        for i, arg in enumerate(sys.argv[1:]):
            print(f"Argument {i + 1}: {arg}")
    else:
        print("No arguments provided!")

    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    print("=== Command Quest ===")
    process_arg()

======= ex1/ft_score_analytics.py =======
import sys


def score_analytics() -> None:
    if len(sys.argv) < 2:
        print(
            "No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...")
        return
    score = []
    for arg in sys.argv[1:]:
        try:
            score.append(float(arg))
        except ValueError:
            print(f"Invalid parameter: '{arg}'")
    if len(score) == 0:
        print(
            "No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...")
        return
    total_players = len(score)
    total_score = round(sum(score))
    average_score = total_score / total_players
    high_score = round(max(score))
    low_score = round(min(score))
    score_range = high_score - low_score

    print("Scores processed:", [round(i) for i in score])
    print("Total players:", total_players)
    print("Total score:", total_score)
    print("Average score:", average_score)
    print("High score:", high_score)
    print("Low score:", low_score)
    print("Score range:", score_range)


if __name__ == "__main__":
    print("=== Player Score Analytics ===")
    score_analytics()

======= ex2/ft_coordinate_system.py =======
import math
from typing import Tuple


def get_coordinates(prompt: str) -> Tuple[float, float, float]:
    while True:
        coord = input(prompt)
        parts = coord.split(',')
        if len(parts) != 3:
            print("Invalid syntax")
            continue
        try:
            x = float(parts[0].strip())
            y = float(parts[1].strip())
            z = float(parts[2].strip())
            return (x, y, z)
        except ValueError as e:
            for p in parts:
                p = p.strip()
                try:
                    float(p)
                except ValueError:
                    print(f"Error on parameter '{p}': {e}")
                    break


if __name__ == "__main__":
    print("=== Game Coordinate System ===")
    print("Get a first set of coordinates")
    pos1 = get_coordinates("Enter new coordinates as floats in format 'x,y,z': ")
    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")
    dist1 = math.sqrt(pos1[0]**2 + pos1[1]**2 + pos1[2]**2)
    print("Distance to center: {:.4f}".format(dist1))
    print("Get a second set of coordinates")
    pos2 = get_coordinates("Enter new coordinates as floats in format 'x,y,z': ")
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    dz = pos2[2] - pos1[2]
    dist2 = math.sqrt(dx**2 + dy**2 + dz**2)
    print("Distance between the 2 sets of coordinates: {:.4f}".format(dist2))

======= ex3/ft_achievement_tracker.py =======
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

======= ex4/ft_inventory_system.py =======
#!/usr/bin/env python3

import sys


def parse_inventory(args) -> dict[str, int]:
    inventory = {}
    for arg in args:
        if ':' not in arg:
            print(f"Error - invalid parameter '{arg}'")
            continue
        item, qty_str = arg.split(':', 1)
        if item in inventory:
            print(f"Redundant item '{item}' - discarding")
            continue
        try:
            qty = int(qty_str)
        except ValueError as e:
            print(f"Quantity error for '{item}': {e}")
            continue
        inventory[item] = qty
    return inventory


def display_inventory(inventory):
    print(f"Got inventory: {inventory}")
    items = list(inventory.keys())
    print(f"Item list: {items}")
    total_qty = sum(inventory.values())
    print(f"Total quantity of the {len(items)} items: {total_qty}")
    for item in items:
        percent = round(inventory[item] / total_qty * 100, 1)
        print(f"Item {item} represents {percent}%")
    # Most and least abundant items
    max_qty = max(inventory.values())
    min_qty = min(inventory.values())
    # pick first item in case of tie
    most_item = next(k for k, v in inventory.items() if v == max_qty)
    least_item = next(k for k, v in inventory.items() if v == min_qty)
    print(f"Item most abundant: {most_item} with quantity {max_qty}")
    print(f"Item least abundant: {least_item} with quantity {min_qty}")
    # Add new item
    inventory['magic_item'] = 1
    print(f"Updated inventory: {inventory}")


def main():
    print("=== Inventory System Analysis ===")
    if len(sys.argv) < 2:
        print("Usage: python3 ft_inventory_system.py item1:qty1 item2:qty2 ...")
        return
    args = sys.argv[1:]
    inventory = parse_inventory(args)
    display_inventory(inventory)


if __name__ == "__main__":
    main()

======= ex5/ft_data_stream.py =======
import random
from typing import Generator


def gen_event() -> Generator[tuple[str, str], None, None]:
    players = ["bob", "alice", "charlie", "dylan"]
    actions = [
        "run",
        "eat",
        "sleep",
        "grab",
        "move",
        "climb",
        "swim",
        "release",
        "use"]
    while True:
        yield (random.choice(players), random.choice(actions))


def consume_event(
    events: list[tuple[str, str]]
) -> Generator[tuple[str, str], None, None]:
    while events:
        i = random.randint(0, len(events) - 1)
        yield events.pop(i)


def main() -> None:
    print("=== Game Data Stream Processor ===")

    event_gen = gen_event()
    for i in range(1000):
        player, action = next(event_gen)
        print(f"Event {i}: Player {player} did action {action}")

    event_list = [next(event_gen) for _ in range(10)]
    print(f"\nBuilt list of 10 events: {event_list}")

    for event in consume_event(event_list):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {event_list}")


if __name__ == "__main__":
    main()

======= ex6/ft_data_alchemist.py =======
import random


def main():
    print("=== Game Data Alchemist ===")

    players = ['Alice', 'bob', 'Charlie', 'dylan',
               'Emma', 'Gregory', 'john', 'kevin', 'Liam']

    print(f"Initial list of players: {players}")

    all_cap = [name.capitalize() for name in players]
    print(f"New list with all names capitalized: {all_cap}")

    cap_only = [name for name in players if name == name.capitalize()]
    print(f"New list of capitalized names only: {cap_only}")

    score_dict = {name: random.randint(0, 1000) for name in all_cap}
    print(f"Score dict: {score_dict}")

    avg = round(sum(score_dict.values()) / len(score_dict), 2)
    print(f"Score average is {avg}")

    high_scores = {name: score for name, score in score_dict.items()
                   if score > avg}
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()

