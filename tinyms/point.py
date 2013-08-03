__author__ = 'tinyms'

#for plugin to extends
class WebConfig():

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