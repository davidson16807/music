# standard
import math 
import os
import sys

# 3rd-party
from pyaudio import PyAudio

# in-house
sys.path.append(os.path.realpath('..'))
import notated
from notated import notes
from notated import (ionian, aeolian, dorian, phrygian, lydian, mixolydian, locrian, major7, minor7)
from notated import (jazz_minor, harmonic_minor, major5, blues_major, egyptian, minor5, blues_minor)

import played
from played import series, mix, progression

# progression = lambda :

'''
hertz = 440 
track=series(1)(
    series(3)(
        square(hertz, volume),
        square(9/8*hertz, volume),
        square(10/8*hertz, volume),
    ),
    series(3)(
        saw(hertz, volume),
        saw(9/8*hertz, volume),
        saw(10/8*hertz, volume),
    ),
    series(3)(
        triangle(hertz, volume),
        triangle(9/8*hertz, volume),
        triangle(10/8*hertz, volume),
    ),
    series(3)(
        parabola(hertz, volume),
        parabola(9/8*hertz, volume),
        parabola(10/8*hertz, volume),
    ),
    series(3)(
        played.sine(hertz, volume),
        played.sine(9/8*hertz, volume),
        played.sine(10/8*hertz, volume),
    ),
)
'''

# track=series(1)(
#     series(3)(
#         timbre(half(0)),
#         timbre(half(4)),
#         timbre(half(7)),
#     ),
# )
et12 = played.style(played.equal(432,12), played.sine(0.1))
# et12 = played.style(played.equal(440,12), played.sine(0.1))
harmony = et12(mix, [0,1,2])
melody = et12(series(3), [0,1,2])
key = major7(notes['d'])
# track = series(3/2)(*[harmony(4, chord) for chord in triads.values()]) # iterates through harmonic chords
# track = series(3/2)(*[melody(0, chord) for chord in triads.values()]) # iterates through arpeggiated chords

pyaudio = PyAudio()
play = played.sound(
    pyaudio.open(format=pyaudio.get_format_from_width(1), # open stream
        channels=1,
        rate=41900,
        output=True
    ), 41900
)

# progressions
four_chords = '1 5 6m 4' # so coined by Axis of Awesome, examples: basically everything
sensitive_female = '6m 4 1 5' # so coined by Boston Globe, example: zombie, snow, real world, poker face, otherside
doowop = '1 6m 4 5'
pachabel = '8 5 6m 3m 4 1 4 5'
hallelujah = '1 6m 1 6m 4 5 1 5 1 4 5 6m 4 5 37 6m 4 6m 4 1 5 1'
anime_theme = '47 5m7 3m7 6m' # 
rickroll = '4m9 7m7 5m7 1m' # 
dire_dire_docks = '1 7 1 7 6m 7' #
# dire_dire_docks2 = '4M 3m 2m 1M' #
# dire_dire_docks = '4M 3m 2m 1- 2m 5M 1M' #
dollars_and_cents = '1 1 1m 1m' #[0,0,1,2,3,2,3,2,3,6]
morning_bell = '2m 2M7 2m 2M7 1s2 5' #[0,0,1,2,3,2,3,2,3,6]
daydreaming = '6m 1 1 4M7 6m 1 1 4M7 6m 1 1 2s2 2m 2s2 2m 2s2 2m 2s2 2m' #[6,0,1,2,1,0] # something doesn't play right here
everything_in_its_right_place = '5 1 2b 3b' #[0,0,1,2,3,2,3,2,3,6]
epitaph = '1 5m7'
last_of_us = '1m 1s2 1m 1s2 3 1m'
test = '1 1b 4 4b 5 5b' #[0,0,1,2,3,2,3,2,3,6]
chocobo = '5 4'
revived_power = '2 1 3 4 5 6 2 1 1 7b 1 7b 1 2m 6b 2m 6b 2 2 6m 2m 6m 2b 1 2 6m 2 5 2 6m 2 5 2 7b 2 1 7b 2 1'
cosmos = '1 5 1 6m 4 1 5 5 1 4 1 4 1 4 1 4 1'
koyaanisqatsi1 = '5 4 3b'
koyaanisqatsi2 = '5 2m 1m 2 5m 2'


# track1 = progression(played.style(played.equal(440/2,12), parabola(0.1))(mix, monad),       key, 1, pachabel)
# track2 = progression(played.style(played.equal(440,12), played.sine(0.1))(mix, [0,1,2]),           key, 1, pachabel)
# track3 = progression(played.style(played.equal(440,12), triangle(0.1))(series(3), [0,1,2]), key, 1, pachabel)
# track = series(1/8)( 
#     mix(track1),
#     mix(track1, track2),
#     mix(track1, track2, track3),
# ) # I'll see your ass in hell, Pachabel!

