import random


def main() -> None:
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
