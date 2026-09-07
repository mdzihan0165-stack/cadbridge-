#!/usr/bin/env python3
"""
Setup and installation script for CadBridge.

Author: Montasir Tajwar Jihan
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cadbridge",
    version="1.0.0",
    author="Montasir Tajwar Jihan",
    author_email="montasir.jihan@engineering.local",
    description="Computational 2D CAD Compiler & Algorithmic Drafting Engine for AutoCAD DXF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/montasir-jihan/cadbridge",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Architecture",
        "Intended Audience :: Civil Engineering",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Computer Aided Design (CAD)",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.10",
    install_requires=[
        "ezdxf>=1.4.0",
        "matplotlib>=3.8.0",
    ],
    entry_points={
        "console_scripts": [
            "cadbridge-compile=json2dxf:main",
            "cadbridge-snapshot=cad_snapshot:main",
            "cadbridge-solver=cad_solver:main",
            "cadbridge-boq=cad_boq:main",
        ],
    },
)
