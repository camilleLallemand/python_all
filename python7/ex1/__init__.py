from abc import ABC, abstractmethod
import ex0


class HeaalCapability(ABC):
    @abstractmethod
    def heal(self, target=None) -> str:
        pass


class TransformCapability(ABC):
    def __init__(self):
        self._is_transofrme = False

    @property
    def is_transofrmed(self):
        return self._is_transofrme

    @abstractmethod
    def transform(self) -> str:
        pass

    @abstractmethod
    def revert(self) -> str:
        pass


class Sproutling(ex0.Creature, HeaalCapability):
    def __init__(self):
        ex0.Creature.__init__(self, "Sproutling", "Grass")
        HeaalCapability.__init__(self)

    def attack(self) -> str:
        return f"{self.name} uses Vine Whip!"

    def heal(self, target=None) -> str:
        return f"{self.name} heals itself for a small amount"


class Bloomelle(ex0.Creature, HeaalCapability):
    def __init__(self):
        ex0.Creature.__init__(self, "Bloomelle", "Grass/Fairy")
        HeaalCapability.__init__(self)

    def attack(self) -> str:
        return f"{self.name} uses Petal Dance!"

    def heal(self, target=None) -> str:
        return f"{self.name} heals itself and others for a large amount"


class Shiftling(ex0.Creature, TransformCapability):
    def __init__(self):
        ex0.Creature.__init__(self, "Shiftling", "Normal")
        TransformCapability.__init__(self)

    def attack(self):
        if self.is_transofrmed:
            return f"{self.name} performs a boosted strike!:"
        else:
            return f"{self.name} attacks normally"

    def transform(self) -> str:
        self._is_transofrme = True
        return f"{self.name} shifts into a sharper form!"

    def revert(self) -> str:
        self._is_transofrme = False
        return f"{self.name} returns to normal."


class Morphagon(ex0.Creature, TransformCapability):
    def __init__(self):
        ex0.Creature.__init__(self, "Morphagon", "Normal")
        TransformCapability.__init__(self)

    def attack(self):
        if self.is_transofrmed:
            return f"{self.name} performs a devastating morph strike!"
        else:
            return f"{self.name} attacks normally"

    def transform(self) -> str:
        self._is_transofrme = True
        return f"{self.name} morphs into a dragonic battle form"

    def revert(self) -> str:
        self._is_transofrme = False
        return f"{self.name} stabilizes its form."


class HealingCreatureFactory(ex0.CreatureFactory):
    def create_base(self) -> Sproutling:
        return Sproutling()

    def create_evolved(self) -> Bloomelle:
        return Bloomelle()


class TransformCreatureFactory(ex0.CreatureFactory):
    def create_base(self) -> Shiftling:
        return Shiftling()

    def create_evolved(self) -> Morphagon:
        return Morphagon()


__all__ = ["HealingCreatureFactory", "TransformCreatureFactory"]
