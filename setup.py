#!/usr/bin/env python
import setuptools

setuptools.setup(
    name = 'pylabutils',
    version = '1.0b2',
    author = 'Mario García',
    author_email = 'mariogarcc@gmail.com',
    description = 'Some utils for working with python'
        ' in a simple lab-like environment',
    long_description = open('README.md', 'r').read(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/mariogarcc/pylabutils',
    license = 'MIT',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    # https://test.pypi.org/pypi?%3Aaction=list_classifiers
    platforms = ['any'],
    keywords = 'laboratory utils tools',
    project_urls = {},
    packages = setuptools.find_packages(),
    py_modules = [],
    install_requires = ['ipython', 'numpy', 'matplotlib', 'scipy', 'uncertainties'],
    python_requires = '~=3.7',
    # package_data = {}
    include_package_data = True,
)
