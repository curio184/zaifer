#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup for zaifer."""

import io
import re

from setuptools import find_packages, setup


def readme():
    with io.open('README.md', encoding='utf-8') as fp:
        return fp.read()


def version():
    with io.open('zaifer/__init__.py', encoding='utf-8') as fp:
        return re.search(r'__version__ = \'(.*?)\'', fp.read()).group(1)


setup(
    name='zaifer',
    version=version(),
    description="zaifer is a zaifapi wrapper library. "
                "this library make easily to use zaifapi on python.",
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Yusuke Oya',
    author_email='curio@antique-cafe.net',
    url='https://github.com/curio184/zaifer',
    license='MIT',
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='zaif zaifapi zaif-exchange trade bot',
    install_requires=['requests']
)
