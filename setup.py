from __future__ import annotations
from setuptools import find_packages, setup
from typing import List
def get_requirements() -> List[str]:
    # Return an empty list of requirements
    # requirement_list : List[str] = []
    return []

setup(
    name='sensor',
    version='0.0.1',
    author='Rishav',
    author_email='rishav.sukarna@gmail.com',
    description='APSDetect',
    long_description='Air Pressure System Detection: Enhancing Heavy Duty Vehicle Maintenance with AI-driven Fault Prediction',
    long_description_content_type='text/plain',  # Use 'text/markdown' or 'text/plain' as appropriate
    url='https://github.com/JM-Rishav/Livesensor',
    packages=find_packages(),
    license='MIT',
    install_requires=get_requirements(),  # Call the function to get the list of requirements
)
