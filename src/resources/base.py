# coding=utf-8
"""
BASE
"""
import falcon


class BaseResource(object):
    """
    BASE RESOURCE OTHER RESOURCES WILL INHERIT
    """

    def __init__(self, service_class, serializers=None):
        """
        the initialization of the baseResource
        :param service_class: This is the service class that this resource will operate on
        """
        self.service_class = service_class
        self.serializers = serializers if serializers else {}

    def save(self, data, req):
        """
        Saves information sent in by on_post request, where no object id is specified.

        :param data: the data to be saved.
        :param req: the request data .
        :return: Object that was created
        """
        return self.service_class.create(**data)

    def on_get(self, req, res, path_type=None, resource_name=None):
        """

        :param req: the request body of the api call
        :param res: the response the api will send back
        :param path_type:
        :param resource_name:
        :return:
        """

        raise falcon.HTTP_502

    def on_post(self, req, res, path_type=None, resource_name=None):
        """

        :param req: the request body of a call to the api
        :param res: the response the api will send back
        :param path_type:
        :param resource_name:
        :return:
        """
        data = req.context.get("validated_data") or {}
        data.update(path_type=path_type)
        result = self.save(data, req)
        res.content_type = 'application/json'
        if path_type and 'xml' in path_type:
            res.content_type = 'application/xml'
        if path_type and 'log' in path_type:
            res.content_type = 'text/plain'
        res.status = falcon.HTTP_201
        res.media = result
