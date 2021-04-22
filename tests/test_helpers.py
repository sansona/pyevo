"""Test suite for various helper functions"""
import numpy as np
import pytest
from blobs import *
from helpers import *


@pytest.fixture
def dummy_population() -> np.ndarray:
    """
    Setup fixture for generic, but varied, population

    Returns:
        (np.ndarray)
    """
    b = BaseBlob()
    b.set_probs(0.5, 1.0, 1.0)
    m = MutatedBaseBlob()
    m.set_probs(0.3, 1.0, 1.0)
    b2 = BaseBlob()
    b2.set_probs(0.5, 0.5, 0.5)
    all_b = [[b for x in range(2)] + [m for y in range(2)], [b2]]
    return np.array(all_b, dtype=object)


@pytest.fixture
def dummy_attributes() -> np.ndarray:
    """
    Setup fixture for generic blob attributes. To ensure consistent testing,
    test attributes all set to 0.01

    Returns:
        (np.ndarray)
    """
    return np.array([0.01, 0.01, 0.01, 0.01])


def test_get_pivot_indices_parses_correct_blob_types(dummy_population):
    """Tests that get_pivot_indices gets correct blob types"""
    indices = get_pivot_indices(dummy_population[0])
    assert list(indices[0]) == [
        "BaseBlob",
        "BaseBlob",
        "MutatedBaseBlob",
        "MutatedBaseBlob",
    ]


def test_get_pivot_indices_splits_correct_indices(dummy_population):
    """Tests that get_pivot_indices outputs correct indices of blob type
    changes"""
    indices = get_pivot_indices(dummy_population[0])
    assert list(indices[1]) == [1, 3]


def test_apply_mask_properly_applies_mask(dummy_population, dummy_attributes):
    """Tests that apply_mask_to_population properly masks population on
    attribute values"""
    masked_pop, mask = apply_mask_to_population(
        np.array(dummy_population[0]), dummy_attributes
    )
    assert len(masked_pop) == 0  # Since set attributes to 0, none above mask


def test_get_generation_attributes(dummy_population):
    """Tests that get_generation_attributes retrieves correct attribute values"""
    attrs = get_generation_attributes(dummy_population[0], "survival_prob")
    assert list(attrs) == [0.5, 0.5, 0.3, 0.3]


def test_get_population_at_each_gen_retrieves_proper_counts(dummy_population):
    """Tests that get_population_at_each_generation retrieves proper count
    of blob types across entire population"""
    type_counts, _ = get_population_at_each_generation(dummy_population)
    assert type_counts == {"BaseBlob": [2, 1], "MutatedBaseBlob": [2, 0]}


def test_merge_populations_properly_sorts(dummy_population):
    """Tests that merge_populations properly returns a sorted and merged
    array"""
    merged = merge_populations(dummy_population[0], dummy_population[1])
    merged_types = [b.name for b in merged]
    assert merged_types == (["BaseBlob"] * 3 + ["MutatedBaseBlob"] * 2)


def test_get_population_at_each_gen_retrieves_proper_colors(dummy_population):
    """Tests that get_population_at_each_generation retrieves proper color
    mappings of blob types across entire population"""
    _, color_maps = get_population_at_each_generation(dummy_population)
    assert color_maps == {"BaseBlob": "blue", "MutatedBaseBlob": "red"}


def test_find_closest_food():
    """Tests that find_closest_food function properly identifies the food that
    is closest"""
    # Create dummy blob with set coordinates
    b = PerfectTestBlob()
    b.x, b.y = 0.0, 0.0

    food_list = [(0.01, 0.01), (1.0, 1.0), (1.0, 1.0)]
    closest, _ = find_closest_food(b, food_list)
    assert closest == (0.01, 0.01)


def test_calculate_dist_to_food():
    """Tests that calculate_distance_to_food calculates the proper distance"""
    b = PerfectTestBlob()
    b.x, b.y = 0.0, 0.0
    food_pos = (1.0, 1.0)
    assert calculate_distance_to_food(b, food_pos) == 2.0 ** (1 / 2)
