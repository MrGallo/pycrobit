import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycrobit-mrgallo",
    version="0.0.1",
    author="Daniel Gallo",
    author_email="dangallo110@gmail.com",
    description="A Python interface for BBC micro:bit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrGallo/pycrobit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
