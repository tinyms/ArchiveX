__author__ = 'tinyms'

import sys
import os
import webbrowser

from tornado.ioloop import IOLoop
from tornado.web import Application

from tinyms.common import Plugin
from tinyms.point import IWebConfig
from tinyms.web import AjaxHandler, ApiHandler


Plugin.load()
web_configs = Plugin.get(IWebConfig)

ws_settings = dict()
ws_settings["static_path"] = os.path.join(os.getcwd(), "static")
ws_settings["debug"] = True

ws_url_patterns = [
    (r"/ajax/(.*).js", AjaxHandler),
    #/api/module.class/method
    (r"/api/(.*)/(.*)", ApiHandler)
]

for web_config in web_configs:
    if hasattr(web_config, "ws_settings"):
        web_config.settings(ws_settings)
    if hasattr(web_config, "url_mapping"):
        web_config.url_mapping(ws_url_patterns)

app = Application(ws_url_patterns, **ws_settings)

if __name__ == "__main__":
    webbrowser.open_new_tab("http://localhost:%i" % 8888)
    try:
        app.listen(8888)
        IOLoop.instance().start()
    except Exception as e:
        print("%s" % e)
        sys.exit(1)
    pass