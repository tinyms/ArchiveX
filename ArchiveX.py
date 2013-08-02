__author__ = 'tinyms'

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler,Application
import webbrowser,os,sys

from tinyms.model import ArchiveXConfig
from tinyms.common import Plugin

class DefaultHandler(RequestHandler):
    def get(self):
        self.redirect("/static/index.html")

settings = {
    "static_path" : os.path.join(os.getcwd(), "static")
}

Plugin.load()
test = Plugin.get(object,"archivex_config.Test")
test.hello("my plugin.")

app = Application([
    (r"/",DefaultHandler),
],**settings)

if __name__ == "__main__":
    # webbrowser.open_new_tab("http://localhost:%i" % ArchiveXConfig.Port)
    # try:
    #     app.listen(ArchiveXConfig.Port)
    #     IOLoop.instance().start()
    # except Exception as e:
    #     print("%s" % e)
    #     sys.exit(1)
    pass