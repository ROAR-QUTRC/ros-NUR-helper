from setuptools import setup, find_packages

_ = setup(
    name="ros-NUR-helper",
    version="0.0.0",
    packages=find_packages(),
    scripts=["./src/ros-NUR-helper.py"],
)
