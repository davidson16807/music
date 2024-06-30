import math 
from pyaudio import PyAudio
audio = PyAudio() # create PyAudio oobject
stream = audio.open(format=audio.get_format_from_width(1), # open stream
                    channels=1,
                    rate=41900,
                    output=True)

# "track": maps time ⟶ waveheight
# "timbre": maps hertz ⟶ track, the track represents an elemental unit of track composition
# NOTE: suck it, python, stop imposing dogma on us and give us arrow notation
sine     = lambda volume: lambda hertz: lambda time: int(volume*255*(math.sin(2*math.pi*time*hertz)+1)/2)
square   = lambda volume: lambda hertz: lambda time: int(volume*255*((time*hertz)%1.0 > 0.5))
saw      = lambda volume: lambda hertz: lambda time: int(volume*255*((time*hertz)%1.0))
triangle = lambda volume: lambda hertz: lambda time: int(volume*255*abs(((time*hertz)%2.0) - 1))
parabol  = lambda t: (1-t)*(1-t*t) + t*(t-1)**2 # so named because it is the lead-in to "parabola"
parabola = lambda volume: lambda hertz: lambda time: int(volume*255*parabol(abs((2*(time*hertz+1)%2.0) - 1)))
''' ^^^The `parabola` wave is an interpolation between 
parabolic approximations of a cosine's crest and trough where the interpolant "t" is a triangle wave.'''

# combinations: fundamental operators of track composition
mix    =                     lambda *tracks: lambda time: sum(track(time) for track in tracks)
series = lambda track_hertz: lambda *tracks: lambda time: tracks[int((time*track_hertz)%len(tracks))](time)

