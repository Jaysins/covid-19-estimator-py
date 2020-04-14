# coding=utf-8
"""
THE SERVICE, STRUCTURE.

"""
import json

from dicttoxml import dicttoxml


from src import *
from src.custom.handlers import CustomJSONEncoder
from src.estimator import *


class CovidService(object):
    """
    SERVICE CLASS FOR HANDLING COVID REQUESTS
    """

    @classmethod
    def hash_data(cls, data, **kwargs):
        """

        :param data:
        :param kwargs:
        :return:
        """
        data.update(cache_type=kwargs.get("cache_type", "json"))
        return str(hash(json.dumps(data)))

    @classmethod
    def check_redis(cls, key, **kwargs):
        """

        :param key:
        :param kwargs:
        :return:
        """
        res = redis.hget("covid_estimate", key)
        res = json.loads(res) if res else None
        return res

    @classmethod
    def set_redis(cls, key, value, **kwargs):
        """

        :param key:
        :param value:
        :param kwargs:
        :return:
        """
        data = json.dumps(value, cls=CustomJSONEncoder)
        redis.hset(name="covid_estimate", key=key, value=data)
        return data

    @classmethod
    def do_estimate(cls, **kwargs):
        """

        :param kwargs:
        :return:
        """
        path_type = kwargs.pop("path_type", None)
        cache_type = 'str' if path_type and 'xml' in path_type else 'json'
        data_hash = cls.hash_data(kwargs, cache_type=cache_type)
        response = cls.check_redis(key=data_hash)
        kwargs.pop("cache_type", None)

        if not response:
            response = estimator(kwargs)
            response = dict(response=dicttoxml(response, attr_type=False)) if cache_type == 'str' else response
            cls.set_redis(key=data_hash, value=response)
        return response

    @classmethod
    def load_logs(cls, **kwargs):
        """

        :param kwargs:
        :return:
        """
        try:
            f = open(settings.LOGS_PATH)
            return dict(response=bytes(f.read().encode()))
        except Exception as e:
            print(e)
            return dict(response="No records yet")

