from setuptools import find_packages
from setuptools import setup

setup(
    name='battery_lab_custom_msg',
    version='0.0.0',
    packages=find_packages(
        include=('battery_lab_custom_msg', 'battery_lab_custom_msg.*')),
)
