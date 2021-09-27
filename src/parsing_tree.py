from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

tags = {
    'ignore': ['head', 'a', 'map', 'style', 'meta', 'base',
               'link', 'script', 'noscript', 'img'],
    'table': ['table'],
    'table_cell': ['td', 'th'],
    'table_colspan': 'colspan',
    'table_row': ['tr'],
    'table_rowspan': 'rowspan'
}


class ParsingTree:
    def __init__(self, html):
        self.tags = tags
        self.bs = BeautifulSoup(html, 'html.parser')
        self.elements = self.parse_tree(self.bs)

    def parse_tree(self, vertex):
        elements = []
        if self.is_table(vertex):
            elements.append(('table', self.parse_table_tree(vertex)))
        else:
            if self.is_navigable(vertex):
                for child in vertex.children:
                    elements += self.parse_tree(child)
            elif type(vertex) == NavigableString:
                text = str(vertex)
                if not self.is_void(text):
                    elements.append(('text', text))
        return elements

    def parse_table_tree(self, vertex):
        return self.parse_meta_tree(
            vertex,
            self.is_table_row,
            self.parse_row_tree)

    def parse_row_tree(self, vertex):
        return self.parse_meta_tree(
            vertex,
            self.is_table_cell,
            self.parse_cell_tree)

    def parse_cell_tree(self, vertex):
        row_span, col_span = self.get_span(vertex)
        text = ' | '.join(self.parse_string_tree(vertex))
        return row_span, col_span, text

    @staticmethod
    def get_text(string):
        return str(string) if string else ''

    @staticmethod
    def is_void(text):
        if len(text.strip()) == 0:
            return True
        return False

    def parse_string_tree(self, vertex):
        return self.parse_meta_tree(
            vertex,
            self.is_string,
            self.get_text)

    def is_string(self, vertex):
        if (type(vertex) == NavigableString
                and not self.is_void(str(vertex))):
            return True

    def get_span(self, cell):
        rowspan, colspan = 1, 1
        if self.tags['table_rowspan'] in cell.attrs:
            rowspan = int(cell[self.tags['table_rowspan']])
        if self.tags['table_colspan'] in cell.attrs:
            colspan = int(cell[self.tags['table_colspan']])
        return rowspan, colspan

    def parse_meta_tree(self, vertex, condition, parse_result):
        meta_tags = []
        if condition(vertex):
            meta_tags.append(parse_result(vertex))
        elif self.is_navigable(vertex):
            for child in vertex.children:
                meta_tags += self.parse_meta_tree(child, condition,
                                                  parse_result)
        return meta_tags

    def is_table_row(self, vertex):
        return vertex.name in self.tags['table_row']

    def is_table_cell(self, vertex):
        return vertex.name in self.tags['table_cell']

    def is_navigable(self, tag):
        if type(tag) not in [Tag, BeautifulSoup]:
            return False
        if tag.name in self.tags['ignore']:
            return False
        return True

    def is_table(self, tag):
        if tag.name in self.tags['table']:
            return True
        return False
