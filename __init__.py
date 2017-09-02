import six

from pyramid.config import Configurator
from waitress import serve

from app import settings as main_settings
from app.routes import routes

from wsgicors import CORS

if six.PY2:
    attr = 'iteritems'
else:
    attr = 'items'
settings = {K: V for K, V in getattr(main_settings.__dict__, attr)() if
            K.isupper() and K.isalpha()}

config = Configurator(settings=settings)



def main(**settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Pyramid requires an authorization policy to be active.
    # Enable JWT authentication.
    all_routes = []
    for route in routes:
        if route not in all_routes:
            all_routes.append(route)
            config.add_route(*route)
            print route
        else:
            print "Found conflicting routes, ignoring "
            print route
    config.scan('app.base.api.main')
    return CORS(config.make_wsgi_app(), headers="*", methods="*", origin="*")

if __name__ == '__main__':
    serve(main(), host='0.0.0.0', port=7000)

