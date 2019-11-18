#####################################
KhorosJX Python Library Documentation
#####################################

Introduction
============
The **khorosjx** library acts as a Python software development kit (SDK)
to administer and manage `Khoros JX <https://community.khoros.com/t5/Atlas-Insights-Blog/Lithium-and-Jive-x-
It-s-Official/ba-p/325465>`_ (formerly `Jive-x <https://www.prnewswire.com/news-releases/lithium-technologies-
completes-acquisition-of-external-online-community-business-from-jive-300531058.html>`_) and 
`Jive-n <https://www.jivesoftware.com/>`_ online community platforms.


Installation
============
.. todo:: Coming Soon!


Modules
=======
The KhorosJX Python Library consists of the following `primary modules`_:

`Core Module (khorosjx.core)`_
    This module contains core functions such as initializing the connection to the API, getting API version
    information, performing GET and PUT requests, etc.

`Admin Module (khorosjx.admin)`_
    This module contains administrative functions that would only be performed by a platform administrator
    or a community manager.

`Content Module (khorosjx.content)`_
    This module contains functions relating to content within the platform which allows for creating, editing
    and managing content such as documents, ideas, videos, etc.

`Groups Module (khorosjx.groups)`_
    This module contains functions for working with security groups (and eventually social groups) such as
    obtaining and managing group membership.

`Spaces Module (khorosjx.spaces)`_
    This module contains functions for working with spaces, such as identifying content within spaces, etc.

`Users Module (khorosjx.users)`_
    This module contains functions for working with users, such as obtaining their account/profile information, 
    getting a count of their created content, etc.


The library also includes some `auxilliary modules`_ to support the overall functionality of 
the `primary modules`_, as well as modules containing global `classes and exceptions`_ for the library, which
are listed below.

`Core Utilities Module (khorosjx.utils.core_utils)`_
    This module includes various utilities to assist in converting dictionaries to JSON, formatting timestamps, etc.

`Classes Module (khorosjx.utils.classes)`_
    This module contains nearly all classes utilized by other modules within the library.

`Exceptions Module (khorosjx.errors.exceptions)`_
    This module contains all of the exception classes leveraged in functions throughout the library.


Primary Modules
---------------
The subsections below contain the functions within each of the primary modules.


Core Module (khorosjx.core)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: khorosjx.core
    :members:


Admin Module (khorosjx.admin)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: khorosjx.admin
    :members:


Content Module (khorosjx.content)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: khorosjx.content
    :members:


Groups Module (khorosjx.groups)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: khorosjx.groups
    :members:


Spaces Module (khorosjx.spaces)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: khorosjx.spaces
    :members:


Users Module (khorosjx.users)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: khorosjx.users
    :members:


Auxilliary Modules
------------------
The subsections below contain the functions within each of the auxilliary modules.


Core Utilities Module (khorosjx.utils.core_utils)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: khorosjx.utils.core_utils
    :members:


Classes and Exceptions
----------------------
The subsections below contain the classes and exceptions leveraged throughout the library.


Classes Module (khorosjx.utils.classes)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: khorosjx.utils.classes
    :members:


Exceptions Module (khorosjx.errors.exceptions)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: khorosjx.errors.exceptions
    :members:


.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
