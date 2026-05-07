import inspect
import time
import functools
from collections.abc import Callable


def spell_timer(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Casting {func.__name__}...")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result
    return wrapper


def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        param_names = list(inspect.signature(func).parameters.keys())

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if 'power' in kwargs:
                power = kwargs['power']
            elif 'power' in param_names:
                idx = param_names.index('power')
                power = args[idx] if idx < len(args) else None
            else:
                power = args[0] if args else None

            if power is not None and power >= min_power:
                return func(*args, **kwargs)
            return "Insufficient power for this spell"
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(
                        f"Spell failed, retrying... "
                        f"(attempt {attempt}/{max_attempts})"
                    )
            return f"Spell casting failed after {max_attempts} attempts"
        return wrapper
    return decorator


class MageGuild:

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and all(
            char.isalpha() or char == ' ' for char in name)

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


if __name__ == "__main__":
    print("Testing spell timer...")

    @spell_timer
    def fireball() -> str:
        time.sleep(0.1)
        return "Fireball cast!"

    result = fireball()
    print(f"Result: {result}")

    print("\nTesting power validator...")

    @power_validator(min_power=20)
    def lightning_bolt(power: int, target: str) -> str:
        return f"Lightning strikes {target} for {power} damage"

    print(lightning_bolt(50, "Dragon"))
    print(lightning_bolt(5, "Dragon"))

    print("\nTesting retrying spell...")

    @retry_spell(max_attempts=3)
    def always_fails() -> str:
        raise RuntimeError("This spell always fails")

    result = always_fails()
    print(result)

    print("\nWaaaaaaagh spelled !")

    print("\nTesting MageGuild...")
    guild = MageGuild()
    print(MageGuild.validate_mage_name("Alex"))
    print(MageGuild.validate_mage_name("X2"))

    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Thunder", 5))
