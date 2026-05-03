from ex0 import FlameFactory, AquaFactory


def test_factory(factory):
    print("Testing factory")
    base = factory.create_base()
    evolved = factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())


def battle(factory1, factory2):
    print("Testing battle")
    base1 = factory1.create_base()
    base2 = factory2.create_base()
    print(base1.describe())
    print("vs.")
    print(base2.describe())
    print("fight!")
    print(base1.attack())
    print(base2.attack())


if __name__ == "__main__":
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()

    test_factory(flame_factory)
    test_factory(aqua_factory)
    battle(flame_factory, aqua_factory)
