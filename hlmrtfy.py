import tornado.escape
import tornado.httpclient
import tornado.ioloop
import tornado.web

from bs4 import BeautifulSoup

import os.path
import urllib2


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Yo')

class ReadHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        url_to_read = self.request.arguments['url'][0]
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch(url_to_read, callback=self.on_response)

    def on_response(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        self.write(tornado.escape.json_encode([string for string in soup.body.stripped_strings]))
        self.finish()

settings = {
    'static_path' : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
    'default_filename': 'index.html'
}

print settings
application = tornado.web.Application([
    (r'/read', ReadHandler),
    (r'/(.*)', tornado.web.StaticFileHandler, dict(path=settings['static_path'], default_filename='index.html')),
], **settings)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