# temperament: : semitones ⟶ hertz
equal = lambda a, steps: lambda step, octave=0: a*2**(octave+(step/steps))
pythagorean = lambda base_hertz: lambda step, octave=0: (
        base_hertz*
        (2**octave+step//12)*
        (3**[0,-5,2,-3,4,-1,-6,6,1,-4,3,-2,5][step%12])*
        (2**[0,8,-3,5,-6,2,10,-9,-1,7,-4,4,-7][step%12])
    )
quarter_comma_meantone = lambda base_hertz: lambda step, octave=0: (
        base_hertz*
        (2**octave+step//12)*
        ([1.0000,1.0449,1.1180,1.1963,1.2500,1.3375,1.3975,1.4953,1.5625,1.6719,1.7889,1.8692][step%12])
    )
werckmeister1 = lambda base_hertz: lambda step, octave=0: (
        base_hertz*
        (2**octave+step//12)*
        (2**([0,90,192,294,390,498,588,696,792,888,996,1092][step%12]/1200))
    )
werckmeister2 = lambda base_hertz: lambda step, octave=0: (
        base_hertz*
        (2**octave+step//12)*
        (2**([0,85.8,195.3,295.0,393.5,498.0,590.2,693.3,787.7,891.6,1003.8,1088.3][step%12]/1200))
    )
werckmeister3 = lambda base_hertz: lambda step, octave=0: (
        base_hertz*
        (2**octave+step//12)*
        (2**([0,96,204,300,396,504,600,702,792,900,1002,1098][step%12]/1200))
    )
werckmeister4 = lambda base_hertz: lambda step, octave=0: (
        base_hertz*
        (2**octave+step//12)*
        (2**([0,91,196,298,395,498,595,698,793,893,1000,1097][step%12]/1200))
    )

# mode: : fulltones ⟶ semitones
mode = lambda halves: lambda tonic: lambda degree: tonic+halves[(degree-1)%len(halves)]+12*((degree-1)//len(halves))

# timbre ∘ temprament ∘ mode

# diatonic modes
ionian     = mode([0,2,4,5,7,9,11]) # AKA major diatonic, bilawal, shankarabharanam
aeolian    = mode([0,2,3,5,7,8,10]) # AKA natural minor, descending melodic minor scale
dorian     = mode([0,2,3,5,7,9,10])
phrygian   = mode([0,1,3,5,7,8,10])
lydian     = mode([0,2,4,6,7,9,11])
mixolydian = mode([0,2,4,5,7,9,10])
locrian    = mode([0,1,3,5,6,8,10])
jazz_minor = mode([0,2,3,5,7,9,11]) # AKA ionian♭3, dorian♯7, ascending melodic minor scale
harmonic_minor = mode([0,2,3,5,7,8,11]) # AKA aeolian♯7

major7 = ionian
minor7 = aeolian

# pentatonic modes
major5     = mode([0,2,4,7,9]) # AKA major pentatonic, gōng, bhoopali, mohanam, mullaittīmpāṇi
blues_major= mode([0,2,5,7,9]) # AKA ritsusen, yo, zhǐ, durga, shuddha saveri, koṉṟai
egyptian   = mode([0,2,5,7,10])# AKA suspended, shāng, megh, madhyamavati, centurutti
minor5     = mode([0,3,5,7,10])# AKA yǔ, dhani, dhuddha dhanyasi, āmpal
blues_minor= mode([0,3,5,8,10])# AKA man gong, jué, malkauns, hindolam, intaḷam

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
    'monad' : [0], # functional programmers love their monads, right?
    'power' : [0,7],
    ''     : [0,4,7], # major
    'M'    : [0,4,7], # major
    'm'    : [0,3,7], # minor
    's2'   : [0,2,7], # suspended 2
    's4'   : [0,5,7], # suspended 4
    '+'    : [0,4,8], # augmented
    '-'    : [0,3,6], # diminished
    'M7'   : [0,4,7,11], # major 7th
    'm7'   : [0,3,7,10], # minor 7th
    '7'    : [0,4,7,10], # dominant 7 / major minor 7
    '-7'   : [0,3,6,9 ], # diminished
    'mM7'  : [0,3,7,11], # minor major 7
    '+M7'  : [0,4,8,11], # augmented major
    '+7'   : [0,4,8,11], # augmented
    'M9'   : [0,4,7,11,14], # major 9th
    'm9'   : [0,3,7,10,14], # minor 9th
}

# style: the manner of playing chords, maps root×chord ⟶ track
style = lambda temperament, timbre: lambda combination, sequence:  (
    lambda root, chord: combination(*[
        timbre(temperament(root+chord[interval%len(chord)], octave=interval//len(chord))) 
        for interval in sequence
    ])
)

# lifts or lowers by one full tone an interval that is reported in semitones
class Diatonic:
    def __init__(self):
        pass
    def lift(self, full):
        return (full + (1 if full % 12 in {2,7} else 2))
    def lower(self, full):
        return (full - (1 if full % 12 in {3,8} else 2))

class Tonnetz:
    def __init__(self, diatonic):
        self.diatonic = diatonic
    def parallel(self, chord): # swap major and minor, this operation is involute
        is_major = (chord[1]%12) - (chord[0]%12) > 3
        first, third, fifth = chord
        return [first, third+(-1 if is_major else 1), fifth]
    def relative(self, chord): # move up or down a full tone
        is_major = (chord[1]%12) - (chord[0]%12) > 3
        first, third, fifth = chord
        return ([self.diatonic.lift(fifth)-12, first, third] if is_major
            else [third, fifth, self.diatonic.lower(first)+12])
    def leading(self, chord): # move up or down a semitone
        is_major = (chord[1]%12) - (chord[0]%12) > 3
        first, third, fifth = chord
        return ([third, fifth, first+11] if is_major
            else [fifth-11, first, third])

tonnetz = Tonnetz(Diatonic())
tonnetz.relative([0,4,7])
# breakpoint()

et12 = style(equal(440,12), sine(0.1))(mix, [0,1,2])
c = notes['c']
# track=series(1)(
#     et12(c, [0,4,7]),
#     et12(c, tonnetz.relative([0,4,7])),
#     et12(c, tonnetz.relative(tonnetz.relative([0,4,7]))),
#     et12(c, [0,4,7]),
#     et12(c, tonnetz.leading([0,4,7])),
#     et12(c, tonnetz.leading(tonnetz.leading([0,4,7]))),
#     et12(c, [0,4,7]),
#     et12(c, tonnetz.parallel([0,4,7])),
#     et12(c, tonnetz.parallel(tonnetz.parallel([0,4,7]))),
# )

class NeoRiemannianProgression:
    def __init__(self, tonnetz):
        self.tonnetz = tonnetz
        self.code = {
            'l': tonnetz.leading,
            'p': tonnetz.parallel,
            'r': tonnetz.relative,
        }
    def progression(self, style, chord_hertz, root, start, notation):
        chord = [root+interval for interval in start]
        chords = [chord]
        for transform in notation.split():
            for character in transform:
                chord = self.code[character](chord)
            chords.append(chord)
        return series(chord_hertz)(*[
            style(0, chord)
            for chord in chords
        ])

et12 = style(equal(440,12), sine(0.1))
nrp = NeoRiemannianProgression(tonnetz)
# track = nrp.progression(et12(mix, [2,1,0]), 1/3, notes['f'], chords['M'], 'rlp') # tifa
track = nrp.progression(et12(series(5/2), [0,2,1,0,-1]), 1/2, notes['c'], chords['M'], 'lrlr lrlr') # et

# progression = lambda :

hertz = 440 
# hertz = 432

'''
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
        sine(hertz, volume),
        sine(9/8*hertz, volume),
        sine(10/8*hertz, volume),
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
part = style(equal(440,12), sine(0.1))
harmony = part(mix, [0,1,2])
melody = part(series(3), [0,1,2])
key = major7(notes['d'])
# track = series(3/2)(*[harmony(4, chord) for chord in triads.values()]) # iterates through harmonic chords
# track = series(3/2)(*[melody(0, chord) for chord in triads.values()]) # iterates through arpeggiated chords

progression = lambda style, key, chord_hertz, notation: (
    series(chord_hertz)(*[
        style(
            key(int(chord[0]))+('#' in chord)-('b' in chord), 
            chords[chord[1:].replace('b','').replace('#','')]
        ) 
        for chord in notation.split()
    ])
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
daydreaming = '6m 1 1 4M7 6m 1 1 4M7 6m 1 1 2s2 2m 2s2 2m 2s2 2m 2s2 2m' #[6,0,1,2,1,0] # something doesn't sound right here
everything_in_its_right_place = '5 1 2b 3b' #[0,0,1,2,3,2,3,2,3,6]
epitaph = '1 5m7'
last_of_us = '1m 1s2 1m 1s2 3 1m'
test = '1 1b 4 4b 5 5b' #[0,0,1,2,3,2,3,2,3,6]
chocobo = '5 4'
revived_power = '2 1 3 4 5 6 2 1 1 7b 1 7b 1 2m 6b 2m 6b 2 2 6m 2m 6m 2b 1 2 6m 2 5 2 6m 2 5 2 7b 2 1 7b 2 1'
cosmos = '1 5 1 6m 4 1 5 5 1 4 1 4 1 4 1 4 1'
koyaanisqatsi1 = '5 4 3b'
koyaanisqatsi2 = '5 2m 1m 2 5m 2'

et12 = style(equal(440,12), sine(0.1))

# track1 = progression(style(equal(440/2,12), parabola(0.1))(mix, monad),       key, 1, pachabel)
# track2 = progression(style(equal(440,12), sine(0.1))(mix, [0,1,2]),           key, 1, pachabel)
# track3 = progression(style(equal(440,12), triangle(0.1))(series(3), [0,1,2]), key, 1, pachabel)
# track = series(1/8)( 
#     mix(track1),
#     mix(track1, track2),
#     mix(track1, track2, track3),
# ) # I'll see your ass in hell, Pachabel!

# track = progression(et12(series(4/2), [0,1,0,2]), phrygian(c), 1/2,  '1m 4m 5m') # brooding
# track = progression(et12(series(4/2), [0,1,0,2]), phrygian(c), 1/2,  '1m 1m 6 7') # brooding
# track = progression(et12(series(4/2), [0,1,0,2]), phrygian(c), 1/2,  '1m 6 4m 5') # brooding
# track = progression(et12(series(4/2), [0,1,0,2]), phrygian(c), 1/2,  '1 2') # brooding
# track = progression(et12(series(4/2), [0,1,0,2]), locrian(c), 1/2,  '1 2') # brooding
# track = progression(et12(series(4/2), [0,1,0,2]), major7(c), 1/2,  '1m 3 2m 1m') # mysterious
# track = progression(et12(series(4/2), [0,1,0,2]), major7(c), 1/2,  '1m 6 4m') # brooding
# track = progression(et12(series(4/2), [0,1,0,2]), major7(c), 1/2,  '1m 7 3m 2m') # haunted
# track = progression(et12(series(3/2), [0,2,1]), major7(c), 1/2,  '1m 7 4m 5m') # donnie darko
# track = progression(et12(mix, [0,1,2]), major7(c), 1/2,  '1m 6 3 7') # brooding
# track = progression(et12(series(5/1), [0,1,2,3,4,3,2]), phrygian(c), 1/1,  '1m 6 1M9') # evil genius boss fight
# track = progression(et12(series(7/1), [0,1,2,3,4,3,2]), phrygian(c), 1/1,  '1m 6 3 1M9') # boss fight
# track = progression(et12(series(5/1), [0,1,2,3,4,3,2]), major7(c), 1/1,  '1m 3 2m 1m') # unfolding mystery
# track = progression(et12(series(6/2), [0,1,2,3,2,1]), major7(c), 1/2,  hallelujah)
# track = progression(et12(series(10/2), [0,0,1,2,3,2,3,2,3,6]), major7(c), 1/2,  dollars_and_cents)
# track = progression(et12(series(10/2), [0,0,1,2,3,2,3,2,3,6]), major7(c), 1/2,  morning_bell)
# track = progression(et12(series(5/1), [0,1,2,3,4,3]), phrygian(c), 1/2,  '1 1b 4 4b 5 5b') # wacky science lab
# track = progression(et12(series(5/1), [0,1,2]), major7(c), 1/2,  '1m 3 1m 2 1m 7 1m') # "its coming from inside the house!"
# track = progression(et12(series(4/1), [0,3,4,5]), mixolydian(notes['a']), 1/1,  '1 5m7') # epitaph, ff6
# track = progression(et12(series(4/1), [0,3,4,5]), mixolydian(c), 1/1,  '4 5') # chocobo
# track = progression(et12(mix, [0,1,2]), major7(c), 1/2,  '1m 1s2 1m 1s2 3 1m') # last of us
# track = progression(et12(series(7/2), [0,1,2,4,3,2,1,0]), major7(c), 1/2,  revived_power) 
# track = progression(et12(series(3/2), [2,0,1]), major7(notes['a']), 1/2,  cosmos) 
# track = progression(et12(series(3), [0,1,2]), major7(notes['d']), 1, pachabel)
# track = progression(et12(series(3), [0,1,2]), major7(c), 1, doowop)
# track = progression(et12(mix, [1,0,1,2]), major7(notes['g']), 1, koyaanisqatsi1)
# track = progression(et12(mix, [0,1,2]), major7(notes['d']), 1/2,  '5 1 3m 5') # higher and higher
# track = progression(et12(series(6/2), [0,1,2,3,2,1]), major7(c), 1/2,  '1 5 2m 5') # walking up and down fifths, "love song" vibes
# track = progression(et12(series(6/2), [0,1,2,3,2,1]), major7(c), 1/2,  '1 5 2 5') # walking up and down fifths, "sing song", uninterestingly happy
# track = progression(et12(series(6/2), [0,1,2,3,2,1]), major7(c), 1/2,  '8 5 2m 5') # walking up and down fifths, "sing song", uninterestingly happy
# track = progression(et12(series(3/1), [0,1,2]), major7(c), 1/1,  '1m 1m 1m 1m 1m 1m 1m 1m 6 6 2b 2b 57 1m 5s4 57') # moonlight sonata, notation currently restricts some chords

duration = len(hallelujah)*2
# duration = 8*2
framerate = 41900
stream.write(bytes(bytearray(tuple(track(time/framerate) for time in range(int(duration*framerate)))))) 



# vii IV I V ii