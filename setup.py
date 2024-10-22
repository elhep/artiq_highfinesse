import subprocess

from setuptools import find_packages, setup
from setuptools.command.install import install

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="artiq_highfinesse",
    install_requires=required,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "aqctl_artiq_highfinesse = artiq_highfinesse.aqctl_artiq_highfinesse:main",
        ],
    },
)
