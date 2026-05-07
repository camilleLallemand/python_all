def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return (
        sorted(
            artifacts,
            key=lambda artifact: artifact['power'],
            reverse=True))


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return (
        list(
            filter(
                lambda mage: mage['power'] >= min_power,
                mages)))


def spell_transformer(spell: list[str]) -> list[str]:
    return (
        list(
            map(
                lambda spell: f"* {spell} *",
                spell)))


def mage_stats(mages: list[dict]) -> list[dict]:
    max_power = max(mages, key=lambda mage: mage['power'])['power']
    min_power = min(mages, key=lambda mage: mage['power'])['power']
    avg_power = round(
        sum(map(lambda mage: mage['power'], mages)) / len(mages), 2)
    return {
        'max_power': max_power,
        'min_power': min_power,
        'avg_power': avg_power
    }


if __name__ == "__main__":
    artifacts = [
        {'name': 'Crystal Orb', 'power': 85, 'type': 'orb'},
        {'name': 'Fire Staff', 'power': 92, 'type': 'staff'},
        {'name': 'Shadow Dagger', 'power': 60, 'type': 'blade'},
    ]

    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    first, second = sorted_artifacts[0], sorted_artifacts[1]
    print(
        f"{first['name']} ({first['power']} power) comes before "
        f"{second['name']} ({second['power']} power)"
    )

    mages = [
        {'name': 'Alex', 'power': 90, 'element': 'fire'},
        {'name': 'Jordan', 'power': 45, 'element': 'water'},
        {'name': 'Riley', 'power': 70, 'element': 'earth'},
    ]

    print("\nTesting power filter...")
    filtered = power_filter(mages, 70)
    for mage in filtered:
        print(f"{mage['name']} ({mage['power']} power)")

    spells = ["fireball", "heal", "shield"]
    print("\nTesting spell transformer...")
    transformed = spell_transformer(spells)
    print(" ".join(transformed))

    print("\nTesting mage stats...")
    stats = mage_stats(mages)
    print(f"Max power: {stats['max_power']}")
    print(f"Min power: {stats['min_power']}")
    print(f"Avg power: {stats['avg_power']}")
