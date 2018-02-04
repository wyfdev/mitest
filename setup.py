from setuptools import setup
from mitest import __version__

from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name        = 'mitest',
    author      = 'WYF',
    author_email= 'dev@wyf.io',
    version     = __version__,
    packages    = ['mitest'],
    url         = 'http://project.wyf.io/mitest',
    license     = 'MIT',
    description = 'mongo inspired policy test',
    include_package_data=True,
    long_description = long_description,
    python_requires  = '>=3.5'
)
