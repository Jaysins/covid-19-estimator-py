# coding=utf-8
"""
API file
"""


from wsgiref import simple_server

import falcon

import settings
from src.custom.middleware import RequestResponseMiddleware, register_api
from src.custom.handlers import *
from src.resources.covid import CovidResource
from src.services.covid import CovidService

custom_handlers = {
    'application/xml': XMLHandler(),
    'application/json': JsonHandler(),
    'application/json; charset=UTF-8': JsonHandler(),
    'text/plain': TextHandler(),
    '/': TextHandler(),
}


app = falcon.API(middleware=[RequestResponseMiddleware()])

# only updating response handlers because input data should be json!!!
app.resp_options.media_handlers.update(custom_handlers)


covid = CovidResource(CovidService, CovidResource.serializers)


register_api(app, covid, '/on-covid-19', '/on-covid-19/{path_type}', prefix=settings.API_PREFIX)

if __name__ == "__main__":
    httpd = simple_server.make_server('127.0.0.1', 4440, app)
    print("running on ", httpd.server_address)
    httpd.serve_forever()
