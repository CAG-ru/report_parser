class Text:
    def __init__(self, text_list):
        self.text_list = text_list

    def __str__(self):
        return '\n'.join(self.text_list)

    def contains(self, pattern):
        searchable = ' '.join(self.text_list).lower()
        return pattern.lower() in searchable