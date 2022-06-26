from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as requirement_file:
    requirements_list = requirement_file.readlines()
    requirements_list = [lib.replace("\n", "") for lib in requirements_list]

requirements = requirements_list

setup(
    name="Agritech-LIDAR",
    version="0.1.0",
    description="Agritech-LIDAR is an open-source python package for retrieving, transforming, and visualizing point cloud data.",
    url="https://github.com/nahomfix/Agritech-LIDAR.git",
    author="Nahom Bekele",
    author_email="nahom.fix@gmail.com",
    license="MIT License",
    install_requires=requirements,
    long_description=readme,
)
