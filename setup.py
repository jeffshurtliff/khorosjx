# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="khorosjx",
    version="1.3.0.b0",
    author="Jeff Shurtliff",
    author_email="jeff.shurtliff@rsa.com",
    description="Useful tools and utilities to assist in managing a Khoros JX (formerly Jive-x) or Jive-n community.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeffshurtliff/khorosjx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Communications",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards",
        "Topic :: Internet :: WWW/HTTP :: Site Management"
    ],
    python_requires='>=3.6',
)
