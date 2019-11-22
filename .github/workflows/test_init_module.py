import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

import khorosjx

# Test the init_module() function
def init_module_operation():
    khorosjx.init_module('admin', 'content', 'groups', 'spaces', 'users')
    return True

# Verify that the operation was successful
def test_init_module():
    assert init_module_operation() is True