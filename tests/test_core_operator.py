import pytest

from pandas.testing import assert_frame_equal
from datar.all import *

def test_neg():
    df = tibble(x=[1, 2])
    out = df >> mutate(y=-f.x)
    assert_frame_equal(out, tibble(x=[1,2], y=[-1,-2]))

def test_or_():
    df = tibble(x=1, y=2, z=3)
    out = df >> select(c(f.x, f.y) | [f.y, f.z])
    assert_frame_equal(out, tibble(x=1,y=2,z=3))

def test_ne():
    df = tibble(x=[1,2], y=[1,3])
    # out = mutate(df, z=f.x!=f.y)
    # assert_frame_equal(out, tibble(x=[1,2], y=[1,3], z=[False, True]))
    out = mutate(df, z=f.x.size != f.y.size)
    assert_frame_equal(out, tibble(x=[1,2], y=[1,3], z=[False, False]))
