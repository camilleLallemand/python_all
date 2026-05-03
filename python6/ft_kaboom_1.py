print("=== Kaboom 1 ===")
print("Access to alchemy/grimoire/dark_spellbook.py directly")
print("Test import now - THIS WILL RAISE A CAUGHT EXCEPTION")
try:
    from alchemy.grimoire.dark_spellbook import dark_spell_record
except BaseException as e:
    print(e)
