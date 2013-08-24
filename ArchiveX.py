__author__ = 'tinyms'

import os, sys
import logging as log
import webbrowser

from tornado.ioloop import IOLoop
from tornado.web import Application

from tinyms.common import Plugin, Utils, Postgres
from tinyms.point import IWebConfig, IDatabase
from tinyms.web import IRequest
from tinyms.widgets import IWidget
from tinyms.orm import SessionFactory

Plugin.load()

db_config = Plugin.one(IDatabase)
if db_config:
    if hasattr(db_config, "name"):
        Postgres.DATABASE_NAME = db_config.name()
    if hasattr(db_config, "user"):
        Postgres.USER_NAME = db_config.user()
    if hasattr(db_config, "password"):
        Postgres.PASSWORD = db_config.password()
    if hasattr(db_config, "orm_engine"):
        SessionFactory.__engine__ = db_config.orm_engine()
        SessionFactory.create_tables()

web_configs = Plugin.get(IWebConfig)

ws_settings = dict()
ws_settings["static_path"] = os.path.join(os.getcwd(), "static")
ws_settings["template_path"] = os.path.join(os.getcwd(), "templates")
ws_settings["debug"] = True

ws_settings["ui_modules"] = dict()
for key in IWidget.__ui_mapping__:
    ws_settings["ui_modules"][key] = IWidget.__ui_mapping__[key]

if web_configs:
    for web_config in web_configs:
        if hasattr(web_config, "ws_settings"):
            web_config.settings(ws_settings)

#compress js and css file to one
Utils.combine_text_files(os.path.join(os.getcwd(), "static/jslib/"), "tinyms.common")

log.info(IRequest.__url_patterns__)
app = Application(IRequest.__url_patterns__, **ws_settings)

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