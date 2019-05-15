# -*- coding: utf-8 -*-
import distutils
import os.path

from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install as setuptools_install


PTH = """
# -*- coding: utf-8 -*-
try:
    import __transform__
    import source_transform
except ImportError:
    pass
else:
    source_transform.setup_meta_path()
"""


class install(setuptools_install):

    def initialize_options(self):
        setuptools_install.initialize_options(self)

        contents = 'import sys; exec({!r})\n'.format(PTH)
        self.extra_path = (self.distribution.metadata.name, contents)

    def finalize_options(self):
        setuptools_install.finalize_options(self)

        install_suffix = os.path.relpath(
            self.install_lib, self.install_libbase,
        )
        if install_suffix == '.':
            distutils.log.info('skipping install of .pth during easy-install')
        elif install_suffix == self.extra_path[1]:
            self.install_lib = self.install_libbase
            distutils.log.info(
                "will install .pth to '%s.pth'",
                os.path.join(self.install_lib, self.extra_path[0]),
            )
        else:
            raise AssertionError(
                'unexpected install_suffix',
                self.install_lib, self.install_libbase, install_suffix,
            )


setup(
    name='source-transform',
    version='0.1.1',
    author='Grant Bakker',
    author_email='grant@bakker.pw',
    description='Python source transformation framework',
    url='https://github.com/bakkerthehacker/source-transform/',
    classifiers=(
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ),
    packages=find_packages(exclude=['tests.*', 'tests']),
    install_requires=['six', 'toolz'],
    cmdclass={'install': install},
)
