"""Repository for all Blob classes and related methods"""
import random

class BaseBlob:
    """
    Base class for blobs

    Attributes:
        name (str): name associated with blob type
        survival_prob (float): probability of survival at each epoch
        reproduction_prob (float): probability of reproduction at each epoch
        mutation_prob (float): probability of mutation at each epoch

        mutation_class (Callable): class to mutate to
        mutated_offspring_traits (tuple): traits used to init mutated offspring
        color (str): color of Blob for display
        x (float): x-coordinate of Blob
        y (float): y-coordinate of Blob
        step (float): increment at which blob moves across environment
    """
    def __init__(self, survival_prob, reproduction_prob, mutation_prob) -> None:
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
        self.mutated_offspring_traits = (0.5, 0.5, 0.0)
        self.color: str = "blue"
        self.x = random.random()
        self.y = random.random()
        self.step = 1.0

    def reproduce(self):
        """
        Generic reproduction function. If mutate, return a generic
        MutatedBaseBlob with attributes defined

        Returns:
            (Blob)
        """
        mutation_event = random.random()
        if mutation_event <= self.mutation_prob:
            return self.mutation_class(*self.mutated_offspring_traits)
        else:
            return BaseBlob(self.survival_prob,
                    self.reproduction_prob,
                    self.mutation_prob)

    def move(self, coords: tuple) -> None:
        """
        Function for determining blob movement. BaseBlob move randomly

        Args:
            coords (tuple): coordinates to move towards
            """
        move_scale = 0.1
        self.x = self.x + (self.step * random.uniform(-move_scale, move_scale))
        self.y = self.y + (self.step * random.uniform(-move_scale, move_scale))

class MutatedBaseBlob(BaseBlob):
    """Test class for mutated base blob"""
    def __init__(self, survival_prob, reproduction_prob, mutation_prob) -> None:
        super().__init__(survival_prob, reproduction_prob, mutation_prob)
        self.name: str = "MutatedBaseBlob"
        self.color: str = "red"

class TestBlob(BaseBlob):
    """Test class for generic secondary blob"""
    def __init__(self, survival_prob, reproduction_prob, mutation_prob) -> None:
        super().__init__(survival_prob, reproduction_prob, mutation_prob)
        self.name: str = "TestBlob"
        self.color: str = "green"

class BlobWithFoodSense(BaseBlob):
    """Class for Blob with detection sense for where food is"""
    def __init__(self, survival_prob, reproduction_prob, mutation_prob) -> None:
        super().__init__(survival_prob, reproduction_prob, mutation_prob)
        self.name: str = "BlobWithFoodSense"
        self.color="purple"

    def move(self, coords: tuple) -> None:
        """
        Function for determining blob movement. BaseBlob move randomly

        Args:
            coords (tuple): coordinates to move towards
        """
        move_x = self.step * (1 if self.x < coords[0] else -1)
        move_y = self.step * (1 if self.y < coords[1] else -1)
        self.x += move_x
        self.y += move_y
