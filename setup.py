#!/usr/bin/env python3
"""
Setup script for NetWatch - Network Monitor
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read the requirements
def read_requirements():
    return ["psutil>=5.7.0"]

setup(
    name="netwatch-monitor",
    version="1.0.0",
    author="PC0staS",
    author_email="pablocostasnieto@gmail.com",  
    description="A beautiful console-based network monitoring tool with ASCII graphs",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/PC0staS/netwatch",  
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "netwatch=netwatch.cli:main",
            "netwatch-monitor=netwatch.cli:main",
        ],
    },
    keywords="network monitoring, bandwidth monitor, console, ascii graphs, system monitoring",
    project_urls={
        "Bug Reports": "https://github.com/PC0staS/netwatch/issues",
        "Source": "https://github.com/PC0staS/netwatch",
        "Documentation": "https://github.com/PC0staS/netwatch#readme",
    },
    include_package_data=True,
    zip_safe=False,
)
