__author__ = 'tinyms'

from functools import wraps
from tinyms.core.entity import SecurityPoint
#for plugin to extends
class EmptyClass(): pass


class ObjectPool():
    points = list()
    api = dict()
    ajax = dict()
    url_patterns = list()
    sidebar_menus = list()
    ui_mapping = dict()
    treeview = dict()


class IWebConfig():
    def get_server_port(self):
        return 80

    def get_database_driver(self):
        return None

    def settings(self, ws_setting):
        """
        Append or modify tornado setting
        :param ws_setting: dict()
        :return:
        """
        return


def reg_point(key, category="", group_="", description=""):
    if not key:
        return
    for sp in ObjectPool.points:
        if sp.key_ == key:
            return
    point = SecurityPoint()
    point.key_ = key
    point.description = description
    point.group_ = group_
    point.category = category
    ObjectPool.points.append(point)


def route(pattern):
    """
    url mapping.
    """

    def ref_pattern(cls):
        ObjectPool.url_patterns.append((pattern, cls))
        return cls

    return ref_pattern


def sidebar(path, url, label="", point="", position=0, icon_class="icon-link"):
    """

    :param path: /dashboard/count etc
    :param url:
    :param label:
    :param point:
    :param position: 1-1000
    :param icon_class:
    :return:
    """

    def ref_sidebar(cls):
        if path:
            if not url:
                return cls
            label_ = "Uname"
            if not label:
                label_ = path.split("/")[-1]
            else:
                label_ = label
            ObjectPool.sidebar_menus.append((position, path, url, label_, point, icon_class ))
        return cls

    return ref_sidebar


def auth(points=set(), default_value=None):
    def handle_func(func):
        @wraps(func)
        def returned_func(*args, **kwargs):
            self_ = args[0]
            account_id = self_.request.get_current_user()
            if not account_id:
                return returned_func
            points_ = self_.request.get_current_account_points()
            diff = points & points_
            if len(diff) > 0:
                return func(*args, **kwargs)
            else:
                return default_value

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


def ui(name):
    """
    ui mapping. 配置UI至模版可用
    """

    def ref_pattern(cls):
        ObjectPool.ui_mapping[name] = cls
        return cls

    return ref_pattern