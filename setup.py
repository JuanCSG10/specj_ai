from setuptools import find_packages, setup

from specj_ai import __author__, __description__, __license__, __name__, __version__

setup(
    author=__author__,
    description=__description__,
    license=__license__,
    name=__name__,
    packages=find_packages(),
    version=__version__,
)
