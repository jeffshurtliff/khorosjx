# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.utils.tests.test_init_module
:Synopsis:       This module is used by pytest to verify that primary modules can  be imported successfully
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  22 Nov 2019
"""

import os
import sys


def set_package_path():
    """This function adds the high-level khorosjx directory to the sys.path list."""
    sys.path.insert(0, os.path.abspath('../..'))
    return


# Test the init_module() function
def init_module_operation():
    """This function imports the primary modules for the package and returns ``True`` when successful."""
    import khorosjx
    khorosjx.init_module('admin', 'content', 'groups', 'spaces', 'users')
    return True


# Verify that the operation was successful
def test_init_module():
    """This function tests to confirm that all primary modules are able to be imported successfully."""
    set_package_path()
    assert init_module_operation() is True
