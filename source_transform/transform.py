# -*- coding: utf-8 -*-
from abc import ABCMeta

from six import with_metaclass


class BaseTransform(with_metaclass(ABCMeta, object)):

    def trigger(self):
        pass

    def transform(self):
        pass
