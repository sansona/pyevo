"""Repository for all Environment related classes"""
from typing import List, Dict
import random
import copy
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from blobs import BaseBlob
from settings import ENVIRONMENT_DIMENSIONS, BLOB_DISPLAY_SIZE
from helpers import (get_pivot_indices,
        get_generation_attributes,
        get_population_at_each_generation,
        apply_mask_to_population)

sns.set()

class BaseEnvironment:
    """
    Base class for defining boundary conditions for blobs to interact
    within

    Attributes:
        dimension (int): dimension of environment for Blobs to interact in.
            Note that dimension will be broadcast to a square environment
        population (List): container of all Blobs that exist in Environment
    """
    def __init__(self ) -> None:
        """
        Inits BaseEnvironment

        Args:
            (None)
        Returns:
            (None)
        """
        self.dimension: int  = ENVIRONMENT_DIMENSIONS
        self.population: List = []

    def spawn_population(self, pop: List) -> None:
        """
        Vectorizes addition of a generation. Usually used to define first
        generation in population

        Args:
            pop (List): list of Blobs to add to population
        Returns:
            (None)
        """
        pop.sort(key=lambda x: x.name)
        pop_arr = np.array(pop)
        self.population.append(pop_arr)

    def interact(self) -> None:
        """
        Enables most recent population to interact with environmental
        parameters.

        Args:
            (None)
        Returns:
            (None)
        """
        #Get relevant attrs
        surv_attrs = get_generation_attributes(
                self.population[-1], 'survival_prob')
        repr_attrs = get_generation_attributes(
                self.population[-1], 'reproduction_prob')

        #Kill off some portion of population based off Blob survival attrs
        surv_pop, surv_mask = apply_mask_to_population(self.population[-1], surv_attrs)

        #Surviving population reproduced based off Blob reproduction attrs
        repr_attrs = repr_attrs[surv_mask]
        pop_produced, _ = apply_mask_to_population(surv_pop, repr_attrs)
        #Each new blob gets new coordinates for visualization
        mod_pop = []
        for new_blob in pop_produced:
            #need to set new attrs at instance level, therefore deepcopy
            new_blob = copy.deepcopy(new_blob)
            new_blob.x, new_blob.y = random.random(), random.random()
            mod_pop.append(new_blob)

        #Save instances that survived and new instances, add to population
        next_gen = list(np.append(surv_pop, mod_pop))
        next_gen.sort(key=lambda x: x.name)
        next_gen = np.array(next_gen)
        self.population.append(next_gen)

    def show(self, generation: int, close=False) -> None:
        """
        Plots graphical display of environment and existing blobs

        Args:
            generation (int): idx of generation within population
            close (bool): to close display after making. Used in tests
        Returns:
            (None)
        """
        current_gen = self.population[generation]
        types = list(set([b.name for b in current_gen]))

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12,12))
        for idx, t in enumerate(types):
            t_idx = [i for i in range(len(
                current_gen)) if current_gen[i].name == t]
            t_population = [current_gen[i] for i in t_idx]

            ax.scatter(
                x=[s.x*self.dimension for s in t_population],
                y=[s.y*self.dimension for s in t_population],
                color=t_population[0].color,
                s=BLOB_DISPLAY_SIZE,
                label=types[idx])

        plt.title(
            f"Generation {generation}:{len(self.population[generation])} blobs",
            fontsize=20)
        ax.legend(loc='upper right', frameon=True)
        ax.set_xlim([0, self.dimension])
        ax.set_ylim([0, self.dimension])

        plt.show()
        if close:
            plt.close()

    def plot_growth(self, close=False, log=True) -> None:
        """
        Plots growth of populations across generations

        Args:
            close (bool): to close display after making. Used in tests
            log (bool): True/False to plot y-axis (Count) in log scale
        Returns:
            (None)
        """
        data, colors = get_population_at_each_generation(self.population)

        fig2, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(12,12))
        for t in data:
            ax2.fill_between(
                    range(len(data[t])), 0, data[t], color=colors[t], label=t, alpha=0.5)
        if log:
            ax2.set_yscale('log')

        plt.title(f"Growth of blob populations", fontsize=20)
        ax2.set_xlabel('Generation', fontsize=16)
        ax2.set_ylabel('Number blobs', fontsize=16)
        ax2.legend(loc='upper right', frameon=True)

        plt.show()
        if close:
            plt.close()
