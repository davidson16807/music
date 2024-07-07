
class DelimitedTable:
    def __init__(self, delimiter):
        self.delimiter = delimiter
    def format(self, data):
        return '\n'.join([
            self.delimiter.join([str(cell) for cell in row]) 
            for row in data
        ])
    def parse(self, text):
        return [line.split(self.delimiter) for line in text.split('\n')]

class Composition:
    def __init__(self, shallow, deep):
        self.shallow = shallow
        self.deep = deep
    def format(self, data):
        return self.deep.format(self.shallow.format(data))
    def parse(self, text):
        return self.shallow.parse(self.deep.parse(data))
