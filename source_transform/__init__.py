# -*- coding: utf-8 -*-
from .discovery import find_transforms
from .transform import BaseTransform


def register():
    find_transforms()


__all__ = ['register', 'BaseTransform']
