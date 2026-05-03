#!/usr/bin/env python3
from ex0 import FlameFactory, AquaFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import NormalStrategy, AggressiveStrategy, DefensiveStrategy, InvalidCombinationError


def battle(opponents: list[tuple]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    for i in range(len(opponents)):
        for j in range(i + 1, len(opponents)):
            factory1, strategy1 = opponents[i]
            factory2, strategy2 = opponents[j]

            creature1 = factory1.create_base()
            creature2 = factory2.create_base()

            print("* Battle *")
            print(creature1.describe())
            print("vs.")
            print(creature2.describe())
            print("now fight!")
            try:
                actions1 = strategy1.act(creature1)
                for action in actions1:
                    print(action)
            except InvalidCombinationError as e:
                print(f"Battle error, aborting tournament: {e}")
                return
            try:
                actions2 = strategy2.act(creature2)
                for action in actions2:
                    print(action)
            except InvalidCombinationError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


if __name__ == "__main__":
    print("Tournament 0 (basic)")
    flame_factory = FlameFactory()
    healing_factory = HealingCreatureFactory()
    normal_strategy = NormalStrategy()
    defensive_strategy = DefensiveStrategy()

    print("[ (Flameling+Normal), (Healing+Defensive) ]")
    battle([
        (flame_factory, normal_strategy),
        (healing_factory, defensive_strategy),
    ])
    print()
    print("Tournament 1 (error)")
    aggressive_strategy = AggressiveStrategy()

    print("[ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([
        (flame_factory, aggressive_strategy),
        (healing_factory, defensive_strategy),
    ])

    print()
    print("Tournament 2 (multiple)")
    aqua_factory = AquaFactory()
    transform_factory = TransformCreatureFactory()

    print("[ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    battle([
        (aqua_factory, normal_strategy),
        (healing_factory, defensive_strategy),
        (transform_factory, aggressive_strategy),
    ])
