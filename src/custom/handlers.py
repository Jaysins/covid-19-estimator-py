# coding=utf-8
"""
Handlers for content type
"""
from falcon.media import JSONHandler
from datetime import datetime
import six  # not necessary but advisable to avoid 'environment' issues
import json


class CustomJSONEncoder(json.JSONEncoder):
    """ JSON encoder that supports date formats """

    def default(self, obj):
        """

        :param obj:
        :return:
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        return json.JSONEncoder.default(self, obj)


class JsonHandler(JSONHandler):
    """
    Custom Handler for JSON
    """

    def serialize(self, media, content_type):
        """

        :param media:
        :param content_type:
        :return:
        """

        result = json.dumps(media, ensure_ascii=False, cls=CustomJSONEncoder)
        if six.PY3 or not isinstance(result, bytes):
            return result.encode()

        return result


class XMLHandler(JsonHandler):
    """Handler built using ...."""

    def serialize(self, media, content_type):
        """

        :param media:
        :param content_type:
        :return:
        """

        result = media.values()
        result = str("".join(result))
        if six.PY3 or not isinstance(result, bytes):
            return result.encode()
        return result


class TextHandler(JsonHandler):
    """
    TEXT handler
    """

    def serialize(self, media, content_type):

        """

        :param media:
        :param content_type:
        :return:
        """

        result = media.values()
        result = str("".join(result))
        if six.PY3 or not isinstance(result, bytes):
            return result.encode()
        return result

