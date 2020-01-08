===============
Primary Modules
===============
This section provides details around the primary modules used in the **khorosjx** package,
which are listed below.

* `Init Module (khorosjx)`_
* `Core Module (khorosjx.core)`_
* `Admin Module (khorosjx.admin)`_
* `Content Module (khorosjx.content)`_
    * `Base Content Module (khorosjx.content.base)`_
    * `Documents Module (khorosjx.content.docs)`_
    * `Events Module (khorosjx.content.events)`_
    * `Ideas Module (khorosjx.content.ideas)`_
    * `Threads Module (khorosjx.content.threads)`_
    * `Videos Module (khorosjx.content.videos)`_
* `Groups Module (khorosjx.groups)`_
* `Places Module (khorosjx.places)`_
    * `Base Places Module (khorosjx.places.base)`_
    * `Blogs Module (khorosjx.places.blogs)`_
    * `Spaces Module (khorosjx.places.spaces)`_
* `Spaces Module (khorosjx.spaces)`_
* `Users Module (khorosjx.users)`_

|

Init Module (khorosjx)
======================
This module (being the primary ``__init__.py`` file for the library) contains the functions
to initialize the modules and the :doc:`Helper Utility <using-helper>`.

.. automodule:: khorosjx
   :members: init_module, init_helper

:doc:`Return to Top <primary-modules>`

|

Core Module (khorosjx.core)
===========================
This module contains core functions such as initializing the connection to the API, getting 
API version information, performing GET and PUT requests, etc.

.. automodule:: khorosjx.core
   :members:

:doc:`Return to Top <primary-modules>`

|

Admin Module (khorosjx.admin)
=============================
This module contains administrative functions that would only be performed by a platform 
administrator or a community manager.

.. automodule:: khorosjx.admin
   :members:

:doc:`Return to Top <primary-modules>`

|

Content Module (khorosjx.content)
=================================
This module contains functions relating to content within the platform which allows for 
creating, editing and managing content such as documents, ideas, videos, etc.

.. automodule:: khorosjx.content
   :members: get_content_id, overwrite_doc_body, get_document_info, get_document_attachments

:doc:`Return to Top <primary-modules>`

|

Base Content Module (khorosjx.content.base)
-------------------------------------------
This module contains the core functions relating to content within the platform which allows for
creating, editing and managing content.

.. automodule:: khorosjx.content.base
   :members:

:doc:`Return to Top <primary-modules>`

|

Documents Module (khorosjx.content.docs)
----------------------------------------
This module contains functions specific to handling documents.

.. automodule:: khorosjx.content.docs
   :members:

:doc:`Return to Top <primary-modules>`

|

Events Module (khorosjx.content.events)
---------------------------------------
This module contains functions specific to handling events.

.. automodule:: khorosjx.content.events
   :members:

:doc:`Return to Top <primary-modules>`

|

Ideas Module (khorosjx.content.ideas)
-------------------------------------
This module contains functions specific to handling ideas.

.. automodule:: khorosjx.content.ideas
   :members:

:doc:`Return to Top <primary-modules>`

|

Threads Module (khorosjx.content.threads)
-----------------------------------------
This module contains functions specific to handling community discussion and question threads.

.. automodule:: khorosjx.content.threads
   :members:

:doc:`Return to Top <primary-modules>`

|

Videos Module (khorosjx.content.videos)
---------------------------------------
This module contains functions specific to handling videos.

.. automodule:: khorosjx.content.videos
   :members:

:doc:`Return to Top <primary-modules>`

|

Groups Module (khorosjx.groups)
===============================
This module contains functions for working with security groups (and eventually social 
groups) such as obtaining and managing group membership.

.. automodule:: khorosjx.groups
   :members:

:doc:`Return to Top <primary-modules>`

|

Places Module (khorosjx.places)
===============================
This module contains sub-modules containing functions for working with containers
known as places, which are identified as either spaces or blogs.

.. automodule:: khorosjx.places
   :members:

:doc:`Return to Top <primary-modules>`

|

Base Places Module (khorosjx.places.base)
-----------------------------------------
This module contains core functions relating to places. (i.e. spaces and blogs)

.. automodule:: khorosjx.places.base
   :members:

:doc:`Return to Top <primary-modules>`

|

Blogs Module (khorosjx.places.blogs)
------------------------------------
This module contains functions for working with blogs (meaning the containers rather
than the individual blog posts) such as identifying posts within a blog, etc.

.. automodule:: khorosjx.places.blogs
   :members:

:doc:`Return to Top <primary-modules>`

|

Spaces Module (khorosjx.places.spaces)
--------------------------------------
This module contains functions for working with spaces, such as identifying content
within spaces, space permissions, permitted content types, etc.

.. automodule:: khorosjx.places.spaces
   :members:

:doc:`Return to Top <primary-modules>`

|

Spaces Module (khorosjx.spaces)
===============================
This module contains functions for working with spaces, such as identifying content 
within spaces, etc.

.. automodule:: khorosjx.spaces
   :members:

:doc:`Return to Top <primary-modules>`

|

Users Module (khorosjx.users)
=============================
This module contains functions for working with users, such as obtaining their account/profile 
information, getting a count of their created content, etc.

.. automodule:: khorosjx.users
   :members:

:doc:`Return to Top <primary-modules>`
