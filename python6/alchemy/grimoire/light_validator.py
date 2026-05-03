def validate_ingredients(ingredients: str) -> str:
    from alchemy.grimoire.light_spellbook import (
        light_spell_allowed_ingredients,
    )

    allowed = light_spell_allowed_ingredients()
    ingredients_lower = ingredients.lower()
    for ingredient in allowed:
        if ingredient in ingredients_lower:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
