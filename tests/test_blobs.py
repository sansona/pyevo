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
    assert a.reproduce().name == 'MutatedBaseBlob'

def test_baseblob_reproduce_no_mutation():
    """Tests that a blob with no mutation prob will reproduce to same class"""
    a = BaseBlob(1.0, 1.0, 0.0)
    assert a.reproduce().name == 'BaseBlob'
