# -*- coding: utf-8 -*-
"""
:Package:        khorosjx.errors
:Synopsis:       This module includes custom exceptions and accompanying function
:Usage:          ``import khorosjx.errors`` (Imported by default in primary package)
:Example:        ``raise errors.exceptions.BadCredentialsError``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  08 Jan 2020
"""
# Define all modules that will be imported with the "import *" method
__all__ = ['exceptions', 'handlers']

# Always import the warnings package and the exceptions module
from . import exceptions, handlers
