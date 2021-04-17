"""Test suite for environment objects"""
from typing import List
import pytest
from environment import *
from blobs import BaseBlob, MutatedBaseBlob

@pytest.fixture
def starting_population() -> List:
    """
    Sets up a generic population

    Returns:
        (List)
    """
    return [BaseBlob(1.0, 1.0, 1.0), MutatedBaseBlob(1.0, 1.0, 1.0)]

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
    b.spawn_population([BaseBlob(1.0, 1.0, 1.0), MutatedBaseBlob(1.0, 1.0, 1.0)])
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

def test_show_one_gen_first_gen_no_errors(one_gen_env, monkeypatch):
    """Tests that show function on first generation doesn't throw any runtime
    errors"""
    #pytest fixture to close matplotlib figure on display
    monkeypatch.setattr(plt, 'show', lambda: None)
    one_gen_env.show_one_generation(0)

def test_show_one_gen_last_gen_no_errors(one_gen_env, monkeypatch):
    """Tests that show function on last generation doesn't throw any runtime
    errors"""
    monkeypatch.setattr(plt, 'show', lambda: None)
    one_gen_env.show_one_generation(-1)

def test_plot_growth_no_errors(one_gen_env, starting_population, monkeypatch):
    """Tests that plot growth doesn't throw any runtime errors"""
    one_gen_env.spawn_population(starting_population)
    monkeypatch.setattr(plt, 'show', lambda: None)
    one_gen_env.plot_growth()

def test_show_all_generations_no_errors(one_gen_env, starting_population, monkeypatch):
    """Tests show_all_generations shows no runtime errors"""
    one_gen_env.spawn_population(starting_population)
    monkeypatch.setattr(plt, 'show', lambda: None)
    one_gen_env.show_all_generations()
