"""Repository for all Blob classes and related methods"""
import random


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
        mutated_offspring_traits (tuple): traits used to init mutated offspring
        color (str): color of Blob for display
        x (float): x-coordinate of Blob
        y (float): y-coordinate of Blob
        size (float): effective size of blob
        step (float): increment at which blob moves across environment
    """

    def __init__(
        self, survival_prob, reproduction_prob, mutation_prob
    ) -> None:
        """
        Inits BaseBlob

        Args:
            survival_prob (float): probability of survival at each epoch
            reproduction_prob (float): probability of reproduction at each epoch
            mutation_prob (float): probability of mutation at each epoch
        Returns:
            (None)
        """
        self.name: str = "BaseBlob"
        self.survival_prob: float = survival_prob
        self.reproduction_prob: float = reproduction_prob
        self.mutation_prob: float = mutation_prob

        self.mutation_class: Callable = MutatedBaseBlob
        self.repr_class: Callable = BaseBlob
        self.mutated_offspring_traits = (0.5, 0.5, 0.0)
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
            return self.mutation_class(*self.mutated_offspring_traits)
        else:
            return self.repr_class(
                self.survival_prob, self.reproduction_prob, self.mutation_prob
            )

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


class MutatedBaseBlob(BaseBlob):
    """Test class for mutated base blob"""

    def __init__(
        self, survival_prob, reproduction_prob, mutation_prob
    ) -> None:
        super().__init__(survival_prob, reproduction_prob, mutation_prob)
        self.name: str = "MutatedBaseBlob"
        self.color: str = "red"


class GenericBlob(BaseBlob):
    """Test class for generic secondary blob"""

    def __init__(
        self, survival_prob, reproduction_prob, mutation_prob
    ) -> None:
        super().__init__(survival_prob, reproduction_prob, mutation_prob)
        self.name: str = "GenericBlob"
        self.color: str = "green"


class BlobWithFoodSense(BaseBlob):
    """Class for Blob with detection sense for where food is"""

    def __init__(
        self, survival_prob, reproduction_prob, mutation_prob
    ) -> None:
        """See parent docstrings"""
        super().__init__(survival_prob, reproduction_prob, mutation_prob)
        self.name: str = "BlobWithFoodSense"
        self.color = "purple"
        self.mutation_class: Callable = MutatedBlobWithFoodSense
        self.mutated_offspring_traits = (
            survival_prob,
            reproduction_prob,
            mutation_prob,
        )
        self.repr_class: Callable = BlobWithFoodSense

    def move(self, coords: tuple) -> None:
        """
        Function for determining blob movement. Moves towards coords in
        units of step

        Args:
            coords (tuple): coordinates to move towards
        """
        self.x += self.step * (1 if self.x < coords[0] else -1)
        self.y += self.step * (1 if self.y < coords[1] else -1)


class MutatedBlobWithFoodSense(BlobWithFoodSense):
    """Class for Mutated Blob with detection sense for where food is. This
    blob is bigger and faster than the base food sense blob"""

    def __init__(
        self, survival_prob, reproduction_prob, mutation_prob
    ) -> None:
        """See parent docstrings"""
        super().__init__(survival_prob, reproduction_prob, mutation_prob)
        self.name: str = "MutatedBlobWithFoodSense"
        self.color = "pink"
        self.size = 0.3
        self.step = 0.3
        self.repr_class: Callable = MutatedBlobWithFoodSense
