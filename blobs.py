"""Repository for all Blob classes and related methods"""
import random
from typing import List
from helpers import find_closest_coord


class BaseBlob:
    """
    Base class for blob. Each blob class should functionally contain at a
    minimum a reproduce method and a move method

    Attributes:
        name (str): name associated with blob type
        survival_prob (float): probability of survival at each epoch
        reproduction_prob (float): probability of reproduction at each epoch
        mutation_prob (float): probability of mutation at each epoch

        mutation_class (Callable): class to mutate to
        repr_class (Callable) class to produce when reproducing w/o mutation
        color (str): color of Blob for display
        x (float): x-coordinate of Blob
        y (float): y-coordinate of Blob
        size (float): effective size of blob
        step (float): increment at which blob moves across environment
    """

    def __init__(self) -> None:
        """Inits BaseBlob"""
        self.name: str = "BaseBlob"
        self.survival_prob: float = 0.5
        self.reproduction_prob: float = 0.5
        self.mutation_prob: float = 0.5

        self.mutation_class: Callable = MutatedBaseBlob
        self.repr_class: Callable = BaseBlob
        self.color: str = "blue"
        self.x = random.random()
        self.y = random.random()
        self.size = 0.1
        self.step = 0.1

    def reproduce(self):
        """
        Generic reproduction function. If mutate, return a generic
        MutatedBaseBlob with attributes defined

        Returns:
            (Blob): the type of Blob produced will depend on the mutation_class
            and repr_class attributes declared in __init__
        """
        mutation_event = random.random()
        if mutation_event <= self.mutation_prob:
            return self.mutation_class()
        else:
            return self.repr_class()

    def move(self, coords: tuple) -> None:
        """
        Function for determining blob movement. BaseBlob move randomly

        Args:
            coords (tuple): coordinates to move towards. For BaseBlob, this
            is mute since the blobs don't actually move towards the coord
        """
        # Move in random direction (-1 or +1) in increments of step
        self.x += self.step * [-1, 1][random.randrange(2)]
        self.y += self.step * [-1, 1][random.randrange(2)]

    def set_probs(
        self, survival_prob: float, repr_prob: float, mutation_prob: float
    ) -> None:
        """Setter for the three probability attrs"""
        self.survival_prob = survival_prob
        self.reproduction_prob = repr_prob
        self.mutation_prob = mutation_prob

    def __str__(self):
        """Prints out name of blob"""
        return (
            f"""{self.name}(s={self.survival_prob},"""
            f"""r={self.reproduction_prob},m={self.mutation_prob})"""
        )


class PerfectTestBlob(BaseBlob):
    """Blob with 1.0 for all attrs. Used primarily for testing"""

    def __init__(self) -> None:
        super().__init__()
        self.name: str = "PerfectTestBlob"
        self.repr_class: Callable = MutatedBaseBlob


class MutatedBaseBlob(BaseBlob):
    """Class for mutated base blob"""

    def __init__(self) -> None:
        super().__init__()
        self.name: str = "MutatedBaseBlob"
        self.color: str = "red"
        self.repr_class: Callable = MutatedBaseBlob


class SturdyBlob(BaseBlob):
    """Class for generic sturdy blob"""

    def __init__(self) -> None:
        super().__init__()
        self.name: str = "SturdyBlob"
        self.color: str = "green"
        self.repr_class: Callable = SturdyBlob
        self.survival_prob: float = 0.8
        self.reproduction_prob: float = 0.5
        self.mutation_prob: float = 0.0


class HungryBlob(BaseBlob):
    """Class for Blob with detection sense for where food is"""

    def __init__(self) -> None:
        """See parent docstrings"""
        super().__init__()
        self.name: str = "HungryBlob"
        self.color = "purple"
        self.mutation_class: Callable = MutatedHungryBlob
        self.repr_class: Callable = HungryBlob

    def move(self, coords: tuple) -> None:
        """
        Function for determining blob movement. Moves towards coords in
        units of step

        Args:
            coords (tuple): coordinates to move towards
        """
        self.x += self.step * (1 if self.x < coords[0] else -1)
        self.y += self.step * (1 if self.y < coords[1] else -1)


class MutatedHungryBlob(HungryBlob):
    """Class for Mutated Blob with detection sense for where food is. This
    blob is bigger and faster than the base food sense blob"""

    def __init__(self) -> None:
        """See parent docstrings"""
        super().__init__()
        self.name: str = "MutatedHungryBlob"
        self.color = "pink"
        self.size = 0.3
        self.step = 0.3
        self.repr_class: Callable = MutatedHungryBlob


class BaseInteractingBlob(HungryBlob):
    """Base class for Blob that can interact with other blobs. Note that
    this blob is hungry by default"""

    def __init__(self) -> None:
        """See parent docstrings"""
        super().__init__()
        self.name: str = "BaseInteractingBlob"
        self.color = "gray"
        self.survival_prob: float = 0.8
        self.reproduction_prob: float = 0.5
        self.mutation_prob: float = 0.0
        self.size = 0.3
        self.mutation_class: Callable = BaseInteractingBlob
        self.repr_class: Callable = BaseInteractingBlob

    def interact_with_surroundings(self, interaction_list: List) -> None:
        """
        Base function for blobs to interact with surroundings

        Args:
            interaction_list (List): objects to interact with"""
        pass


class AttackingBlob(BaseInteractingBlob):
    """Class for Blob that will attack other nearby blobs"""

    def __init__(self) -> None:
        """See parent docstrings"""
        super().__init__()
        self.name: str = "AttackingBlob"
        self.color = "red"
        self.mutation_class: Callable = AttackingBlob
        self.repr_class: Callable = AttackingBlob
        self.attack_dmg = 0.2

    def interact_with_surroundings(self, interaction_list: List) -> None:
        """
        Attacks nearby blobs, damaging their survival_prob

        Args:
            interaction_list (List): list of blobs to attack
        """
        for b in interaction_list:
            b.survival_prob -= self.attack_dmg


class TimidBlob(BaseInteractingBlob):
    """Class for Blob that will run away from other aggressive blobs"""

    def __init__(self) -> None:
        """See parent docstrings"""
        super().__init__()
        self.name: str = "TimidBlob"
        self.color = "green"
        self.mutation_class: Callable = TimidBlob
        self.repr_class: Callable = TimidBlob

    def run_away(self, coords: tuple) -> None:
        """
        Run away from coordinate of other blob. Opposite of move function

        Args:
            coords (tuple): (x,y) of blob to run away from
        """
        self.x -= self.step * (1 if self.x < coords[0] else -1)
        self.y -= self.step * (1 if self.y < coords[1] else -1)

    def interact_with_surroundings(self, interaction_list: List) -> None:
        """
        TimidBlob runs in the opposite direction of the closest attacking
        blob

        Args:
            interaction_list (List): list of blobs to attack
        """
        blob_coords = [(b.x, b.y) for b in interaction_list]
        closest_attacker_coords, _ = find_closest_coord(
            (self.x, self.y), blob_coords
        )
        if closest_attacker_coords:
            self.run_away(closest_attacker_coords)


class QuickBlob(BaseInteractingBlob):
    """Class for very quick blob. QuickBlobs eat before any other blob, at
    the expense of a generally lower survival_prob"""

    def __init__(self) -> None:
        """See parent docstrings"""
        super().__init__()
        self.name: str = "QuickBlob"
        self.color = "yellow"
        self.mutation_class: Callable = QuickBlob
        self.repr_class: Callable = QuickBlob
