"""Test suite for blobs"""
import pytest
from blobs import *


def test_baseblob_empty_init():
    """Tests that initializing the BaseBlob class with missing vars raise
    TypeError"""
    with pytest.raises(TypeError):
        a = BaseBlob()


def test_baseblob_correct_init():
    """Tests that initializing BaseBlob class will not raise any errors"""
    a = BaseBlob(1.0, 1.0, 1.0)


def test_baseblob_reproduce_guaranteed_mutation():
    """Tests that a blob with a guaranteed mutation will mutate to correct
    class"""
    a = BaseBlob(1.0, 1.0, 1.0)
    assert a.reproduce().name == "MutatedBaseBlob"


def test_baseblob_reproduce_no_mutation():
    """Tests that a blob with no mutation prob will reproduce to same class"""
    a = BaseBlob(1.0, 1.0, 0.0)
    assert a.reproduce().name == "BaseBlob"


def test_baseblob_move():
    """Tests that BaseBlob move function moves in correct increment"""
    a = BaseBlob(1.0, 1.0, 0.0)
    starting_pos = (a.x, a.y)
    a.move((1.0, 1.0))
    ending_pos = (a.x, a.y)
    changes = (
        ending_pos[0] - starting_pos[0],
        ending_pos[1] - starting_pos[1],
    )

    # Since comparing floats, use a min. epsilon to determine floating point
    # equality
    assert (abs(changes[0]) - a.step < 0.001) and (
        abs(changes[1]) - a.step < 0.001
    )


def test_foodsense_blob_move_towards_food():
    """Tests that blobs with food sense reduce distance between current pos
    and food location via. move"""
    pass
