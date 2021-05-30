"""Test suite for environment objects"""
from typing import List
import pytest
from environment import *
from blobs import *


@pytest.fixture
def starting_population() -> List:
    """
    Sets up a generic population

    Returns:
        (List)
    """
    b = PerfectTestBlob()
    m = MutatedBaseBlob()
    m.set_probs(1.0, 1.0, 1.0)
    return [b, m]


@pytest.fixture
def empty_env():
    """
    Creates empty BaseEnvironment

    Returns:
        (BaseEnvironment)
    """
    return BaseEnvironment()


@pytest.fixture
def one_gen_env():
    """
    Creates BaseEnvironment with single starting population

    Returns:
        (BaseEnvironment)
    """
    b = BaseEnvironment()
    base_pop = [BaseBlob(), MutatedBaseBlob()]
    for p in base_pop:
        p.set_probs(1.0, 1.0, 1.0)
    b.spawn_population(base_pop)
    return b


def test_spawn_population(empty_env, starting_population):
    """Tests that spawn population appends a population properly"""
    empty_env.spawn_population(starting_population)
    assert len(empty_env.population) == 1


def test_spawn_adds_correct_population(one_gen_env, starting_population):
    """Tests that adding a new population to an existing environment
    correctly appends new generation in same order"""
    one_gen_env.spawn_population(starting_population)
    assert list(one_gen_env.population[-1]) == starting_population


def test_interact_no_population(empty_env):
    """Tests that interact throws an IndexError when no populations are
    present"""
    with pytest.raises(IndexError):
        empty_env.interact()


def test_interact_spawns_new_population(one_gen_env, starting_population):
    """Tests that adding a new population to an existing environment
    correctly appends one new generation"""
    one_gen_env.spawn_population(starting_population)
    assert len(one_gen_env.population) == 2


def test_interact_throws_no_errors(one_gen_env):
    """Tests that running interact in a loop adds correct number of new
    generations to population"""
    num_epochs = 3
    for i in range(num_epochs):
        one_gen_env.interact()
    # +1 because env comes with 1 seed generation
    assert len(one_gen_env.population) == (num_epochs + 1)


def test_show_one_gen_first_gen_no_errors(one_gen_env, monkeypatch):
    """Tests that show function on first generation doesn't throw any runtime
    errors"""
    # pytest fixture to close matplotlib figure on display
    monkeypatch.setattr(plt, "show", lambda: None)
    one_gen_env.show_one_generation(0)


def test_show_one_gen_last_gen_no_errors(one_gen_env, monkeypatch):
    """Tests that show function on last generation doesn't throw any runtime
    errors"""
    monkeypatch.setattr(plt, "show", lambda: None)
    one_gen_env.show_one_generation(-1)


def test_plot_growth_no_errors(one_gen_env, starting_population, monkeypatch):
    """Tests that plot growth doesn't throw any runtime errors"""
    one_gen_env.spawn_population(starting_population)
    monkeypatch.setattr(plt, "show", lambda: None)
    one_gen_env.plot_growth()


def test_show_all_generations_no_errors(
    one_gen_env, starting_population, monkeypatch
):
    """Tests show_all_generations shows no runtime errors"""
    one_gen_env.spawn_population(starting_population)
    monkeypatch.setattr(plt, "show", lambda: None)
    one_gen_env.show_all_generations()


def test_foodenv_interact_adds_food_and_population():
    """Tests that foodenv interact spawns food and new population. Note that I
    am intentionally testing for both food and population appending since
    population appending is already explicitly tested for earlier"""
    e = EnvironmentWithFood(food=3)
    e.spawn_population([BaseBlob()])
    e.interact()
    # spawn_population adds an extra generation which is why foodenv inits with
    # food pre-populated
    assert (len(e.food_coords) == 2) and (len(e.population) == 2)


def test_foodenv_plots(monkeypatch):
    """Tests that foodenv plotting functions don't throw errors. Note that I
    intentionally chose to wrap multiple tests into a single once since
    the individual plotting functions are already tested previously"""
    # Setup dummy environment with interacted blobs
    e = EnvironmentWithFood(food=3)
    pop = [BaseBlob()] + [HungryBlob() for z in range(3)]
    for p in pop:
        p.set_probs(1.0, 1.0, 1.0)
    e.spawn_population(pop)

    for i in range(3):
        e.interact()
    # Plot all available plotting functions
    monkeypatch.setattr(plt, "show", lambda: None)
    e.show_one_generation(-1)
    e.show_all_generations()
    e.plot_growth()
