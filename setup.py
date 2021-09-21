# -*- coding: utf-8 -*-

import setuptools

import khorosjx.utils.version

with open("README.md", "r") as fh:
    long_description = fh.read()

version = khorosjx.utils.version.__version__

setuptools.setup(
    name="khorosjx",
    version=version,
    author="Jeff Shurtliff",
    author_email="jeff.shurtliff@rsa.com",
    description="Useful tools and utilities to assist in managing a Khoros JX (formerly Jive-x) or Jive-n community.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeffshurtliff/khorosjx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Communications",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards",
        "Topic :: Internet :: WWW/HTTP :: Site Management"
    ],
    python_requires='>=3.6',
    install_requires=[
        "PyYAML>=5.4.1",
        "urllib3>=1.26.6",
        "requests>=2.26.0",
        "pandas>=1.3.3",
        "python-dateutil>=2.8.2",
    ],
)
