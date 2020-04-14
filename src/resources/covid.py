# coding=utf-8
"""
HA HA! A NECESSITY HERE
"""
import falcon

from .base import BaseResource
from ..schema import *


class CovidResource(BaseResource):
    """
    Resource for handling Covid requests
    """

    serializers = {
        "default": CovidRequestSchema,
        "response": CovidResponseSchema
    }

    def save(self, data, req):
        """

        :param data:
        :param req:
        :return:
        """
        path_type = data.get("path_type", None)
        result = self.service_class.load_logs() if path_type and 'log' in path_type else self.service_class.do_estimate(
            **data)

        return result

    def on_get(self, req, res, path_type=None, resource_name=None):
        """

        :param req:
        :param res:
        :param path_type:
        :param resource_name:
        :return:
        """
        if path_type and 'log' in path_type:
            res.status = falcon.HTTP_200
            res.content_type = 'text/plain'
            res.media = self.service_class.load_logs()
