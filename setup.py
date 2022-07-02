"""
equivalent to requirements.txt 
but it is used for installing local packages
"""

from setuptools import setup, find_packages
from typing import List



# Declaring Variables for setup functions
PROJECT_NAME="housing-predictor"
VERSION="0.0.1"
AUTHOR="Utkarsh Tewari"
DESCRIPTION="This is my first project for current FSDS batch"
PACKAGES=["housing"]
LICENSE="MIT License"
PLATFORMS="WEB"
REQUIREMENTS_FILENAME="requirements.txt"



def get_requirements_list()->List[str]:
    """
    This function is responsible for returning the list of name of all
    the dependencies required and mentioned in requirements.txt
    USE OF -e . = when using "pip install -r requirements.txt" in order to specify the installation of any local package present
                  and setup.py is required for installing -e. or local packages

    Returns:
    --------
    List[str]: list
        List of string specifying the packages mentioned in requirements.txt
    
    """
    
    
    with open(REQUIREMENTS_FILENAME) as requirements_file:
        return requirements_file.readlines().remove("-e .")





setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    # packages=PACKAGES,
    packages=find_packages(),
    license=LICENSE,
    platforms=PLATFORMS,
    install_requires=get_requirements_list()

)

