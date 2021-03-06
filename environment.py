"""Repository for all Environment related classes"""
from typing import List, Dict
from pathlib import Path
from time import sleep
import random
from IPython.display import clear_output
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
import numpy as np
from blobs import BaseBlob
from settings import (
    ENVIRONMENT_DIMENSIONS,
    BLOB_DISPLAY_SIZE,
    FOOD_DISPLAY_SIZE,
    FIG_DIMENSIONS,
)
from helpers import *

sns.set()


class BaseEnvironment:
    """
    Base class for defining boundary conditions for blobs to interact
    within. In this environment, blobs spawn, die, and reproduce purely via.
    attribute probabilities.

    Attributes:
        dimension (int): dimension of environment for Blobs to interact in.
            Note that dimension will be broadcast to a square environment
        population (List): container of all Blobs that exist in Environment
    """

    def __init__(self) -> None:
        """
        Inits BaseEnvironment
        """
        self.dimension: int = ENVIRONMENT_DIMENSIONS
        self.population: List = []

    def spawn_population(self, pop: List) -> None:
        """
        Vectorizes addition of a generation. Usually used to define first
        generation in population

        Args:
            pop (List): list of Blobs to add to population
        """
        pop.sort(key=lambda x: x.name)
        pop_arr = np.array(pop)
        self.population.append(pop_arr)
        types, _ = get_pivot_indices(pop)

    def interact(self) -> None:
        """
        Enables most recent population to interact with environmental
        parameters.
        """
        # Get relevant attrs. For this Environment, survival, reproduction,
        # and mutation
        surv_attrs = get_generation_attributes(
            self.population[-1], "survival_prob"
        )
        repr_attrs = get_generation_attributes(
            self.population[-1], "reproduction_prob"
        )

        # Kill off some portion of population based off Blob survival attrs
        surv_pop, surv_mask = apply_mask_to_population(
            self.population[-1], surv_attrs
        )

        # Surviving population reproduced based off Blob reproduction attrs
        repr_attrs = repr_attrs[surv_mask]
        repr_pop, _ = apply_mask_to_population(surv_pop, repr_attrs)

        # Each blob will reproduce, with a chance of mutation
        new_blobs = [b.reproduce() for b in repr_pop]

        # Save instances that survived and new instances, add to population
        self.population.append(merge_populations(surv_pop, new_blobs))

    def show_one_generation(self, generation_idx: int) -> None:
        """
        Plots graphical display of environment and existing blobs in a single
        generation

        Args:
            generation_idx (int): idx of generation within population
        """
        current_gen = self.population[generation_idx]
        types = list(set([b.name for b in current_gen]))

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=FIG_DIMENSIONS)
        for idx, t in enumerate(types):
            t_idx = [
                i for i in range(len(current_gen)) if current_gen[i].name == t
            ]
            t_population = [current_gen[i] for i in t_idx]

            ax.scatter(
                x=[s.x * self.dimension for s in t_population],
                y=[s.y * self.dimension for s in t_population],
                color=t_population[0].color,
                s=BLOB_DISPLAY_SIZE,
                label=f"{types[idx]} - {len(t_population)}",
            )

        plt.title(
            f"Generation {generation_idx}:{len(self.population[generation_idx])} blobs",
            fontsize=20,
        )
        ax.legend(loc="upper right", frameon=True)
        ax.set_xlim([0, self.dimension])
        ax.set_ylim([0, self.dimension])

        plt.show()

    def show_all_generations(self, delay=0.5) -> None:
        """
        Generates slideshow of blobs as they move through generations. Saves
        each generation image as a .SVG and displays each SVG individually

        Args:
            delay (float): time delay between displaying each generation
        """
        for gen_idx, gen in enumerate(self.population):
            self.show_one_generation(gen_idx)
            sleep(delay)
            clear_output(wait=True)

    def plot_growth(self, log=True) -> None:
        """
        Plots growth of populations across generations

        Args:
            log (bool): True/False to plot y-axis (Count) in log scale
        """
        data, colors = get_population_at_each_generation(self.population)

        fig2, ax2 = plt.subplots(nrows=1, ncols=1, figsize=FIG_DIMENSIONS)
        for t in data:
            ax2.fill_between(
                range(len(data[t])),
                0,
                data[t],
                color=colors[t],
                label=t,
                alpha=0.5,
            )
        if log:
            ax2.set_yscale("log")

        plt.title(f"Growth of blob populations", fontsize=20)
        ax2.set_xlabel("Generation", fontsize=16)
        ax2.set_ylabel("Number blobs", fontsize=16)
        ax2.legend(loc="upper right", frameon=True)
        ax2.xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.show()


