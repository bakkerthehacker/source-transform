# -*- coding: utf-8 -*-
from inspect import isabstract
from inspect import isclass

from toolz.functoolz import complement

from .transform import BaseTransform


def all_subclasses(cls):
    return set(cls.__subclasses__()) | {
        sub_recursive
        for sub in cls.__subclasses__()
        for sub_recursive in all_subclasses(sub)
    }


def find_transforms():
    all_transforms = all_subclasses(BaseTransform)

    all_transforms = filter(isclass, all_transforms)
    all_transforms = filter(complement(isabstract), all_transforms)

    return set(all_transforms)
