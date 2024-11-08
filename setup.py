"""
AutoSubber
"""

from setuptools import setup, find_packages

setup(
    name="AutoSubber",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "pandas",
        "cryptography",
        "apscheduler",
    ],
)
