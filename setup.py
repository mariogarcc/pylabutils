#!/usr/bin/env python
import setuptools

setuptools.setup(
    name = 'pylabutils',
    version = '1.1.0',
    author = 'Mario García',
    author_email = 'mariogarcc@gmail.com',
    description = 'Some utils for working with python'
        ' in a simple lab-like environment',
    long_description = open('README.md', 'r').read(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/mariogarcc/pylabutils',
    license = 'MIT',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    platforms = ['any'],
    keywords = 'laboratory utils tools',
    project_urls = {},
    packages = setuptools.find_packages(),
    py_modules = [],
    install_requires = ['ipython', 'numpy', 'matplotlib', 'scipy', 'uncertainties'],
    python_requires = '~=3.7',
    include_package_data = True,
)
