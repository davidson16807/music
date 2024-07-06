# standard
import math 
import itertools
import re

# 3rd-party
from pyaudio import PyAudio

# in-house
import played
import notated
from notated import qualities, root, quality


pyaudio = PyAudio()
play = played.sound(
    pyaudio.open(format=pyaudio.get_format_from_width(1), # open stream
        channels=1,
        rate=41900,
        output=True
    ), 41900
)

et12 = played.style(played.equal(440,12), played.sine(0.1))

def prompt(first, second, is_arpeggio):
    progression_string = f'{first} {second}'
    print(f'progression: {progression_string}')
    count = max(len(qualities[quality(first)]), len(qualities[quality(second)]))
    play(
        played.progression(
            et12(played.series(count) if is_arpeggio else played.mix, list(range(count))), 
            notated.chord(notated.major7(0)), 1, progression_string
        ), 2
    )
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

qualities_filename = 'qualities.tsv'
roots_filename = 'roots.tsv'
serialization = Serialization('\t')
try:
    with open(roots_filename, 'r') as file:
        data = serialization.parse(file.read())
except:
    print('WARNING: an error occured while reading your save, future attempts to save may wipe old data')
    data = []
start_id = max([-1, *[int(i) for i, first, second, is_arpeggio, response in data]])

quality_sequence = 'M m s2 s4 + - M7 m7 7 mM7 M9 m9 M6 m6 M11 m11 ∅7 +M7 -7 +7 add2 add4 add9 M79 m79 M911 m911 m3 M3 P4 P5 P1 '.split()
root_sequence = list(range(12))
interval_sequence = [1,-1,5,-5,4,-4,3,-3,2,-2,7,-7,6,-6,9,-9,8,-8,11,-11,10,-10]
codes = {'', 'save'}

for i, (first, interval, is_arpeggio) in enumerate(itertools.product(root_sequence, interval_sequence, [False,True])):
    if i > start_id:
        response = ''
        while response in codes:
            response = prompt(str(first), str(first+interval), is_arpeggio)
            if response == 'save':
                with open(roots_filename, 'w') as file:
                    file.write(serialization.format(data))
        data.append((i, str(first), str(first+interval), is_arpeggio, response))

# for i, (first, second, is_arpeggio) in enumerate(itertools.product(quality_sequence, quality_sequence, [False,True])):
#     if i > start_id:
#         response = ''
#         while response in codes:
#             response = prompt('1'+first, '1'+second, is_arpeggio)
#             if response == 'save':
#                 with open(qualities_filename, 'w') as file:
#                     file.write(serialization.format(data))
#         data.append((i, first, second, is_arpeggio, response))

