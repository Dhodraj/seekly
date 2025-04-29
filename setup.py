from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="seekly",
    version="0.1.0",
    author="Seekly Team",
    author_email="dhodrajsdr192@gmail.com.com",
    description="Natural language search for files using codet5p-110m-embedding model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="g se",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "seekly=seekly:cli",  # This will use the cli function from seekly.py in the root directory
        ],
    },
    py_modules=["seekly"],  # This includes the root seekly.py file in the package
)