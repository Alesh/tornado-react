import os.path
import tornado.web
import reactmixin
import time

root_path = os.path.dirname(__file__)
reactmixin.register(os.path.join(root_path, 'helloworld.jsx'), 'HelloWorld')

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        if self.settings['time_now'] > self.settings['check_time']:
            raise RuntimeError("Unexpected error")
        self.render("index.html")


class Application(tornado.web.Application,
                  reactmixin.ReactMixin):
    
    def __init__(self, **settings):
        handlers = [
            (r"/index.html", MainHandler),
            (r"/", MainHandler)]
        settings.setdefault('static_path', os.path.join(root_path, 'static'))
        settings.setdefault('template_path', os.path.join(root_path, 'templates'))
        tornado.web.Application.__init__(self, handlers, **settings)
        settings.setdefault('time_now', time.time())
        settings.setdefault('check_time', 1540000000)
        reactmixin.ReactMixin.__init__(self)


if __name__ == '__main__':
    
    import logging
    import tornado.ioloop
    
    logging.basicConfig(level=logging.DEBUG)
    Application(debug=True).listen(5000)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()