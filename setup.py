"""
FWAdmin PYPI setup file.

Install with: python3 setup.py install
Develop with: python3 setup.py develop
Make it available on PIP with:
    python3 setup.py sdist
    pip3 install twine
    twine upload dist/*
"""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"
__version__ = "0.0.1-dev1"

from setuptools import find_packages, setup

setup(
    name="fwadmin",
    version=__version__,
    description="Firewall manager and viewer plugin for Netbox",
    url="https://github.com/dainok/fwadmin",
    author="Andrea Dainese",
    author_email="andrea@adainese.it",
    license="GNU v3.0",
    install_requires=[
        "requests",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    project_urls={
        "Source": "https://github.com/dainok/fwadmin",
    },
)
