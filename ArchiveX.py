__author__ = 'tinyms'

import os,sys
import webbrowser

from tornado.ioloop import IOLoop
from tornado.web import Application

from tinyms.common import Plugin,Postgres
from tinyms.point import IWebConfig,IDatabase
from tinyms.web import AjaxHandler, ApiHandler
from tinyms.orm import SessionFactory

Plugin.load()

db_config = Plugin.one(IDatabase)
if db_config:
    if hasattr(db_config,"name"):
        Postgres.DATABASE_NAME = db_config.name()
    if hasattr(db_config,"user"):
        Postgres.USER_NAME = db_config.user()
    if hasattr(db_config,"password"):
        Postgres.PASSWORD = db_config.password()
    if hasattr(db_config,"engine"):
        SessionFactory.__engine__ =db_config.engine()
        SessionFactory.create_tables()

web_configs = Plugin.get(IWebConfig)

ws_settings = dict()
ws_settings["static_path"] = os.path.join(os.getcwd(), "static")
ws_settings["template_path"] = os.path.join(os.getcwd(), "templates")
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
    port = 80
    while True:
        try:
            app.listen(port)
            break
        except Exception as e:
            print("%s" % e)
            port += 1
            continue
    webbrowser.open_new_tab("http://localhost:%i" % port)
    try:
        IOLoop.instance().start()
    except Exception as e:
        print("%s" % e)
        sys.exit(1)