# -*- coding: utf-8 -*-
"""
:Module:         khorosjx.utils.classes
:Synopsis:       Collection of classes relating to the khorosjx library
:Usage:          ``from khorosjx.utils.classes import Users``
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  06 Mar 2020
"""


# Define a class for lists of JSON fields for various API data sets
class FieldLists:
    """This class provides lists of JSON fields for various API data sets."""
    document_fields = ['id', 'entityType', 'followerCount', 'likeCount', 'published', 'tags',
                       'updated', 'contentID', 'author', 'content', 'parent', 'favoriteCount',
                       'replyCount', 'status', 'subject', 'viewCount', 'visibleToExternalContributors',
                       'parentVisible', 'parentContentVisible', 'restrictComments', 'editDisabled',
                       'version', 'attachments', 'helpfulCount', 'unhelpfulCount', 'type', 'typeCode',
                       'lastActivityDate']
    idea_fields = ['id', 'subject', 'followerCount', 'replyCount', 'favoriteCount', 'viewCount', 'voteCount',
                   'commentCount', 'published', 'updated', 'tags', 'contentID', 'author.id', 'author.name.formatted',
                   'author.email.value', 'content.text', 'parent', 'status', 'visibleToExternalContributors',
                   'type','typeCode','lastActivityDate','score','stage','authorshipPolicy']
    people_fields = ['id', 'followerCount', 'published', 'updated', 'displayName', 'mentionName',
                     'name.formatted', 'email.value', 'followingCount', 'directReportCount',
                     'initialLogin', 'jive.lastAuthenticated', 'jive.externalIdentities.identityType',
                     'jive.externalIdentities.identity', 'jive.username', 'jive.status']
    place_fields = ['id', 'followerCount', 'followed', 'published', 'tags', 'updated', 'placeID', 'contentTypes',
                    'description', 'displayName', 'name', 'parent', 'status', 'viewCount', 'placeTopics', 'childCount',
                    'visibleToExternalContributors',  'locale', 'inheritsAppliedEntitlements', 'type', 'typeCode',
                    'resources.html.ref']
    publication_fields = ['id', 'published', 'updated', 'subscriptions', 'name', 'author', 'displayOrder',
                          'subscriberCount', 'associationCount', 'receiveEmails', 'subscribersType', 'beingProcessed',
                          'type', 'typeCode']
    security_group_fields = ['id', 'published', 'updated', 'administratorCount', 'memberCount', 'name',
                             'description', 'federated']
    stream_fields = ['id', 'name', 'published', 'receiveEmails', 'source', 'updated', 'type']
    subscription_fields = ['id', 'published', 'updated', 'name', 'subscriberCount', 'subscribers', 'associations',
                           'type', 'typeCode']
    video_fields = ['id', 'followerCount', 'followed', 'likeCount', 'published', 'tags', 'updated', 'contentID',
                    'author', 'content', 'parent', 'contentVideos', 'favoriteCount', 'replyCount', 'status',
                    'subject', 'viewCount', 'visibleToExternalContributors', 'parentVisible', 'parentContentVisible',
                    'lastActivity', 'abuseCount', 'categories', 'visibility', 'duration', 'inline', 'externalID',
                    'hours', 'minutes', 'seconds', 'stillImageURL', 'authtoken', 'autoplay', 'height', 'playerBaseURL',
                    'playerName', 'width', 'watermarkURL', 'videoType', 'videoMetadata', 'embedded', 'type',
                    'typeCode', 'lastActivityDate']


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

    # Map the datasets to their respective field lists
    datasets = {
        'blog': FieldLists.place_fields,
        'document': FieldLists.document_fields,
        'group_admins': FieldLists.people_fields,
        'group_members': FieldLists.people_fields,
        'idea': FieldLists.idea_fields,
        'people': FieldLists.people_fields,
        'place': FieldLists.place_fields,
        'publication': FieldLists.publication_fields,
        'security_group': FieldLists.security_group_fields,
        'space': FieldLists.place_fields,
        'stream': FieldLists.stream_fields,
        'subscriptions': FieldLists.subscription_fields,
        'video': FieldLists.video_fields
    }

    # Map security group query URI identifiers to datasets
    security_group_uri_map = {
        '/administrators': 'group_admins',
        '/members': 'group_members'
    }

    # Map query URI identifiers to dataset nicknames
    uri_dataset_mapping = {
        'abuseReports': 'abuse_report',                         # Not yet supported
        'acclaim': 'acclaim',                                   # Not yet supported
        'actions': 'action',                                    # Not yet supported
        'activities': 'activity',                               # Not yet supported
        'addOns': 'add_on',                                     # Not yet supported
        'admin/plugins': 'admin_plugin',                        # Not yet supported
        'admin/profileFields': 'admin_profile_field',           # Not yet supported
        'admin/properties': 'admin_property',                   # Not yet supported
        'announcements': 'announcement',                        # Not yet supported
        'attachments': 'attachment',                            # Not yet supported
        'calendar': 'calendar',                                 # Not yet supported
        'checkpoints': 'checkpoint',                            # Not yet supported
        'collaborations': 'collaboration',                      # Not yet supported
        'comments': 'comment',                                  # Not yet supported
        'deletedObjects': 'deleted_object',                     # Not yet supported
        'dms': 'dms',                                           # Not yet supported
        'events': 'event',                                      # Not yet supported
        'eventTypes': 'event_type',                             # Not yet supported
        'extprops': 'extended_properties',                      # Not yet supported
        'extstreamDefs': 'external_stream_definition',          # Not yet supported
        'extstreams': 'external_stream',                        # Not yet supported
        'ideaVotes': 'idea_vote',                               # Not yet supported
        'images': 'image',                                      # Not yet supported
        'inbox': 'inbox',                                       # Not yet supported
        'invites': '__get_invite_dataset',                      # Not yet supported
        'v3/members': 'social_group_member',                    # Not yet supported
        'mentions': 'mention',                                  # Not yet supported
        'messages': 'message',                                  # Not yet supported
        'metadata/locales': 'metadata_locale',                  # Not yet supported
        'metadata/objects': 'metadata_object',                  # Not yet supported
        'metadata/properties': '__get_metadata_dataset',        # Not yet supported
        'metadata/resources': 'metadata_resource',              # Not yet supported
        'metadata/timezones': 'metadata_timezone',              # Not yet supported
        'moderation': '__get_moderation_dataset',               # Not yet supported
        'oembed': 'oembed',                                     # Not yet supported
        'outcomes': 'outcome',                                  # Not yet supported
        'pages': 'page',                                        # Not yet supported
        'v3/people': 'people',
        'v3/places': 'place',
        'placeTemplateCategories': 'place_template_category',   # Not yet supported
        'placeTemplates': 'place_template',                     # Not yet supported
        'placeTopics': 'place_topic',                           # Not yet supported
        'profileImages': 'profile_image',                       # Not yet supported
        'publications': 'publication',
        'questions': 'question',                                # Not yet supported
        'rsvp': 'rsvp',                                         # Not yet supported
        'search': '__get_search_dataset',                       # Not yet supported
        'v3/sections': 'section',                               # Not yet supported
        'securityGroups': '__get_security_group_dataset',
        'shares': 'share',                                      # Not yet supported
        'slides': 'slide',                                      # Not yet supported
        'supportCenter': '__get_support_center_dataset',        # Not yet supported
        'stages': 'stage',                                      # Not yet supported
        'statics': 'static_resource',                           # Not yet supported
        'streamEntries': 'stream_entry',                        # Not yet supported
        'streams': 'stream',                                    # Not yet supported
        'v3/tags': 'tag',                                       # Not yet supported
        'tileDefs': 'tile_definition',                          # Not yet supported
        'tiles': '__get_tile_dataset',                          # Not yet supported
        'urls': 'url',                                          # Not yet supported
        'versions': 'version',                                  # Not yet supported
        'videos': 'video',                                      # Not yet supported
        'vitals': 'vitals',                                     # Not yet supported
        'votes': 'vote',                                        # Not yet supported
        'webhooks': 'webhook'                                   # Not yet supported
    }


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
