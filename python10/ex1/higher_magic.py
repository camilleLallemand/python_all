from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def combined(target: str, power: int) -> tuple:
        return (spell1(target, power), spell2(target, power))
    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def conditional(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return conditional


def spell_sequence(spells: list[Callable]) -> Callable:
    def sequence(target: str, power: int) -> list:
        return [spell(target, power) for spell in spells]
    return sequence


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} for {power} damage"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


def frost_bolt(target: str, power: int) -> str:
    return f"Frost Bolt chills {target} for {power} damage"


if __name__ == "__main__":

    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    result = combined("Dragon", 20)
    print(f"Combined spell result: {result[0]}, {result[1]}")

    print("\nTesting power amplifier...")
    mega_fireball = power_amplifier(fireball, 3)
    base_power = 10
    original = fireball("Goblin", base_power)
    amplified = mega_fireball("Goblin", base_power)
    print(f"Original: {base_power}, Amplified: {base_power * 3}")
    print(f"  -> {original}")
    print(f"  -> {amplified}")

    print("\nTesting conditional caster...")
    high_power_only = conditional_caster(
        lambda target, power: power >= 30,
        fireball
    )
    print(f"Power 50: {high_power_only('Troll', 50)}")
    print(f"Power 10: {high_power_only('Troll', 10)}")

    print("\nTesting spell sequence...")
    sequence = spell_sequence([fireball, heal, frost_bolt])
    results = sequence("Ancient Dragon", 25)
    for r in results:
        print(f"  -> {r}")

    print("\nVerifying callable() usage:")
    print(f"fireball is callable: {callable(fireball)}")
    print(f"42 is callable: {callable(42)}")
    print(f"spell_combiner is callable: {callable(spell_combiner)}")
