# -*- coding: utf-8 -*-
from abc import ABCMeta
from abc import abstractmethod

from six import with_metaclass


class BaseTransform(with_metaclass(ABCMeta, object)):

    @staticmethod
    @abstractmethod
    def trigger(**kwargs):
        return False

    @staticmethod
    @abstractmethod
    def transform(data, **kwargs):
        return data
