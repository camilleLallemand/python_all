from alchemy.elements import create_air
from alchemy.potions import strength_potion
from elements import create_fire


def lead_to_gold() -> str:
    air = create_air()
    strength = strength_potion()
    fire = create_fire()
    return (
        f"Recipe transmuting Lead to Gold: brew '{air}' and "
        f"'{strength}' mixed with '{fire}'")
