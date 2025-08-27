"""
Setup configuration for shapix geometry engine
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Shapix - A geometry engine for Python"

setup(
    name="shapix",
    version="0.1.0",
    author="BerkayZ",
    author_email="zelyurtberkay@gmail.com",
    description="A geometry engine for Python with text-based syntax and PNG export",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/berkayz/shapix",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Education",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pillow>=8.0.0",  # For PNG export
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.10",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.910",
        ],
        "gui": [
            "tkinter",  # Usually included with Python
        ]
    },
    entry_points={
        "console_scripts": [
            "shapix=shapix.cli:main",
        ],
    },
    keywords=[
        "geometry", 
        "mathematics", 
        "visualization", 
        "education", 
        "graphics", 
        "shapes", 
        "canvas",
        "png",
        "export"
    ],
    project_urls={
        "Bug Reports": "https://github.com/BerkayZ/shapix/issues",
        "Source": "https://github.com/BerkayZ/shapix",
    },
)