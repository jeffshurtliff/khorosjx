# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.utils.classes
:Synopsis:       Collection of classes relating to the khorosjx library
:Usage:          ``from khorosjx.utils.classes import Users``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  08 Jan 2020
"""


# Define a class for content-related list, dictionaries and other utilities
class Content:
    """This class includes content-related lists, dictionaries and other utilities."""
    # Map the content types to their respective contentTypeID
    content_types = {
        'blog post': 38,
        'discussion': 1,
        'document': 102,
        'event': 96891546,
        'idea': 3227383,
        'question': 1,
        'thread': 1,
        'video': 1100
    }

    # Map the content types to the delimiter the URL for them
    content_url_delimiters = {
        'blog post': '/community',
        'discussion': '/thread',
        'document': '/docs',
        'event': '/events',
        'idea': '/ideas',
        'question': '/thread',
        'thread': '/thread',
        'video': '/videos'
    }

    # Define the permitted file types for videos
    permitted_video_file_types = ['avi', 'mov', 'wmv', 'mp4', 'mpg', 'mpeg', 'flv', '3gp', '3g2']


# Define a class for lists of JSON fields for various API data sets
class FieldLists:
    """This class provides lists of JSON fields for various API data sets."""
    document_fields = ['id', 'entityType', 'followerCount', 'likeCount', 'published', 'tags',
                       'updated', 'contentID', 'author', 'content', 'parent', 'favoriteCount',
                       'replyCount', 'status', 'subject', 'viewCount', 'visibleToExternalContributors',
                       'parentVisible', 'parentContentVisible', 'restrictComments', 'editDisabled',
                       'version', 'attachments', 'helpfulCount', 'unhelpfulCount', 'type', 'typeCode',
                       'lastActivityDate']
    people_fields = ['id', 'followerCount', 'published', 'updated', 'displayName', 'mentionName',
                     'name.formatted', 'email.value', 'followingCount', 'directReportCount',
                     'initialLogin', 'jive.lastAuthenticated', 'jive.externalIdentities.identityType',
                     'jive.externalIdentities.identity', 'jive.username', 'jive.status']
    place_fields = ['id', 'followerCount', 'followed', 'published', 'tags', 'updated', 'placeID', 'contentTypes',
                    'description', 'displayName', 'name', 'parent', 'status', 'viewCount', 'placeTopics', 'childCount',
                    'visibleToExternalContributors',  'locale', 'inheritsAppliedEntitlements', 'type', 'typeCode',
                    'resources.html.ref']
    security_group_fields = ['id', 'published', 'updated', 'administratorCount', 'memberCount', 'name',
                             'description', 'federated']


# Define a class for group-related lists, dictionaries and other utilities
class Groups:
    """This class provides various mappings to security group-related information."""
    # Map the membership types to the appropriate API endpoint
    membership_types = {
        'admin': 'administrators',
        'member': 'members'
    }

    # Map the user types to the response data types
    user_type_mapping = {
        'admin': 'group_admins',
        'member': 'group_members'
    }


# Define a class for platform-related lists, dictionaries and other utilities
class Platform:
    """This class provides various mappings to Jive-related information such as environments, URLs, etc."""
    # Define the high-level core API versions
    core_api_versions = ['v2', 'v3']


# Define a class for user-related lists, dictionaries and other utilities
class Users:
    """This class includes user-related lists, dictionaries and other utilities."""

    # Define a class for user JSON fields
    class UserJSON:
        """This class maps the field names in the users table to the JSON field names."""
        fields = {
            'user_jive_id': 'id',
            'user_full_name': ('name', 'formatted'),
            'user_email': ('emails', 0, 'value'),
            'user_username': ('jive', 'username'),
            'user_enabled': ('jive', 'enabled'),
            'user_federated': ('jive', 'federated'),
            'user_external_id': ('jive', 'externalIdentities', 0, 'identity'),
            'user_first_login': 'initialLogin',
            'user_last_login': ('jive', 'lastAuthenticated'),
            'user_agm_level': ('jive', 'level', 'name'),
            'user_agm_points': ('jive', 'level', 'points'),
            'user_tags': 'tags',
            'user_address_street': ('addresses', 0, 'value', 'streetAddress'),
            'user_address_city': ('addresses', 0, 'value', 'locality'),
            'user_address_state': ('addresses', 0, 'value', 'region'),
            'user_address_zip': ('addresses', 0, 'value', 'postalCode'),
            'user_address_country': ('addresses', 0, 'value', 'country'),
            'user_locale': ('jive', 'locale'),
            'user_profile': ('jive', 'profile')
        }
        profile_fields = {
            'Company': 'user_company',
            'Title': 'user_job_title',
            'Certifications': 'user_certifications',
            'Department': 'user_department',
            'Biography': 'user_biography',
            'Occupation': 'user_occupation',
            'URL': 'user_website',
            'Twitter': 'user_twitter'
        }


# Define class related to time and date information
class TimeUtils:
    """This class contains dictionaries and other utilities to assist with time-related function calls."""
    # Define a dictionary of time formats and their respective syntax
    time_formats = {
        'delimited': '%Y-%m-%dT%H:%M:%S',
        'split': '%Y-%m-%d %H:%M:%S'
    }
