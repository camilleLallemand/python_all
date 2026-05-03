from abc import ABC, abstractmethod
import ex0
import ex1


class InvalidCombinationError(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: ex0.Creature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: ex0.Creature) -> list[str]:
        pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: ex0.Creature) -> bool:
        return True

    def act(self, creature: ex0.Creature) -> list[str]:
        if not self.is_valid(creature):
            raise InvalidCombinationError(
                f"Invalid creature '{creature.name}' for this normal strategy"
            )
        return [creature.attack()]


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: ex0.Creature) -> bool:
        return isinstance(creature, ex1.TransformCapability)

    def act(self, creature: ex0.Creature) -> list[str]:
        if not self.is_valid(creature):
            raise InvalidCombinationError(
                f"Invalid creature '{
                    creature.name}' for this aggressive strategy")
        actions = []
        actions.append(creature.transform())
        actions.append(creature.attack())
        actions.append(creature.revert())
        return actions


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: ex0.Creature) -> bool:
        return isinstance(creature, ex1.HeaalCapability)

    def act(self, creature: ex0.Creature) -> list[str]:
        if not self.is_valid(creature):
            raise InvalidCombinationError(
                f"Invalid creature '{
                    creature.name}' for this defensive strategy")
        actions = []
        actions.append(creature.attack())
        actions.append(creature.heal())
        return actions


__all__ = [
    "NormalStrategy",
    "AggressiveStrategy",
    "DefensiveStrategy",
    "InvalidCombinationError"
]
