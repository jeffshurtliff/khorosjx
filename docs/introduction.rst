############
Introduction
############
The **khorosjx** library acts as a Python software development kit (SDK)
to administer and manage `Khoros JX <https://community.khoros.com/t5/Atlas-Insights-Blog/Lithium-and-Jive-x-
It-s-Official/ba-p/325465>`_ (formerly `Jive-x <https://www.prnewswire.com/news-releases/lithium-technologies-
completes-acquisition-of-external-online-community-business-from-jive-300531058.html>`_) and
`Jive-n <https://www.jivesoftware.com/>`_ online community platforms.

|

************
Installation
************
The package can be installed via pip using the syntax below.

.. code-block:: default

    # pip install khorosjx

You may also clone the repository and install from source using the syntax below.

.. code-block:: default

    # git clone git://github.com/jeffshurtliff/khorosjx.git
    # cd khorosjx/
    # python3 setup.py install

|

**********
Change Log
**********
Changes for each release can be found on the :doc:`Change Log <changelog>` page.

|

***********
Basic Usage
***********
This section provides basic usage instructions for the package.

|

.. include:: basic-usage.rst

|

************
Requirements
************
The following packages are leveraged within the khorosjx package:

* numpy 1.17.4
* pandas-0.25.3
* python-dateutil 2.8.1
* pytz 2019.3
* requests 2.22.0
* urllib3 1.25.7

The full requirements list can be found in
the `requirements.txt <https://github.com/jeffshurtliff/khorosjx/blob/master/requirements.txt>`_ file.

|

*******
Modules
*******
The KhorosJX Python Library consists of the following :doc:`primary modules <primary-modules>`:

:ref:`primary-modules:Core Module (khorosjx.core)`
    This module contains core functions such as initializing the connection to the API, getting API version
    information, performing GET and PUT requests, etc.

:ref:`primary-modules:Admin Module (khorosjx.admin)`
    This module contains administrative functions that would only be performed by a platform administrator
    or a community manager.

:ref:`primary-modules:Content Module (khorosjx.content)`
    This module contains functions relating to content within the platform which allows for creating, editing
    and managing content such as documents, ideas, videos, etc.

:ref:`primary-modules:Groups Module (khorosjx.groups)`
    This module contains functions for working with security groups (and eventually social groups) such as
    obtaining and managing group membership.

:ref:`primary-modules:Spaces Module (khorosjx.spaces)`
    This module contains functions for working with spaces, such as identifying content within spaces, etc.

:ref:`primary-modules:Users Module (khorosjx.users)`
    This module contains functions for working with users, such as obtaining their account/profile information,
    getting a count of their created content, etc.

|

The library also includes some :doc:`supporting modules <supporting-modules>` to support the overall functionality of
the :doc:`primary modules <primary-modules>`, as well as modules containing global :ref:`supporting-modules:classes
and exceptions` for the library, which are listed below.

:ref:`supporting-modules:Core Utilities Module (khorosjx.utils.core_utils)`
    This module includes various utilities to assist in converting dictionaries to JSON, formatting timestamps, etc.

:ref:`supporting-modules:Classes Module (khorosjx.utils.classes)`
    This module contains nearly all classes utilized by other modules within the library.

:ref:`supporting-modules:Exceptions Module (khorosjx.errors.exceptions)`
    This module contains all of the exception classes leveraged in functions throughout the library.

|

*******
License
*******
This package falls under the `MIT License <https://github.com/jeffshurtliff/khorosjx/blob/master/LICENSE>`_.

|

****************
Reporting Issues
****************
Issues can be reported within the `GitHub repository <https://github.com/jeffshurtliff/khorosjx/issues>`_.

|

**********
Disclaimer
**********
This package is in no way endorsed or supported by the `Khoros <https://www.builtinaustin.com/company/khoros>`_
or `Aurea Software, Inc. <https://www.jivesoftware.com/>`_ companies.