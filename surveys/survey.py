# standard
import itertools
import os
import sys

# 3rd-party
from pyaudio import PyAudio

# in-house
sys.path.append(os.path.realpath('..'))
import played
import notated
import stored
import drawn

pyaudio = PyAudio()
play = played.sound(
    pyaudio.open(format=pyaudio.get_format_from_width(1), # open stream
        channels=1,
        rate=41900,
        output=True
    ), 41900
)

et12 = played.style(played.equal(440,12), played.sine(0.1))

sequences = {
    'harmonic': lambda count: list(range(count)),
    'ascending': lambda count: list(range(count)),
    'descending': lambda count: list(range(count-1, -1, -1)),
}

def prompt(first, second, sequence):
    print(f'progression: {first} → {second}, {sequence}')
    count = max(
        len(notated.qualities[notated.quality(first)]), 
        len(notated.qualities[notated.quality(second)])
    )
    play(
        played.progression(
            et12(played.mix if sequence=='harmonic' else played.series(count), sequences[sequence](count)), 
            notated.chord(notated.major7(0)), 1, [first, second]
        ), 2
    )
    return input('what do you feel? [press "enter" to replay, type "save" to save progress] ')

combination_sequence = 'harmonic ascending descending'.split()
quality_sequence = 'M m s2 s4 + - M7 m7 7 mM7 M9 m9 M6 m6 M11 m11 ∅7 +M7 -7 +7 add2 add4 add9 M79 m79 M911 m911 m3 M3 P4 P5 P1 '.split()
root_sequence = list(range(12))
interval_sequence = [1,-1,5,-5,4,-4,3,-3,2,-2,7,-7,6,-6,9,-9,8,-8,11,-11,10,-10]
codes = {'', 'save'}

progression_sequence = itertools.chain(
    ((f'1{first}', f'1{second}', combination) for (first, second, combination) in itertools.product(quality_sequence, quality_sequence, combination_sequence)),
    ((f'{first+1}M', f'{first+interval+1}M', combination) for (first, interval, combination) in itertools.product(root_sequence, interval_sequence, combination_sequence)),
)

chords_filename = 'chords.tsv'
storage = stored.DelimitedLookup('\t')
with open(chords_filename, 'r') as file:
    data = storage.parse(file.read())

for parameters in progression_sequence:
    if parameters not in data:
        response = ''
        while response in codes:
            response = prompt(*parameters)
            if response == 'save':
                with open(chords_filename, 'w') as file:
                    file.write(storage.format(data))
        data[parameters] = response
