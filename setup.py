from setuptools import find_packages,setup
from typing import List

def get_requirement()->List[str]:
    try:
        requirement_list:List[str]=[]
        with open('requirement.txt','r') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
            
                if requirement and requirement!='-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print('file is not found ')
        
    return requirement_list

setup(
    name="network security",
    version="0.0.0.0",
    author="muhammed rishad c",
    author_email="muhammed.risshad@gmail.com",
    packages=find_packages(),
    install_requires=get_requirement()
    
)
    