from io import StringIO
from html.parser import HTMLParser


class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()