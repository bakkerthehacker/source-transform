# -*- coding: utf-8 -*-
import imp
import mmap
import sys

from toolz import memoize

from .discovery import find_transforms


class TransformFinderLoader(object):

    def find_module(self, fullname, path=None):
        self.fullname = fullname
        self.path = path

        try:
            self.found = imp.find_module(fullname.rpartition('.')[-1], path)
            (
                self.file,
                self.pathname,
                (self.suffix, self.mode, self.type)
            ) = self.found
        except Exception:
            return None

        if self.type in (
            imp.C_BUILTIN,
            imp.C_EXTENSION,
            imp.PY_COMPILED,
            imp.PY_FROZEN,
        ):
            return None

        if not self.file:
            return None

        if self.mode and (
            not self.mode.startswith(('r', 'U'))
            or '+' in self.mode
        ):
            return None

        triggered_transforms = self.get_triggered_transforms()

        if triggered_transforms:
            self.triggered_transforms = triggered_transforms
            return self

        return None

    def get_kwargs(self):
        return {
            key: getattr(self, key)
            for key in (
                'fullname', 'path', 'file', 'pathname', 'suffix',
                'mode', 'type', 'found', 'mmaped_file',
            )
        }

    def get_triggered_transforms(self):
        self.mmaped_file = mmap.mmap(
            self.file.fileno(),
            0,
            prot=mmap.PROT_READ
        )

        triggered_transforms = set()
        for transform in self.transforms:
            self.file.seek(0)
            self.mmaped_file.seek(0)

            if transform.trigger(**self.get_kwargs()):
                triggered_transforms.add(transform)

        self.mmaped_file.close()

        return triggered_transforms

    @property
    @memoize
    def transforms(self):
        return find_transforms()

    def load_module(self, fullname):
        try:
            return sys.modules[fullname]
        except KeyError:
            pass

        try:

            module = imp.new_module(fullname)
            sys.modules[fullname] = module
            module.__file__ = self.pathname
            module.__loader__ = self

            if self.type == imp.PKG_DIRECTORY:
                module.__path__ = [self.pathname]
                module.__package__ = fullname
            elif self.type == imp.PY_SOURCE:
                module.__package__ = fullname.rpartition('.')[0]

            data = self.file.read()

            for transform in self.triggered_transforms:
                data = transform.transform(data, **self.get_kwargs())

            code = compile(data, self.pathname, 'exec')

            exec(code, module.__dict__)

        except Exception:
            if fullname in sys.modules:
                del sys.modules[fullname]
            raise

        return module


TRANSFORM_FINDER_LOADER = TransformFinderLoader()


def setup_meta_path():
    if TRANSFORM_FINDER_LOADER not in sys.meta_path:
        sys.meta_path.insert(0, TRANSFORM_FINDER_LOADER)
