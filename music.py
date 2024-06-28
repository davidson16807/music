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
two parabolic approximations of a cosine where the interpolant "t" is a triangle wave.'''

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
    'f♭' : 8,
    'f'  : 9,
    'f♯' : 10,
    'g♭' : 10,
    'g'  : 11,
    'g♯' : 12,
}

# chords: picking semitones to play together


chords = {
    'monad' : [0], # functional programmers love their monads, right?
    'power' : [0,7],
    ''     : [0,4,7], # major
    'm'    : [0,3,7], # minor
    's2'   : [0,2,7], # suspended 2
    's4'   : [0,5,7], # suspended 4
    '+'    : [0,4,8], # augmented
    '-'    : [0,3,6], # diminished
    'M7'   : [0,4,7,11], # major 9th
    'm7'   : [0,3,7,10], # minor
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
        style(key(int(chord[0])), chords[chord[1:]]) 
        for chord in notation.split()
    ])
)

# progressions
pachabel = '8 5 6m 3m 4 1 4 5'
doowop = '1 6m 4 5'
hallelujah = '1 6m 1 6m 4 5 1 5 1 4 5 6m 4 5 37 6m 4 6m 4 1 5 1'
sensitive_female = '6m 4 1 5' # so coined by Boston Globe, example: zombie, snow, real world, poker face, otherside
four_chords = '1 5 6m 4' # so coined by Axis of Awesome, examples: basically everything
anime_theme = '47 5m7 3m7 6m' # 
rickroll = '4m9 7m7 5m7 1m' # 
dire_dire_docks = '1 7 1 7 6m 7' #
# dire_dire_docks2 = '4M 3m 2m 1M' #
# dire_dire_docks = '4M 3m 2m 1- 2m 5M 1M' #

# track1 = progression(style(equal(440/2,12), parabola(0.1))(mix, monad),       key, 1, pachabel)
# track2 = progression(style(equal(440,12), sine(0.1))(mix, [0,1,2]),           key, 1, pachabel)
# track3 = progression(style(equal(440,12), triangle(0.1))(series(3), [0,1,2]), key, 1, pachabel)
# track = series(1/8)( 
#     mix(track1),
#     mix(track1, track2),
#     mix(track1, track2, track3),
# ) # I'll see your ass in hell, Pachabel!

track = progression(style(equal(220,12), triangle(0.1))(series(6/2), [0,2,3,4,5,6]), dorian(notes['c']), 1/2, hallelujah)

duration = 22*2
framerate = 41900
stream.write(bytes(bytearray(tuple(track(time/framerate) for time in range(int(duration*framerate)))))) 
