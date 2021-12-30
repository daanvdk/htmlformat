from html.parser import HTMLParser
import re

from .constants import SELF_CLOSING_TAGS


class Parser(HTMLParser):

    def __init__(self):
        super().__init__()
        self._stack = [[]]

    def handle_startendtag(self, tag, attrs):
        self.add_node('tag', tag, tuple(attrs), ())

    def handle_starttag(self, tag, attrs):
        self.add_node('tag', tag, tuple(attrs), ())
        if tag not in SELF_CLOSING_TAGS:
            self._stack.append([])

    def handle_endtag(self, tag):
        for index in range(len(self._stack) - 2, -1, -1):
            if self._stack[index][-1][2] == tag:
                self.close_tags(index)
                break

    def handle_data(self, data):
        self.add_node('text', data)

    def handle_decl(self, decl):
        self.add_node('declaration', decl)

    def handle_comment(self, data):
        self.add_node('comment', data)

    def add_node(self, type, *data):
        line, column = self.getpos()
        column += 1

        if type != 'text':
            self._stack[-1].append((type, (line, column), *data))
            return

        content, = data

        parts = []
        index = 0
        for sep in re.finditer(r'[^\S\n]*\n[^\S\n]*', content):
            parts.append((index, sep.start()))
            index = sep.end()
        parts.append((index, len(content)))

        index = 0
        for start, end in parts:
            if start == end:
                continue
            for char in content[index:start]:
                if char == '\n':
                    line += 1
                    column = 1
                else:
                    column += 1
            index = start
            self._stack[-1].append(
                ('text', (line, column), content[start:end])
            )

    def close_tags(self, index=0):
        while len(self._stack) - 1 > index:
            children = tuple(self._stack.pop())
            self._stack[-1][-1] = (*self._stack[-1][-1][:-1], children)

    def get_nodes(self):
        self.close()
        self.close_tags()
        return tuple(self._stack[0])


def parse(content):
    parser = Parser()
    parser.feed(content)
    return parser.get_nodes()
