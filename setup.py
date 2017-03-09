"""
Scrape-Utils

https://github.com/mardix/magic-scrap

"""

import os
from setuptools import setup, find_packages

setup(
    name="scrape-utils",
    version="0.1.0",
    license="MIT",
    author="Mardix",
    author_email="mardix@pylot.io",
    description="",
    url="",
    long_description=__doc__,
    py_modules=['scrape_utils'],
    include_package_data=True,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        "requests",
        "grab",
        "bitarray",
        "mmh3"
    ],
    keywords=['scrape-utils'],
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False
)

