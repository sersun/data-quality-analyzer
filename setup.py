from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="data-quality-analyzer",
    version="0.1.0",
    author="Sersun Denis",
    author_email="d.sersun@gmail.com",
    description="A comprehensive tool for analyzing data quality in ML datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sersun/data-quality-analyzer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "data-quality-analyzer=data_quality_analyzer:main",
        ],
    },
)