class EnvironmentWithFood(BaseEnvironment):
    """
    Environment w/ food resources that need to be competed for. Blobs in this
    environment can move and must collect food to survive

    Attributes:
        food (int): number of food to spawn each epoch
    """

    def __init__(self, food: int) -> None:
        """See parent docstring"""
        super().__init__()
        self.food: int = food
        self.food_coords = [
            [(random.random(), random.random()) for f in range(self.food)]
        ]

    def spawn_food(self):
        """Spawn food at randomly distributed coordinates"""
        gen_food_coords = []
        for f in range(self.food):
            f_coord = (random.random(), random.random())
            gen_food_coords.append(f_coord)
        self.food_coords.append(gen_food_coords)

    def interact(self):
        """
        Spawns food, then blobs move towards food. Those who eat food
        survive, those who don't roll the dice for survival
        """
        self.spawn_food()

        # Determine what blobs survive based off ability to reach food
        survived = []
        for b in self.population[-1]:
            closest_food, dist = find_closest_coord(
                (b.x, b.y), self.food_coords[-1]
            )
            b.move(closest_food)
            new_dist = calculate_distance_to_coord((b.x, b.y), closest_food)
            try_to_eat(b, new_dist, survived)

        # Surviving population rolls dice to reproduce
        repr_attrs = get_generation_attributes(survived, "reproduction_prob")
        repr_pop, repr_mask = apply_mask_to_population(survived, repr_attrs)

        new_blobs = [b.reproduce() for b in repr_pop]

        # Save instances that survived and new instances, add to population
        self.population.append(merge_populations(survived, new_blobs))

    def show_one_generation(self, generation_idx: int) -> None:
        """
        Plots graphical display of environment and existing blobs in a single
        generation

        Args:
            generation_idx (int): idx of generation within population
        """
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=FIG_DIMENSIONS)

        # Plot location of food
        gen_food = self.food_coords[generation_idx]
        ax.scatter(
            [f[0] * self.dimension for f in gen_food],
            [f[1] * self.dimension for f in gen_food],
            color="orange",
            s=FOOD_DISPLAY_SIZE,
            label="Food",
        )

        # Plot location of blobs. Note that this is functionally equivalent
        # to the BaseBlob implementation
        current_gen = self.population[generation_idx]
        types = list(set([b.name for b in current_gen]))
        for idx, t in enumerate(types):
            t_idx = [
                i for i in range(len(current_gen)) if current_gen[i].name == t
            ]
            t_population = [current_gen[i] for i in t_idx]
            ax.scatter(
                x=[s.x * self.dimension for s in t_population],
                y=[s.y * self.dimension for s in t_population],
                color=t_population[0].color,
                s=BLOB_DISPLAY_SIZE,
                label=f"{types[idx]} - {len(t_population)}",
            )

        plt.title(
            f"Generation {generation_idx}:{len(self.population[generation_idx])} blobs"
            f"\n{self.food} pieces of food",
            fontsize=20,
        )
        ax.legend(loc="upper right", frameon=True)
        ax.set_xlim([0, self.dimension])
        ax.set_ylim([0, self.dimension])

        plt.show()


class InteractiveEnvironment(EnvironmentWithFood):
    """
    Environment where blobs can interact with each other. Blobs in this
    environment can move and must collect food to survive

    Attributes:
        food (int): number of food to spawn each epoch
    """

    def __init__(self, food: int) -> None:
        """See parent docstring"""
        super().__init__(food)
        self.food = food

    def interact(self) -> None:
        """
        Spawns food, then blobs move towards food. QuickBlobs eat first, then
        rest of blobs interact to decide who eats
        """
        self.spawn_food()

        survived = []
        remaining_food = self.food_coords[-1]
        eaten_food = []
        for b in self.population[-1]:
            closest_food, dist = find_closest_coord(
                (b.x, b.y), self.food_coords[-1]
            )
            # All blobs move towards food simultaneously
            b.move(closest_food)
            # QuickBlobs eat first
            if b.name == "QuickBlob":
                new_dist = calculate_distance_to_coord(
                    (b.x, b.y), closest_food
                )
                successfully_ate = try_to_eat(b, new_dist, survived)
                if successfully_ate:
                    eaten_food.append(closest_food)

        # Remove food that's already been eaten by QuickBlobs
        for f in set(eaten_food):
            if f in remaining_food:
                remaining_food.remove(f)

        # Now rest of blobs interact
        for b in self.population[-1]:
            if b.name != "QuickBlob":
                closest_food, dist = find_closest_coord(
                    (b.x, b.y), remaining_food
                )
                nearby_blobs = find_blobs_in_reach(b, self.population[-1])
                try:
                    b.interact_with_surroundings(nearby_blobs)
                except AttributeError:
                    # Blobs not inheriting from BaseInteractingBlob will not
                    # contain this method, so no interaction from them
                    pass
                # If blob is sufficiently weakened from attack, can't eat even
                # if within range
                if b.survival_prob > 0:
                    try_to_eat(b, dist, survived)

        # Surviving population rolls dice to reproduce
        repr_attrs = get_generation_attributes(survived, "reproduction_prob")
        repr_pop, repr_mask = apply_mask_to_population(survived, repr_attrs)

        new_blobs = [b.reproduce() for b in repr_pop]
        self.population.append(merge_populations(survived, new_blobs))
