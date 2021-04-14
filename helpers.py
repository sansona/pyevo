"""Repository of small helper functions used across project. In general,
this project obeys the convention that functions that modify an objects
internal state wil be kept as class methods and the rest here"""
from typing import List
import numpy as np

def get_pivot_indices(population: List) -> tuple:
    """
    Outputs name of blob types present and the indices corresponding to each
    blob type

    Args:
        population (List): population to get indices for
    Returns:
        Tuple: np.ndarrays of unique blob types and indices of pivots
"""
    names = np.array([x.name for x in population])
    pivot_idx = np.append(
        np.where(names[:-1] != names[1:])[0], len(population)-1)
    return (names, pivot_idx)

def apply_mask_to_population(
        population: np.ndarray, attributes: np.ndarray) -> tuple:
    """
    Applies mask to population based off randomly generated array vs
    population attributes

    Args:
        population (np.ndarray): population to mask
        attributes (np.ndarray): attributes of population
    Returns:
        Tuple: masked population and mask
    """
    event_prob = np.random.uniform(
            low=0.0, high=1.0, size=pop.shape)
    mask = event_prob < attributes
    return (population[mask], mask)

def get_generation_attributes(population: List, attribute: str) -> np.ndarray:
    """
    Gets attributes of population

    Args:
        population (List): population to get attributes for
        attribute (str): name of attribute to get. Attribute must be a class
            variable for Blob type
    returns:
        np.ndarray: attributes of population
    """
    #Get indexes of pivot points in population
    names, pivots = get_pivot_indices(population)

    attr_values = []
    #For each blob type, save attributes in lists
    for i, idx in np.ndenumerate(pivots):
        if i[0] == 0:
            blah = population[idx].__dict__.keys()
            attr_values.extend([getattr(population[idx], attr)]*(idx+1))
        else:
            attr_values.extend(
                [getattr(population[idx], attr)]*(idx - pivots[i[0]-1]))
    return np.array(attr_values)

def get_population_at_each_generation(population: np.ndarray) -> tuple:
    """
    Parses through entire population and counts up number of blobs of each
    type in each generation

    Args:
        population (np.ndarray): entire population, including all generations
    Returns:
        Tuple: Dicts with count of each type across generations and color map
            mapping each blob type to a color
    """
    #Get all blob instances across all generations and note unique
    #instances
    all_blobs = list(np.concatenate(population.ravel()))
    all_blobs.sort(key=lambda x: x.name)
    all_blob_types = set([x.name for x in all_blobs])
    type_dict = {t: [] for t in all_blob_types}
    color_maps = {t: None for t in all_blob_types}

    #Iterate through generations and count each type of blob
    for g, gen in enumerate(population):
        type_tracker = list(all_blob_types)
        names, pivots = get_pivot_indices(gen)
        #Since population is sorted, instead of iterating through each
        #instance and noting the type, only note indices corresponding
        #to type changes and infer the types from the changes
        for i, idx in np.ndenumerate(pivots):
            type_blob = gen[idx-1].name
            color_maps[type_blob] = gen[idx-1].color
            if i[0] == 0:
                count = idx + 1
            else:
                count = idx - pivots[i[0]-1]
            type_dict[type_blob].append(count)
            if type_blob in type_tracker:
                type_tracker.remove(type_blob)
        if type_tracker:
            #If blob type absent in generation but present in other
            #generations
            for t in type_tracker:
                type_dict[t].append(0)
    return (type_dict, color_maps)
