__author__ = 'tinyms'

from tornado.ioloop import IOLoop
from tornado.web import Application
import webbrowser,os,sys

from tinyms.common import Plugin
from tinyms.point import WebConfig

Plugin.load()
web_configs = Plugin.get(WebConfig)

ws_settings = dict()
ws_url_patterns = list()

for web_config in web_configs:
    web_config.settings(ws_settings)
    web_config.url_mapping(ws_url_patterns)

app = Application(ws_url_patterns,**ws_settings)

if __name__ == "__main__":
    # webbrowser.open_new_tab("http://localhost:%i" % ArchiveXConfig.Port)
    # try:
    #     app.listen(ArchiveXConfig.Port)
    #     IOLoop.instance().start()
    # except Exception as e:
    #     print("%s" % e)
    #     sys.exit(1)
    pass