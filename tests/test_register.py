# -*- coding: utf-8 -*-
import sys


def test_register():
    assert any(
        'TransformFinderLoader' in repr(finder_loader)
        for finder_loader in sys.meta_path
    )
