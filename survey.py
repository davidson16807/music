import math 
import itertools

from pyaudio import PyAudio


# "track": maps time ⟶ waveheight
# "timbre": maps hertz ⟶ track, the track represents an elemental unit of track composition
sine     = lambda volume: lambda hertz: lambda time: int(volume*255*(math.sin(2*math.pi*time*hertz)+1)/2)

# combinations: fundamental operators of track composition
mix    =                     lambda *tracks: lambda time: sum(track(time) for track in tracks)
series = lambda track_hertz: lambda *tracks: lambda time: tracks[int((time*track_hertz)%len(tracks))](time)

# temperament: : semitones ⟶ hertz
equal = lambda a, steps: lambda step, octave=0: a*2**(octave+(step/steps))

# mode: : fulltones ⟶ semitones
mode = lambda halves: lambda tonic: lambda degree: tonic+halves[(degree-1)%len(halves)]+12*((degree-1)//len(halves))

# diatonic modes
ionian     = mode([0,2,4,5,7,9,11]) # AKA major diatonic, bilawal, shankarabharanam

major7 = ionian

notes = {
    'a♭' :-1,
    'a'  : 0,
    'a♯' : 1,
    'b♭' : 1,
    'b'  : 2,
    'c♭' : 2,
    'b♯' : 3,
    'c'  : 3,
    'c♯' : 4,
    'd♭' : 4,
    'd'  : 5,
    'd♯' : 6,
    'e♭' : 6,
    'e'  : 7,
    'f♭' : 7,
    'e♯' : 8,
    'f'  : 8,
    'f♯' : 9,
    'g♭' : 9,
    'g'  : 10,
    'g♯' : 11,
}

# chords: picking semitones to play together
chords = {
    'P1'   : [0], 
    'm3'   : [0,3],
    'M3'   : [0,4],
    'P4'   : [0,5],
    'P5'   : [0,7],
    ''     : [0,4,7], # major
    'M'    : [0,4,7], # major
    'm'    : [0,3,7], # minor
    'M6'   : [0,4,7,9], # major 6th
    'm6'   : [0,3,7,8], # minor 6th
    'M7'   : [0,4,7,11], # major 7th
    'm7'   : [0,3,7,10], # minor 7th
    'M9'   : [0,4,7,14], # major 9th
    'm9'   : [0,3,7,13], # minor 9th
    'M11'  : [0,4,7,18], # major 11th
    'm11'  : [0,3,7,17], # minor 11th
    '∅7'   : [0,3,6,10], # half diminished
    'M79'  : [0,4,7,11,14], # major 7th/9th
    'm79'  : [0,3,7,10,14], # minor 7th/9th
    'M911' : [0,4,7,11,18], # major 9th/11th
    'm911' : [0,3,7,10,17], # minor 9th/11th
    's2'   : [0,2,7], # suspended 2
    's4'   : [0,5,7], # suspended 4
    '+'    : [0,4,8], # augmented
    '-'    : [0,3,6], # diminished
    '7'    : [0,4,7,10], # dominant 7 / major minor 7
    '-7'   : [0,3,6,9 ], # diminished 7
    'mM7'  : [0,3,7,11], # minor major 7
    '+M7'  : [0,4,8,11], # augmented major
    '+7'   : [0,4,8,11], # augmented
    'add2' : [0,2,4,7],  # added 2nd
    'add4' : [0,4,5,7],  # added 4th
    'add9' : [0,4,7,14], # added 9th
}

# style: the manner of playing chords, maps root×quality ⟶ track
style = lambda temperament, timbre: lambda combination, sequence:  (
    lambda root, quality: combination(*[
        timbre(temperament(root+quality[interval%len(quality)], octave=interval//len(quality))) 
        for interval in sequence
    ])
)

progression = lambda style, key, chord_hertz, notation: (
    series(chord_hertz)(*[
        style(
            key(int(chord[0]))+('#' in chord)-('b' in chord), 
            chords[chord[1:].replace('b','').replace('#','')]
        ) 
        for chord in notation.split()
    ])
)

audio = PyAudio() # create PyAudio oobject
stream = audio.open(format=audio.get_format_from_width(1), # open stream
                    channels=1,
                    rate=41900,
                    output=True)

def play(track, duration, framerate): 
    stream.write(bytes(bytearray(tuple(track(time/framerate) for time in range(int(duration*framerate)))))) 

et12 = style(equal(440,12), sine(0.1))

def prompt(first, second, is_arpeggio):
    notation = f'{first} {second}'
    count = max(len(chords[first[1:]]), len(chords[second[1:]]))
    print(f'progression: {notation}')
    play(progression(et12(series(count) if is_arpeggio else mix, list(range(count))), major7(0), 1, notation), 2, 41900)
    return input('what do you feel? [press "enter" to replay, type "save" to save progress] ')

class Serialization:
    def __init__(self, delimiter):
        self.delimiter = delimiter
    def format(self, data):
        return '\n'.join([
            self.delimiter.join([str(cell) for cell in row]) 
            for row in data
        ])
    def parse(self, text):
        return [line.split(self.delimiter) for line in text.split('\n')]

filename = 'chords.tsv'
serialization = Serialization('\t')
try:
    with open(filename, 'r') as file:
        data = serialization.parse(file.read())
except:
    print('WARNING: an error occured while reading your save, future attempts to save may wipe old data')
    data = []
start_id = max([-1, *[int(i) for i, first, second, is_arpeggio, response in data]])

quality_sequence = 'M m s2 s4 + - M7 m7 7 mM7 M9 m9 M6 m6 M11 m11 ∅7 +M7 -7 +7 add2 add4 add9 M79 m79 M911 m911 m3 M3 P4 P5 P1 '.split()
root_sequence = list(range(12))
codes = {'', 'save'}

end_id = 0
for i, (first, second, is_arpeggio) in enumerate(itertools.product(quality_sequence, quality_sequence, [False,True])):
    if i > start_id:
        response = ''
        while response in codes:
            response = prompt('1'+first, '1'+second, is_arpeggio)
            if response == 'save':
                with open(filename, 'w') as file:
                    file.write(serialization.format(data))
        data.append((i, first, second, is_arpeggio, response))
    end_id = i

for i, (first, second, is_arpeggio) in enumerate(itertools.product(root_sequence, root_sequence, [False,True])):
    if i+end_id > start_id:
        response = ''
        while response in codes:
            response = prompt(first, second, is_arpeggio)
            if response == 'save':
                with open(filename, 'w') as file:
                    file.write(serialization.format(data))
        data.append((i+end_id, first, second, is_arpeggio, response))
