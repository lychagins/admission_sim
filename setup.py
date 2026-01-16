from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="admission_sim",
    version="0.1.0",
    author="lychagins",
    description="Simple simulation tool for evaluating student admission strategies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lychagins/admission_sim",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.20.0",
    ],
)
