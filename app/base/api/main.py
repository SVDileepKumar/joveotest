import json
import six
import re
import glob

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.compat import escape

from app.utils import DictList
from app.utils import import_by_path


__all__ = ['Resource']


class resource_meta(type):
    def __new__(Klass, name, parent, attrs):
        if 'route_name' not in attrs:
            route_name = name.lower()
            attrs['route_name'] = route_name
        else:
            route_name = str(attrs['route_name'])
        New_Klass = type.__new__(Klass, name, parent, attrs)

        # it will avoid errors due to unregistered route
        if New_Klass.__name__ in ('Resource'):
            return New_Klass
        return view_config(route_name=route_name)(New_Klass)


class Resource(object):
    __metaclass__ = resource_meta
    _allowed_methods = ['get', 'put', 'post', 'delete']

    def __init__(self, request, *args, **settings):
        self.request = request
        super(Resource, self).__init__(*args, **settings)

    def __call__(self, *args, **kwargs):
        if self.request:
            meth = self.request.method.lower()
            if hasattr(self, meth) and meth in self._allowed_methods:
                # We are keeping `kwargs` for future compatibility reasons
                kwargs.update(self.escaped_params)

                return view_config(request_method=meth)(getattr(self, meth)
                                                        (*args, **kwargs))
            return Response(status=403)

    @property
    def escaped_qs(self):
        """

        :return: this gives all the url parameters from query string
        """
        req_params = self.request.params

        keys = []

        esc_params = DictList()
        if req_params is not None:
            for d in req_params.dicts:
                keys.extend(d.mixed())
            for key in keys:
                value_list = req_params.getall(key)
                for value in value_list:
                    if issubclass(type(value), unicode):
                        esc_value = escape(value)
                    else:
                        esc_value = value
                    esc_params.__setitem__(key, esc_value)
        return esc_params

    @property
    def escaped_url(self):
        return escape(self.request.url)

    @property
    def escaped_params(self):
        req_route_match = {}
        path_match = self.request.matchdict
        print(path_match)
        for key in path_match.keys():
            req_route_match[key] = escape(path_match[key])
        return req_route_match

    @property
    def escaped_json(self):
        try:
            # fields with empty values are discarded
            req_json = {k: v for k, v in self.request.json.items() if v != ''}
            req_json_str = json.dumps(req_json)
            return json.loads(escape(req_json_str))
        except ValueError:
            message = "couldn't find valid json object"
            six.reraise(ValueError, ValueError(message))



#### Auto Imports ########

files =  glob.glob('*/controller/*.py')


def imports():
    for filename in files:
        print(re.sub('/', '.', re.sub('.py', '', filename)))
        try:
            class_dict_items = \
                {k: v for k, v in
                 import_by_path(re.sub('/', '.', re.sub('.py', '', filename)) + '.*',
                                module=True).__dict__.items() if not k.startswith('_')}
            for k, v in class_dict_items.items():
                globals()[k] = v
        except AttributeError:
            continue


imports()
# print globals()
###### end Auto Imports #######

