# coding=utf-8
"""
errors.py expected errors and handlers
"""
import falcon


class BlogHTTPError(falcon.HTTPError):
    """
       The generic http error that can be thrown from within a falcon app
       """

    def __init__(self, status, data=None, code=None):
        """
        the initialization
        :param data:
        """
        self.data = data
        self.status = status
        self.code = code
        super(BlogHTTPError, self).__init__(self.status)

    def to_dict(self, obj_type=dict):
        """

        :param obj_type:
        :return:
        """
        return self.data


class ValidationFailed(BlogHTTPError):
    """
    The generic http error that can be thrown from within a falcon app
    """

    def __init__(self, data=None, code=None):
        """
        the initialization
        :param data:
        """
        self.data = data
        self.status = "409 "
        self.code = code
        super(ValidationFailed, self).__init__(self.status, data=data)
