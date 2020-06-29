from os import path
from io import open
from setuptools import setup, find_packages
from importlib.util import find_spec


def get_readme():
    here = path.dirname(__file__)
    with open(path.join(here, 'README.md'),
              encoding='utf8') as readme_file:
        readme = readme_file.read()
        return readme


def get_history():
    here = path.dirname(__file__)
    with open(path.join(here, 'HISTORY.md'),
              encoding='utf8') as history_file:
        history = history_file.read()
        return history


def get_requirements():
    here = path.dirname(__file__)
    with open(path.join(here, 'requirements.txt'),
              encoding='utf8') as requirements_file:
        return requirements_file.read().splitlines()


setup(
    name='mlsocket',
    version='0.1.1',
    author='SeBeom Lee',
    author_email='moses97@gmail.com',
    description='Python socket for machine learning data',
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    install_requires=get_requirements(),
    license='MIT',
    include_package_data=True,
    keywords=["socket", "ml", "machine learning"],
    packages=find_packages(include=['mlsocket']),
    test_suite="tests",
    url='https://github.com/k2sebeom/mlsocket',
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
)
