'use strict';

/*
`played` consists of representations of pure functions that are useful 
for synthesizing music from notes, chords, and progressions.
*/

// "sound" plays "tracks", where a "track" maps time ⟶ waveheight and represents an elemental unit of track composition
const sound = (context, sample_rate) => (track, duration) => {
    context.sample_Rate = sample_rate
    const sample_count = duration*sample_rate;
    const array = new Float32Array(sample_count);
    for (let time = 0; time < sample_count; time++) { array[time] = track(time/sample_rate); }
    const buffer = context.createBuffer(1, sample_count, sample_rate);
    buffer.copyToChannel(array, 0);
    const source = context.createBufferSource();
    source.buffer = buffer;
    source.connect(context.destination);
    source.start(0);
}

// "timbre": maps hertz ⟶ track
// NOTE: suck it, python, stop imposing dogma on us and give us arrow notation
const sine     = volume => hertz => time => volume*Math.sin(2*Math.PI*time*hertz);
const square   = volume => hertz => time => ((time*hertz)%1.0 > 0.5)
const saw      = volume => hertz => time => ((time*hertz)%1.0)
const triangle = volume => hertz => time => abs(((time*hertz)%2.0) - 1)
const parabol  = t => (1-t)*(1-t*t) + t*(t-1)**2 // so named because it is the lead-in to "parabola" :)
const parabola = volume => hertz => time => parabol(abs((2*(time*hertz+1)%2.0) - 1))
/* ^^^The `parabola` wave is an interpolation between 
parabolic approximations of a cosine's crest and trough where the interpolant "t" is a triangle wave.*/

// "combinations": fundamental operators of track composition
const mix    =                (...tracks) => time => {let sum = 0; for (let track of tracks) {sum+= track(time);} return sum;}
const series = track_hertz => (...tracks) => time => tracks[((time*track_hertz)%tracks.length)|0](time)

// temperament: : semitones ⟶ hertz
// "equal" temperament is most commonly used for modern music
const equal = (a, steps) => (step, octave=0) => a*2**(octave+(step/steps))
// "quarter_comma_meantone" is most commonly used to play ancient music, such as that of the greeks or mesopotamians
const pythagorean = base_hertz => (step, octave=0) => (
        base_hertz*
        (2**octave+(step/12)|0)*
        (3**[0,-5,2,-3,4,-1,-6,6,1,-4,3,-2,5][step%12])*
        (2**[0,8,-3,5,-6,2,10,-9,-1,7,-4,4,-7][step%12])
    );
// "quarter_comma_meantone" is most commonly used to play medieval music
const quarter_comma_meantone = base_hertz => (step, octave=0) => (
        base_hertz*
        (2**octave+(step/12)|0)*
        ([1.0000,1.0449,1.1180,1.1963,1.2500,1.3375,1.3975,1.4953,1.5625,1.6719,1.7889,1.8692][step%12])
    );
// "werckmeister1" is most commonly used to play bach music
const werckmeister1 = base_hertz => (step, octave=0) => (
        base_hertz*
        (2**octave+(step/12)|0)*
        (2**([0,90,192,294,390,498,588,696,792,888,996,1092][step%12]/1200))
    );
// "werckmeister2-4" are other "well temperaments" the same creator as werckmeister1
const werckmeister2 = base_hertz => (step, octave=0) => (
        base_hertz*
        (2**octave+(step/12)|0)*
        (2**([0,85.8,195.3,295.0,393.5,498.0,590.2,693.3,787.7,891.6,1003.8,1088.3][step%12]/1200))
    );
const werckmeister3 = base_hertz => (step, octave=0) => (
        base_hertz*
        (2**octave+(step/12)|0)*
        (2**([0,96,204,300,396,504,600,702,792,900,1002,1098][step%12]/1200))
    );
const werckmeister4 = base_hertz => (step, octave=0) => (
        base_hertz*
        (2**octave+(step/12)|0)*
        (2**([0,91,196,298,395,498,595,698,793,893,1000,1097][step%12]/1200))
    );

// "staff": a track that plays according to a representation of "staff notation", which consists of a series of intermixed semitone sets
const staff = (temperament, timbre, tempo_hertz) => semitone_sets =>
    series(tempo_hertz)(...semitone_sets.map(
        semitones => mix(...semitones.map(
            i => timbre(temperament(i))
        ))
    ));

// "style": the manner of playing chords, maps intervals ⟶ track
const style = (temperament, timbre) => (combination, sequence) => intervals =>
    combination(...sequence.map(i => 
        timbre(temperament(intervals[i%intervals.length], (i/intervals.length)|0)) 
    ));

// "progression": a series of chords, plays audio that is represented by string of space separated chords (e.g. "1m", "5M7")
const progression = (style, notation, chord_hertz, chords) => 
    series(chord_hertz)(...chords.map(chord_string => style(notation(chord_string))));

// AudioContext = window.AudioContext || window.webkitAudioContext;
// sound(new AudioContext(), 41900) (sine(0.1)(432), 2); 
// sound(new AudioContext(), 41900) (mix(sine(0.1)(432), sine(0.1)(1.5*432)), 2); 
// sound(new AudioContext(), 41900) (series(2)(sine(0.1)(432), sine(0.1)(1.5*432)), 2); 

