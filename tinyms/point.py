__author__ = 'tinyms'

#for plugin to extends
class IWebConfig():

    def settings(self,ws_setting):
        """
        Append or modify tornado setting
        :param ws_setting: dict()
        :return:
        """
        return
    def url_mapping(self,url_patterns):
        """
        Tornado url mapping
        Append (r'/some/any',RequestHandlerClass)
        :param url_patterns: list()
        :return:
        """
        return

class IAjax():
    def client_javascript_object_name(self):
        return "client_javascript_object_name"

class IApi():pass