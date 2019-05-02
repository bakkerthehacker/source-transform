# -*- coding: utf-8 -*-
from six import PY2


if PY2:
    from .meta_path_py2 import setup_meta_path
else:
    from .meta_path_py3 import setup_meta_path


__all__ = ['setup_meta_path']
