"""docknv."""

from setuptools import setup
from pssh.version import __version__

setup(
    name='pssh',
    version=__version__,
    description='simple SSH connection utility',
    url='',
    author='Denis BOURGE',
    author_email='',
    license='MIT',
    packages=['pssh'],
    install_requires=[
          'six',
          'PyYAML',
          'colorama',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'pssh = pssh.shell:entry_point',
        ]
    },
)
