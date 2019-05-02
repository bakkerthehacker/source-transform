# -*- coding: utf-8 -*-
from inspect import isabstract
from inspect import isclass

from six.moves import filter
from six.moves import filterfalse

from .transform import BaseTransform


def all_subclasses(cls):
    return set(cls.__subclasses__()) | {
        sub_recursive
        for sub in cls.__subclasses__()
        for sub_recursive in all_subclasses(sub)
    }


def find_transforms():
    transforms = all_subclasses(BaseTransform)

    transforms = filter(isclass, transforms)
    transforms = filterfalse(isabstract, transforms)

    return set(transforms)
