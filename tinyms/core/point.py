__author__ = 'tinyms'

from functools import wraps

#for plugin to extends
class EmptyClass():pass

class ObjectPool():
    api = dict()
    ajax = dict()
    url_patterns = list()

class IWebConfig():
    def db_driver(self):
        return None
    def settings(self, ws_setting):
        """
        Append or modify tornado setting
        :param ws_setting: dict()
        :return:
        """
        return

def route(pattern):
    """
    url mapping.
    """
    def ref_pattern(cls):
        ObjectPool.url_patterns.append((pattern, cls))
        return cls
    return ref_pattern

def auth(points=set()):
    def handle_func(func):
        @wraps(func)
        def returned_func(*args,**kwargs):
            self_ = args[0]
            account_id = self_.request.get_current_user()
            if not account_id:
                return returned_func
            points_ = self_.request.get_current_account_points()
            diff = points & points_
            if len(diff) > 0:
                print(True)
            else:
                print(False)
            return func(*args,**kwargs)
        return returned_func
    return handle_func

def api(key):
    """
    api mapping.
    """
    def ref(cls):
        ObjectPool.api[key] = cls
        return cls

    return ref

def ajax(key):
    """
    ajax mapping.
    """
    def ref(cls):
        ObjectPool.ajax[key] = cls
        return cls

    return ref