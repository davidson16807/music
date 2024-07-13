import re

import notated

class ScientificPitch:
    def __init__(self, notes, preferred_accidental='♯'):
        self.semitone_for_note = {**notes, **{note.replace('♭','b').replace('♯','#'): semitone for note, semitone in notes.items()}}
        self.note_for_semitone = {semitone : note for note, semitone in self.semitone_for_note.items() if (preferred_accidental in note) or len(note)==1}
    def parse(self, text):
        return ( 
            (self.semitone_for_note[re.search('^[a-gA-G][♭♯#b]?', text).group(0).lower()] + 9)%12 + 
            (int(re.search('[0-9]+$', text).group(0)) - 4)*12 - 9
        )
    def format(self, semitone):
        return str(self.note_for_semitone[semitone%12]) + str((semitone+9)//12 + 4)

# parse and format copy-pasted content from onlinesequencer.net
class OnlineSequencer:
    def __init__(self, instrument, note_length):
        self.demarcation = Demarcation(Tokenization(list, ';', Tokenization(list, ' ', Identity())), 'Online Sequencer:46419:', ':')
        self.pitch = ScientificPitch(notated.notes, '#')
        self.instrument = instrument
        self.note_length = note_length
    def parse(self, staff):
        notes = demarcation.parse(staff)
        length = max([i for i, pitch, length, instrument in notes])
        staff = [[] for i in range(length)]
        for i, pitch, length, instrument in notes:
            staff[int(i)].append(self.pitch.parse(pitch.lower()))
        return staff
    def format(self, staff):
        notes = [[str(i), self.pitch.format(semitone).upper(), str(self.note_length), str(self.instrument)] 
            for i, beat in enumerate(staff) 
            for semitone in beat]
        return self.demarcation.format(notes)

# pitch = ScientificPitch(notes)
# for semitone in [-10,-9, -1,0,1,2,3,4, 0,12,-12]:
#     print(pitch.format(semitone))
#     print(semitone, pitch.parse(pitch.format(semitone)))

class DelimitedLookup:
    def __init__(self, item_delimiter, dict_delimiter='\n'):
        self.item_delimiter = item_delimiter
        self.dict_delimiter = dict_delimiter
    def format(self, data):
        return self.dict_delimiter.join([
            self.item_delimiter.join([str(cell) for cell in [*key, value]]) 
            for key,value in data.items()
        ])
    def parse(self, text):
        return {
            tuple(cells[:-1]) : cells[-1] 
            for cells in [line.split(self.item_delimiter) for line in text.split('\n') ]
        }

class Identity:
    def __init__(self):
        pass
    def format(self, data):
        return data
    def parse(self, text):
        return text

class Demarcation:
    def __init__(self, body, ldefault, rdefault, lregex=None, rregex=None):
        self.body = body
        self.ldefault = ldefault
        self.rdefault = rdefault
        self.lregex = lregex if lregex else ldefault
        self.rregex = rregex if rregex else rdefault
    def format(self, data):
        return ''.join([self.ldefault, self.body.format(data), self.rdefault])
    def parse(self, text):
        stripped = re.sub(self.lregex,'',text) if self.lregex else text.lstrip(self.ldefault)
        stripped = re.sub(self.rregex,'',text) if self.rregex else text.rstrip(self.rdefault)
        return self.body.parse(stripped)

class Tokenization:
    def __init__(self, container, delimiter, element):
        self.container = container
        self.element = element
        self.delimiter = delimiter
    def format(self, data):
        return self.delimiter.join([self.element.format(element) for element in data])
    def parse(self, text):
        return self.container([self.element.parse(element) for element in text.split(self.delimiter)])

class Composition:
    def __init__(self, shallow, deep):
        self.shallow = shallow
        self.deep = deep
    def format(self, data):
        return self.deep.format(self.shallow.format(data))
    def parse(self, text):
        return self.shallow.parse(self.deep.parse(text))

class Involution:
    def __init__(self, involution):
        self.involution = involution
    def format(self, data):
        return self.involution(data)
    def parse(self, text):
        return self.involution(text)

