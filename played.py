from math import sin, pi

'''
`played` consists of representations of pure functions that are useful 
for synthesizing music from notes, chords, and progressions.
'''

# "sound" plays "tracks", where a "track" maps time ⟶ waveheight and represents an elemental unit of track composition
def sound(stream, samplerate):
    def play(track, duration): 
        stream.write(bytes(bytearray(tuple(track(time/samplerate) for time in range(int(duration*samplerate)))))) 
    return play

# "timbre": maps hertz ⟶ track
# NOTE: suck it, python, stop imposing dogma on us and give us arrow notation
sine     = lambda volume: lambda hertz: lambda time: int(volume*255*(sin(2*pi*time*hertz)+1)/2)
square   = lambda volume: lambda hertz: lambda time: int(volume*255*((time*hertz)%1.0 > 0.5))
saw      = lambda volume: lambda hertz: lambda time: int(volume*255*((time*hertz)%1.0))
triangle = lambda volume: lambda hertz: lambda time: int(volume*255*abs(((time*hertz)%2.0) - 1))
parabol  = lambda t: (1-t)*(1-t*t) + t*(t-1)**2 # so named because it is the lead-in to "parabola" :)
parabola = lambda volume: lambda hertz: lambda time: int(volume*255*parabol(abs((2*(time*hertz+1)%2.0) - 1)))
''' ^^^The `parabola` wave is an interpolation between 
parabolic approximations of a cosine's crest and trough where the interpolant "t" is a triangle wave.'''

# "combinations": fundamental operators of track composition
mix    =                     lambda *tracks: lambda time: sum(track(time) for track in tracks)
series = lambda track_hertz: lambda *tracks: lambda time: tracks[int((time*track_hertz)%len(tracks))](time)

# temperament: : semitones ⟶ hertz
# "equal" temperament is most commonly used for modern music
equal = lambda a, steps: lambda step, octave=0: a*2**(octave+(step/steps))
# "quarter_comma_meantone" is most commonly used to play ancient music, such as that of the greeks or mesopotamians
pythagorean = lambda base_hertz: lambda step, octave=0: (
        base_hertz*
        (2**octave+step//12)*
        (3**[0,-5,2,-3,4,-1,-6,6,1,-4,3,-2,5][step%12])*
        (2**[0,8,-3,5,-6,2,10,-9,-1,7,-4,4,-7][step%12])
    )
# "quarter_comma_meantone" is most commonly used to play medieval music
quarter_comma_meantone = lambda base_hertz: lambda step, octave=0: (
        base_hertz*
        (2**octave+step//12)*
        ([1.0000,1.0449,1.1180,1.1963,1.2500,1.3375,1.3975,1.4953,1.5625,1.6719,1.7889,1.8692][step%12])
    )
# "werckmeister1" is most commonly used to play bach music
werckmeister1 = lambda base_hertz: lambda step, octave=0: (
        base_hertz*
        (2**octave+step//12)*
        (2**([0,90,192,294,390,498,588,696,792,888,996,1092][step%12]/1200))
    )
# "werckmeister2-4" are other "well temperaments" the same creator as werckmeister1
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

# style: the manner of playing chords, maps intervals ⟶ track
style = lambda temperament, timbre: lambda combination, sequence:  (
    lambda intervals: combination(*[
        timbre(temperament(intervals[i%len(intervals)], octave=i//len(intervals))) 
        for i in sequence
    ])
)

progression = lambda style, notation, chord_hertz, chords: (
    series(chord_hertz)(*[
        style(notation(chord_string)) 
        for chord_string in chords
    ])
)

