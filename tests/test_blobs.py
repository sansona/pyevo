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
