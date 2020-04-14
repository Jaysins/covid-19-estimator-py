# coding=utf-8
"""
MIDDLEWARE CONFIGURATION
"""

import falcon
from marshmallow import ValidationError, EXCLUDE
from src.custom.errors import ValidationFailed
from datetime import datetime
import settings


def marshal(resp, schema):
    """
    prepares the response object with the specified schema
    :param resp: the falcon response object
    :param schema: the schema class that should be used to validate the response
    :return: falcon.Response
    """
    data = resp
    resp_ = None
    if isinstance(data, list):
        resp_ = []
        for d in data:
            resp_.append(schema().dump(d))
        # resp.media = resp_
    if isinstance(data, dict):
        resp_ = schema().load(data=data, unknown=EXCLUDE)

    return resp_


def register_api(app_, cls, *urls, **kwargs):
    """

    :param app_:
    :param cls:
    :param urls:
    :param kwargs:
    :return:
    """
    prefix = kwargs.get('prefix', '')
    for url in urls:
        app_.add_route(prefix + url, resource=cls)


def validate(req, schema):
    """
    prepares the response object with the specified schema
    :param req: the falcon request object
    :param schema: the schema class that should be used to validate the response
    :return: falcon.Response
    """
    req_data = req.media
    data = schema().load(data=req_data, unknown=EXCLUDE)
    return data


# noinspection PyMethodMayBeStatic
class RequestResponseMiddleware(object):
    """a middleware to be use to breakdown the url pattern"""

    def __init__(self, **kwargs):
        """"""
        self.domain = kwargs.get('domain', 'blog.auth')
        self.settings = kwargs.get('settings', {})

    def process_resource(self, req, res, resource, params):
        """
        performing some manipulation before the request is routed
        :param req:
        :param res:
        :param resource:
        :param params:
        :return: None
        """

        start_time = datetime.now()
        req.context.start_time = start_time
        req.context.update(params)
        if req.method.lower() in ['post', 'put']:
            try:
                serializer = resource.serializers["default"]
            except (AttributeError, IndexError, KeyError):
                raise falcon.HTTPError(falcon.HTTP_NOT_IMPLEMENTED)
            try:
                req.context["validated_data"] = validate(req, serializer)
            except ValidationError as err:
                raise ValidationFailed(data=err.messages)

    def process_response(self, req, res, resource, req_succeeded):
        """
        performing some manipulation before the request is routed
        :param req:
        :param res:
        :param resource:
        :param req_succeeded:
        :return:
        """
        path_type = req.context.get("path_type")

        if req.method.lower() in ['post'] or (req.method.lower() in ['get'] and path_type):
            try:
                serializer = resource.serializers['response']
            except (AttributeError, IndexError, KeyError):
                return
            try:
                data = res.media
                res.media = marshal(data, serializer)
            except ValidationError as err:
                # raise HTTPError(status=status.HTTP_422 as errors=err.messages)
                raise falcon.HTTPError('409 ', "Validation_failed", "Schema was not matched")
            time_ends = datetime.now()

            print(req.path)
            self.log_response_time(req.method.upper(), req.path, res.status[:3],
                                   str(int((time_ends - req.context.get("start_time")).total_seconds() * 1000)))

    def log_response_time(self, method, path, status, milliseconds):
        """

        :param method:
        :param path:
        :param status:
        :param milliseconds:
        :return:
        """
        f = open(settings.LOGS_PATH, "a")

        f.write("{method}  {path}    {status}   {milliseconds}ms\n".format(method=method, path=path, status=status,
                                                                           milliseconds=milliseconds if len(
                                                                               milliseconds) > 1 else "0{}".format(
                                                                               milliseconds)))
        f.close()
