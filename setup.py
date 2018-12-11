import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name = 'pylabutils',
    version = '1.0',
    author = 'Mario García',
    author_email = 'mariogarcc@gmail.com',
    description = 'Some utils for working with python and latex'
        ' in a simple lab-like environment',
    long_description_content_type ='text/markdown',
    url = 'https://github.com/mariogarcc/pylabutils',
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
