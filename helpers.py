"""Repository of small helper functions used across project. In general,
this project obeys the convention that functions that modify an objects
internal state wil be kept as class methods and the rest here"""
from typing import Union, List
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
        np.where(names[:-1] != names[1:])[0], len(population) - 1
    )
    return (names, pivot_idx)


def apply_mask_to_population(
    population: Union[List, np.ndarray], attributes: np.ndarray
) -> tuple:
    """
    Applies mask to population based off randomly generated array vs
    population attributes

    Args:
        population Union(List, np.ndarray): population to mask
        attributes (np.ndarray): attributes of population
    Returns:
        Tuple: masked population and mask
    """
    if isinstance(population, List):
        population = np.array(population)

    event_prob = np.random.uniform(low=0.1, high=1.0, size=population.shape)
    mask = event_prob <= attributes
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
    if len(population) == 0:
        # If population is empty, all blobs are dead and thus no attrs to return
        return np.array([])

    # Get indexes of pivot points in population
    names, pivots = get_pivot_indices(population)

    attr_values = []
    # For each blob type, save attributes in lists
    for i, idx in np.ndenumerate(pivots):
        if i[0] == 0:
            attr_values.extend(
                [getattr(population[idx], attribute)] * (idx + 1)
            )
        else:
            attr_values.extend(
                [getattr(population[idx], attribute)]
                * (idx - pivots[i[0] - 1])
            )
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
    """
    if len(population) == 0:
        #If population is empty, all blobs are dead and thus no attrs to return
        return ({}, {})
    """
    # Get all blob instances across all generations and note unique
    # instances
    all_blobs = list(np.concatenate(np.array(population, dtype=object)))
    all_blobs.sort(key=lambda x: x.name)
    all_blob_types = set([x.name for x in all_blobs])
    type_dict = {t: [] for t in all_blob_types}
    color_maps = {t: None for t in all_blob_types}

    # Iterate through generations and count each type of blob
    for g, gen in enumerate(population):
        if len(gen) == 0:
            # If generation has died off, append 0 to all counters
            for t in type_dict:
                type_dict[t].append(0)
            continue
        type_tracker = list(all_blob_types)
        # If only one type of blob, don't iterate through everything and just
        # use attrs of that single blob
        if len(type_tracker) == 1:
            rep_blob = type_tracker[0]
            if len(gen) == 0:
                # If entire generation is dead, don't save color attr since
                # won't be displayed
                type_dict[rep_blob].append(0)
            else:
                type_dict[rep_blob].append(len(gen))
                color_maps[rep_blob] = gen[0].color
        else:
            names, pivots = get_pivot_indices(gen)
            # Since population is sorted, instead of iterating through each
            # instance and noting the type, only note indices corresponding
            # to type changes and infer the types from the changes
            for i, idx in np.ndenumerate(pivots):

                type_blob = gen[idx - 1].name
                color_maps[type_blob] = gen[idx - 1].color
                if i[0] == 0:
                    count = idx + 1
                else:
                    count = idx - pivots[i[0] - 1]
                type_dict[type_blob].append(count)
                if type_blob in type_tracker:
                    type_tracker.remove(type_blob)
            if type_tracker:
                # If blob type absent in generation but present in other
                # generations
                for t in type_tracker:
                    type_dict[t].append(0)
    return (type_dict, color_maps)


def merge_populations(
    pop1: Union[List, np.ndarray], pop2: Union[List, np.ndarray]
) -> np.ndarray:
    """
    Combines and sorts two populations into one

    Args:
        pop1 (Union[List, np.ndarray])
        pop2 (Union[List, np.ndarray])
    Returns:
        (np.ndarray)
    """
    if not isinstance(pop1, np.ndarray):
        pop1 = np.array(pop1)
    if not isinstance(pop2, np.ndarray):
        pop2 = np.array(pop2)
    merged = list(np.append(pop1, pop2))
    merged.sort(key=lambda x: x.name)
    return np.array(merged)


def find_closest_food(blob, food_list: List) -> tuple:
    """
    Finds closest food relative to Blob's current position

    Args:
        blob (BaseBlob): blob to base distance off
        food_list (List): List of all available food coordinates
    Returns:
        (tuple)
    """
    min_dist = 1000000
    closest_food_coord = None

    for coord in food_list:
        dist = calculate_distance_to_food(blob, coord)
        if dist < min_dist:
            closest_food_coord = coord
            min_dist = dist
    return closest_food_coord, min_dist


def calculate_distance_to_food(blob, food_coord: tuple) -> float:
    """
    Calculates distance from blob to food

    Args:
        blob (Blob)
        food_coord (tuple): coordinate of food in (x,y)
    Returns:
        (float): distance to food
    """
    return ((food_coord[0] - blob.x) ** 2 + (food_coord[1] - blob.y) ** 2) ** (
        1 / 2
    )
