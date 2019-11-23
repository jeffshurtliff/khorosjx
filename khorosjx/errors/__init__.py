# -*- coding: utf-8 -*-
"""
:Package:        khorosjx.errors
:Synopsis:       This package includes custom exceptions and accompanying function
:Usage:          ``import khorosjx.errors`` (Imported by default in primary package)
:Example:        ``raise errors.exceptions.BadCredentialsError``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  23 Nov 2019
"""
# Define all modules that will be imported with the "import *" method
__all__ = ['exceptions', 'handlers']

# Always import the warnings package and the exceptions module
import warnings

from . import exceptions, handlers
