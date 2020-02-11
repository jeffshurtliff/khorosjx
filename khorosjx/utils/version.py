# -*- coding: utf-8 -*-
"""
:Module:            khorosjx.utils.version
:Synopsis:          This simple script contains the package version
:Usage:             ``from .utils import version``
:Example:           ``__version__ = version.get_full_version()``
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     10 Feb 2020
"""

__version__ = "2.3.0"


def get_full_version():
    """This function returns the current full version of the khorosjx package."""
    return __version__


def get_major_minor_version():
    """This function returns the current major.minor (i.e. X.Y) version of the khorosjx package."""
    return ".".join(__version__.split(".")[:2])
