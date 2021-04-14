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
        color (str): color of Blob for display
        x (float): x-coordinate of Blob
        y (float): y-coordinate of Blob
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
        self.color: str = "blue"
        self.x = random.random()
        self.y = random.random()

class MutatedBlob(BaseBlob):
    """Test class for mutated blob"""
    def __init__(self, survival_prob, reproduction_prob, mutation_prob) -> None:
        super().__init__(survival_prob, reproduction_prob, mutation_prob)
        self.name: str = "MutatedBlob"
        self.color: str = "red"

class TestBlob(BaseBlob):
    """Test class for mutated blob"""
    def __init__(self, survival_prob, reproduction_prob, mutation_prob) -> None:
        super().__init__(survival_prob, reproduction_prob, mutation_prob)
        self.name: str = "TestBlob"
        self.color: str = "green"

