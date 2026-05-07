import functools
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0

    operations = {
        'add': operator.add,
        'multiply': operator.mul,
        'max': lambda a, b: a if a > b else b,
        'min': lambda a, b: a if a < b else b,
    }

    if operation not in operations:
        raise ValueError(f"Unknown operation: '{operation}'. "
                         f"Valid operations: {list(operations.keys())}")

    return functools.reduce(operations[operation], spells)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    fire_enchant = functools.partial(
        base_enchantment, power=50, element='fire')
    water_enchant = functools.partial(
        base_enchantment, power=50, element='water')
    earth_enchant = functools.partial(
        base_enchantment, power=50, element='earth')

    return {
        'fire': fire_enchant,
        'water': water_enchant,
        'earth': earth_enchant,
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n == 0:
        return 0
    if n == 1:
        return 1
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @functools.singledispatch
    def dispatch(spell) -> str:
        return "Unknown spell type"

    @dispatch.register(int)
    def _(spell: int) -> str:
        return f"Damage spell: {spell} damage"

    @dispatch.register(str)
    def _(spell: str) -> str:
        return f"Enchantment: {spell}"

    @dispatch.register(list)
    def _(spell: list) -> str:
        return f"Multi-cast: {len(spell)} spells"

    return dispatch


if __name__ == "__main__":
    print("Testing spell reducer...")
    powers = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(powers, 'add')}")
    print(f"Product: {spell_reducer(powers, 'multiply')}")
    print(f"Max: {spell_reducer(powers, 'max')}")
    print(f"Min: {spell_reducer(powers, 'min')}")
    print(f"Empty list: {spell_reducer([], 'add')}")
    try:
        spell_reducer(powers, 'unknown')
    except ValueError as e:
        print(f"Error handled: {e}")

    print("\nTesting partial enchanter...")

    def base_enchantment(power: int, element: str, target: str) -> str:
        return f"{
            element.capitalize()} enchantment ({power} power) applied to {target}"

    enchants = partial_enchanter(base_enchantment)
    print(enchants['fire'](target='Sword'))
    print(enchants['water'](target='Shield'))
    print(enchants['earth'](target='Armor'))

    print("\nTesting memoized fibonacci...")
    for n in [0, 1, 10, 15]:
        print(f"Fib({n}): {memoized_fibonacci(n)}")
    print(f"Cache info: {memoized_fibonacci.cache_info()}")

    print("\nTesting spell dispatcher...")
    dispatcher = spell_dispatcher()
    print(dispatcher(42))
    print(dispatcher("fireball"))
    print(dispatcher(["bolt", "heal", "shield"]))
    print(dispatcher(3.14))
