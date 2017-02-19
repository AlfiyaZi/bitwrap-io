"""
bitwrap_pnml.api

this module defines routes
"""
import os
import cyclone.web
from cyclone.web import RequestHandler
from bitwrap_pnml.api import headers, spec, rpc, pnml, state, machine, event

VERSION = 'v2'

VENDOR_PATH = os.path.abspath(__file__ + '/../../vendor')

def factory():
    """ build a valid cyclone app """
    return cyclone.web.Application([
        (r"/", cyclone.web.RedirectHandler, {"url": "/ui/index.html"}),
        (r"/version", Version),
        (r"/swagger.json", spec.Resource),
        (r"/ui/?", cyclone.web.RedirectHandler, {"url": "/ui/index.html"}),
        (r"/ui/(.+)", cyclone.web.StaticFileHandler, {"path": VENDOR_PATH + '/swagger-ui'}),
        (r"/pnml/(.*).xml", pnml.Resource),
        (r"/pnml.json", pnml.ListResource),
        (r"/api", rpc.Handler),
        (r"/event/(.*)/(.*)", event.Resource),
        (r"/machine/(.*)", machine.Resource),
        (r"/machine", machine.ListResource),
        (r"/head/(.*)/(.*)", event.HeadResource),
        (r"/stream/(.*)/(.*)", event.ListResource)
    ])

class Version(headers.Mixin, RequestHandler):
    """ index """

    def get(self):
        """ report api version """
        self.write({ __name__: VERSION})
