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


def test_find_closest_coord():
    """Tests that find_closest_coord function properly identifies the food that
    is closest"""
    # Create dummy blob with set coordinates
    b = PerfectTestBlob()
    b.x, b.y = 0.0, 0.0

    food_list = [(0.01, 0.01), (1.0, 1.0), (1.0, 1.0)]
    closest, _ = find_closest_coord((b.x, b.y), food_list)
    assert closest == (0.01, 0.01)


def test_calculate_dist_to_food():
    """Tests that calculate_distance_to_coord calculates the proper distance"""
    b = PerfectTestBlob()
    b.x, b.y = 0.0, 0.0
    food_pos = (1.0, 1.0)
    assert calculate_distance_to_coord((b.x, b.y), food_pos) == 2.0 ** (1 / 2)


def test_determine_number_survivors_of_type_properly_counts():
    """Tests that determine_number_survivors_of_type returns proper value for if
    blobtype present"""
    pop = [[PerfectTestBlob() for x in range(5)] + [BaseBlob()]]
    assert determine_number_survivors_of_type("PerfectTestBlob", pop) == 5
    assert determine_number_survivors_of_type("BaseBlob", pop) == 1
    assert determine_number_survivors_of_type("MiscBlob", pop) == 0


def test_find_blobs_in_reach_accurately_finds_blobs():
    """Test that find_blobs_in_reach will find the right number of blobs in
    reach and append the proper blob IDs"""
    ref_blob = BaseBlob()
    ref_blob.x, ref_blob.y = 0.0, 0.0
    ref_blob.size = 0.2

    in_reach_blobs = [BaseBlob() for b in range(5)]
    for b in in_reach_blobs:
        b.x, b.y = 0.1, 0.1

    out_of_reach_blobs = [BaseBlob() for c in range(10)]
    for c in out_of_reach_blobs:
        c.x, c.y = 0.9, 0.9

    found_blobs = find_blobs_in_reach(
        ref_blob, in_reach_blobs + out_of_reach_blobs
    )
    assert len(found_blobs) == 5
    assert set([(f.x, f.y) for f in found_blobs]) == {(0.1, 0.1)}


def test_try_to_eat():
    """Tests that try_to_eat function results in eating if food is within
    range and not if outside"""
    ref_blob = BaseBlob()
    ref_blob.size = 0.1

    assert try_to_eat(ref_blob, 0.05, [])
    assert not try_to_eat(ref_blob, 0.2, [])

def test_set_attrs_of_population_missing_attrs(dummy_population):
    """Test that set_attrs_of_population will throw ValueError if no
    attrs are passed"""
    with pytest.raises(ValueError):
        set_attrs_of_population(dummy_population[0])

def test_set_attrs_of_population_one_attr(dummy_population):
    """Test that set_attrs_of_population with one attr passed will set
    attrs in population to correct value"""
    s = 0.42
    changed_pop = set_attrs_of_population(dummy_population[0], s=s)
    all_survival_attrs = [b.survival_prob for b in changed_pop]
    assert set(all_survival_attrs) == {s}

def test_set_attrs_of_population_three_attr(dummy_population):
    """Test that set_attrs_of_population with three attrs passed will set
    attrs in population to correct value"""
    srm = (0.42, 0.9, 0.5)
    changed_pop = set_attrs_of_population(dummy_population[0],
            s=srm[0], r=srm[1], m=srm[2])
    all_attrs = [(b.survival_prob, b.reproduction_prob, b.mutation_prob)
            for b in changed_pop]
    assert set(all_attrs) == {srm}

def test_determine_most_prevalent_blob(dummy_population):
    """Tests that `determine_most_prevalent_blob` accurately finds the blob
    that's most prevalent in final generation"""
    pass
