
import uuid
import time
import importlib
from types import ModuleType



class CommonUtils(object):

    @classmethod
    def get_uuid(cls):
        return uuid.uuid4().hex

    @classmethod
    def get_uuid_with_timestamp(cls):
        """
        :return:  First 32 characters are hex of UUID , next 11 characters are the hex of timestamp
        """
        timestamp = cls.get_currenttime_in_milli()
        return cls.get_uuid()  + str(hex(timestamp).lstrip("0x"))
    @classmethod
    def get_currenttime_in_milli(cls):
        return  int(round(time.time() * 1000))


def import_by_path(path, module = False, silent=False, set_globals=False):
    """
    :param path: Full non-relative path of the object in dotted form
    :param silent: setting this to `True` will not throw any import error
    :param set_globals: set this to `True` to set the imported object available by name
            in 'globals()' dictionary instead of returning the object
    :return: if set_globals is set to False, returns imported object
    """
    try:
        modulename, classname = path.rsplit('.', 1)
    except ValueError as e:
        if not silent:
            e.msg = "%s doesn't look like a module path" % path
            raise e
    else:
        mod = importlib.import_module(modulename)
        if module and isinstance(mod, ModuleType):
            return mod
        klass = None
        if hasattr(mod, classname):
            klass = getattr(mod, classname)
        if not set_globals:
            return klass
        return classname, klass


class DictList(dict):
    """This is a Data Structure which helps to retain the value of previous key when the same key with another value is passed
        It will generate a list for each key and the list follows order
    """
    def __setitem__(self, key, value):
        try:
            val = self.__getitem__(key)
            val.append(value)
            super(DictList, self).__setitem__(key, val)
        except KeyError:
            val = list()
            val.append(value)
            super(DictList, self).__setitem__(key, val)

    def __init__(self, iterable=None, **kwargs):
        super(DictList, self).__init__()
        if iterable:
            for item in iterable:
                try:
                    val = list()
                    val.append(item[1])
                    self.__setitem__(item[0], val)
                except KeyError as e:
                    raise KeyError(e)
        if kwargs:
            for k, v in kwargs.items():
                val = list()
                val.append(v)
                self.__setitem__(k, val)
