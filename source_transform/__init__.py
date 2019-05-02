# -*- coding: utf-8 -*-
from .discovery import find_transforms
from .meta_path import setup_meta_path
from .transform import BaseTransform


def register():
    transforms = find_transforms()
    setup_meta_path(transforms)


__all__ = ['register', 'BaseTransform']
