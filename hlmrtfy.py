import tornado.escape
import tornado.httpclient
import tornado.ioloop
import tornado.web

from bs4 import BeautifulSoup
from bs4.element import Comment

import os.path
import re
import urllib2


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Yo')


def visible(element):
    if isinstance(element, Comment):
        return False
    elif element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    return True


def extract_text(html):
    soup = BeautifulSoup(html, 'lxml')
    visible_stuff = filter(visible, soup.findAll(text=True))

    chunks = []
    for chunk in visible_stuff:
        for sub_chunk in chunk.split('.'):
            sub_chunk = sub_chunk.strip()
            if not sub_chunk:
                continue
            chunks.append('%s.' % sub_chunk)
    return chunks
    

class ReadHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        url_to_read = self.request.arguments['url'][0]
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch(url_to_read, callback=self.on_response)

    def on_response(self, response):
        chunks = extract_text(response.body)
        self.write(tornado.escape.json_encode(chunks))
        self.finish()

settings = {
    'static_path' : os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
    'default_filename': 'index.html'
}

application = tornado.web.Application([
    (r'/read', ReadHandler),
    (r'/(.*)', tornado.web.StaticFileHandler, dict(path=settings['static_path'], default_filename='index.html')),
], **settings)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
