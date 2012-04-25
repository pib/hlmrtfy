from unittest import TestCase
from hlmrtfy import extract_text


class ExtractTest(TestCase):
    def verify_extract(self, html, expected):
        texts = extract_text(html)
        self.assertEquals(texts, expected)

    def test_simple_body(self):
        """ The HTML body should be extracted properly """
        html = """\
          <html><head><title>Hello.</title></head>
          <body>
            This is a simple body.
          </body>
          </html>
          """
        self.verify_extract(html, ['This is a simple body.'])

    def test_ignore_comments(self):
        """ Comments anywhere in the HTML should be ignored """
        html = """\
          <html><head><title>Hello.</title>
          <!-- Ignore this -->
          </head>
          <body><!--This is the body-->
            This is a simple body.
          </body>
          </html>
          """
        self.verify_extract(html, ['This is a simple body.'])

    def test_ignore_doctype(self):
        """ Doctype should be ignored """
        html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
          <html><head><title>Hello.</title>
          </head>
          <body>
            This is a simple body.
          </body>
          </html>
          """
        self.verify_extract(html, ['This is a simple body.'])
        
    def test_ignore_script(self):
        """ Script tags anywhere in the HTML should be ignored """
        html = """\
          <html><head><title>Hello.</title>
          <script>
          var foo = 'bar';
          </script>
          </head>
          <body>
            <script>
            var bar = 'baz';
            </script>
            This is a simple body.
          </body>
          </html>
          """
        self.verify_extract(html, ['This is a simple body.'])
        