c = notes['c']
# track = progression(et12(series(4/2), [0,1,0,2]), notated.chord(phrygian(c)), 1/2,  '1m 4m 5m') # brooding
# track = progression(et12(series(4/2), [0,1,0,2]), notated.chord(phrygian(c)), 1/2,  '1m 1m 6 7') # brooding
# track = progression(et12(series(4/2), [0,1,0,2]), notated.chord(phrygian(c)), 1/2,  '1m 6 4m 5') # brooding
# track = progression(et12(series(4/2), [0,1,0,2]), notated.chord(phrygian(c)), 1/2,  '1 2') # brooding
# track = progression(et12(series(4/2), [0,1,0,2]), notated.chord(locrian(c)), 1/2,  '1 2') # brooding
# track = progression(et12(series(4/2), [0,1,0,2]), notated.chord(major7(c)), 1/2,  '1m 3 2m 1m') # mysterious
# track = progression(et12(series(4/2), [0,1,0,2]), notated.chord(major7(c)), 1/2,  '1m 6 4m') # brooding
# track = progression(et12(series(4/2), [0,1,0,2]), notated.chord(major7(c)), 1/2,  '1m 7 3m 2m') # haunted
# track = progression(et12(series(3/2), [0,2,1]), notated.chord(major7(c)), 1/2,  '1m 7 4m 5m') # donnie darko
# track = progression(et12(mix, [0,1,2]), notated.chord(major7(c)), 1/2,  '1m 6 3 7') # brooding
# track = progression(et12(series(5/1), [0,1,2,3,4,3,2]), notated.chord(phrygian(c)), 1/1,  '1m 6 1M9') # evil genius boss fight
# track = progression(et12(series(7/1), [0,1,2,3,4,3,2]), notated.chord(phrygian(c)), 1/1,  '1m 6 3 1M9') # boss fight
# track = progression(et12(series(5/1), [0,1,2,3,4,3,2]), notated.chord(major7(c)), 1/1,  '1m 3 2m 1m') # unfolding mystery
# track = progression(et12(series(5/1), [0,1,2,3,4,3]), notated.chord(phrygian(c)), 1/2,  '1 1b 4 4b 5 5b') # wacky science lab
# track = progression(et12(series(5/1), [0,1,2]), notated.chord(major7(c)), 1/2,  '1m 3 1m 2 1m 7 1m') # "its coming from inside the house!"
# track = progression(et12(series(4/1), [0,3,4,5]), notated.chord(mixolydian)(notes['a']), 1/1,  '1 5m7') # epitaph, ff6
# track = progression(et12(series(4/1), [0,3,4,5]), notated.chord(mixolydian)(c), 1/1,  '4 5') # chocobo
# track = progression(et12(mix, [0,1,2]), notated.chord(major7(c)), 1/2,  '1m 1s2 1m 1s2 3 1m') # last of us
# track = progression(et12(series(3/2), [2,0,1]), notated.chord(major7(notes[)'a']), 1/2,  cosmos) 
# track = progression(et12(series(3), [0,1,2]), notated.chord(major7(c)), 1, doowop)
# track = progression(et12(mix, [1,0,1,2]), notated.chord(major7(notes[)'g']), 1, koyaanisqatsi1)
# track = progression(et12(mix, [0,1,2]), notated.chord(major7(notes[)'d']), 1/2,  '5 1 3m 5') # higher and higher
# track = progression(et12(series(6/2), [0,1,2,3,2,1]), notated.chord(major7(c)), 1/2,  '1 5 2m 5') # walking up and down fifths, "love song" vibes
# track = progression(et12(series(6/2), [0,1,2,3,2,1]), notated.chord(major7(c)), 1/2,  '1 5 2 5') # walking up and down fifths, "sing song", uninterestingly happy
# track = progression(et12(series(6/2), [0,1,2,3,2,1]), notated.chord(major7(c)), 1/2,  '8 5 2m 5') # walking up and down fifths, "sing song", uninterestingly happy
# track = progression(et12(series(3/1), [0,1,2]), notated.chord(major7(c)), 1/1,  '1m 1m 1m 1m 1m 1m 1m 1m 6 6 2b 2b 57 1m 5s4 57') # moonlight sonata, I tried

# track = progression(et12(series(7/2), [0,1,2,4,3,2,1,0]), notated.chord(major7(c)), 1/2,  revived_power) 
# track = progression(et12(series(3), [0,1,2]), notated.chord(major7(notes[)'d']), 1, pachabel)
# track = progression(et12(series(6/2), [0,1,2,3,2,1]), notated.chord(major7(c)), 1/2,  hallelujah)
# track = progression(et12(mix, [0,1,2]), notated.chord(major7(c)), 1/2,  morning_bell)
track = progression(et12(series(10/2), [0,0,1,2,3,2,3,2,3,6]), notated.chord(major7(c)), 1/2, dollars_and_cents)

duration = len(hallelujah)*2

play(track, duration)

# vii IV I V ii


'''
relation between music and feeling:
it is asserted that there exists a map:

music ⟶ feeling

Which accepts a music composition and determines what the average member of a western audience would feel in listening to it.
By iterative approximation, the job of a composer is typically to produce an inverse:

feeling ⟶ music

that maps feelings to an instance of music such that the following commutes:

feeling ↔ music

The question we would like to answer is whether a surrogate can be constructed to approximate this map

The terms "feeling" and "music" are no where formally defined and we do not presume any incontrovertible definitions will be found,
however our surrogate must necessarily create representative data structures for both. 
We suspect that "feeling" is especially difficult to represent,
so our first task is to articulate how "feeling" varies in ways that that can be represent musically.
We will restrict ourselves to western canon in this treatment.

heart beat  tempo

'''