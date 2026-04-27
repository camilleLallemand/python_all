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
