import re

class ScientificPitch:
    def __init__(self, notes, preferred_accidental='♯'):
        self.semitone_for_note = {**notes, **{note.replace('♭','b').replace('♯','#'): semitone for note, semitone in notes.items()}}
        self.note_for_semitone = {semitone : note for note, semitone in notes.items() if preferred_accidental in note or len(note)==1}
        print(self.note_for_semitone)
    def parse(self, text):
        return ( 
            (self.semitone_for_note[re.search('^[a-gA-G][♭♯#b]?', text).group(0).lower()] + 9)%12 + 
            (int(re.search('[0-9]+$', text).group(0)) - 4)*12 - 9
        )
    def format(self, semitone):
        return str(self.note_for_semitone[semitone%12]) + str((semitone+9)//12 + 4)

# pitch = ScientificPitch(notes)
# for semitone in [-10,-9, -1,0,1,2,3,4, 0,12,-12]:
#     print(pitch.format(semitone))
#     print(semitone, pitch.parse(pitch.format(semitone)))

class DelimitedTuples:
    def __init__(self, delimiter):
        self.delimiter = delimiter
    def format(self, data):
        return '\n'.join([
            self.delimiter.join([str(cell) for cell in row]) 
            for row in data
        ])
    def parse(self, text):
        return [line.split(self.delimiter) for line in text.split('\n')]

class DelimitedLookup:
    def __init__(self, delimiter):
        self.delimiter = delimiter
    def format(self, data):
        return '\n'.join([
            self.delimiter.join([str(cell) for cell in [*key, value]]) 
            for key,value in data.items()
        ])
    def parse(self, text):
        return {
            tuple(cells[:-1]) : cells[-1] 
            for cells in [line.split(self.delimiter) for line in text.split('\n') ]
        }

class Composition:
    def __init__(self, shallow, deep):
        self.shallow = shallow
        self.deep = deep
    def format(self, data):
        return self.deep.format(self.shallow.format(data))
    def parse(self, text):
        return self.shallow.parse(self.deep.parse(text))

class Iteration:
    def __init__(self, element):
        self.element = element
    def format(self, data):
        return self.element.format(data)
    def parse(self, text):
        return self.element.parse(text)

class Involution:
    def __init__(self, involution):
        self.involution = involution
    def format(self, data):
        return self.involution(data)
    def parse(self, text):
        return self.involution(text)

