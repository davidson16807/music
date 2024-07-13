import re

'''
`notated` consists of representations of concepts in music (e.g. notes, chords)
without regard to application (e.g. playback, procedural generation, transcription, etc.)
'''

notes = {
    'a'  : 0,
    'a♯' : 1,
    'b♭' : 1,
    'b'  : 2,
    # 'c♭' : 2,
    # 'b♯' : 3,
    'c'  : 3,
    'c♯' : 4,
    'd♭' : 4,
    'd'  : 5,
    'd♯' : 6,
    'e♭' : 6,
    'e'  : 7,
    # 'f♭' : 7,
    # 'e♯' : 8,
    'f'  : 8,
    'f♯' : 9,
    'g♭' : 9,
    'g'  : 10,
    'g♯' : 11,
    'a♭' : 11,
}

# qualities: picking semitones to play together
qualities = {
    'P1'   : [0], 
    'm2'   : [0,1],
    'M2'   : [0,2],
    'm3'   : [0,3],
    'M3'   : [0,4],
    'P4'   : [0,5],
    'P5'   : [0,7],
    # 'm6'   : [0,8],
    # 'M6'   : [0,9],
    # 'm7'   : [0,10],
    # 'M7'   : [0,11],
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
    'Mm7'  : [0,4,7,10], # dominant 7 / major minor 7
    '-7'   : [0,3,6,9 ], # diminished 7
    'mM7'  : [0,3,7,11], # minor major 7
    '+M7'  : [0,4,8,11], # augmented major
    '+7'   : [0,4,8,11], # augmented
    'add2' : [0,2,4,7],  # added 2nd
    'add4' : [0,4,5,7],  # added 4th
    'add9' : [0,4,7,14], # added 9th
}

# mode: : fulltones ⟶ semitones
mode = lambda halves: lambda tonic: lambda degree: tonic+halves[(degree-1)%len(halves)]+12*((degree-1)//len(halves))

# chromatic: the identity mode
chromatic = lambda tonic: lambda degree: tonic+degree-1

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

root = lambda chord_string: int(re.search('^-?[0-9]{1,2}', chord_string).group(0))
quality = lambda chord_string: re.sub('^-?[0-9]{1,2}', '', chord_string)

def chord(mode):
    def parse(chord_string):
        stripped = chord_string.replace('#','').replace('b','')
        return [
            mode(root(stripped)) + interval + ('#' in chord_string)-('b' in chord_string)
            for interval in qualities[quality(stripped)]
        ]
    return parse
