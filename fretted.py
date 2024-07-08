import re

class PartSvg:
	def __init__(self, string_count, string_size, fret_size):
		self.fret_size = fret_size
		self.string_size = string_size
		self.string_count = string_count
	def fret(self, id):
		fret_y = id*self.fret_size
		return f'<path d="M {self.string_size/2} {fret_y} L {(self.string_count-0.5)*self.string_size} {fret_y}" style="fill:none; stroke:dimgrey; stroke-width:2;"/>'
	def string(self, id, fret_count):
		fret_x = (id+0.5)*self.string_size
		max_y = fret_count*self.fret_size	
		return f'<path d="M  {fret_x} 0 L {fret_x} {max_y}" style="fill:none; stroke:dimgrey; stroke-width:2;"/>'
	def press(self, string_id, fret_id):
		return f'<circle cx="{(string_id+0.5) * self.string_size}" cy="{(fret_id-0.5)*self.fret_size}" r="10"/>'
	def marker(self, fret_id):
		marker_size = 5
		return f'<rect x="{(self.string_count/2) * self.string_size - marker_size/2}" y="{(fret_id-0.5)*self.fret_size - marker_size/2}" width="{marker_size}" height="{marker_size}"/>'

class FretSvg:
	def __init__(self, parts, markers, width, height):
		self.parts = parts
		self.markers = markers
	def draw(self, press_ids):
		max_fret_id = max([press_id for press_id in press_ids if press_id] + [4])
		frets = ''.join(self.parts.fret(i) for i in range(max_fret_id))
		strings = ''.join(self.parts.string(i, max_fret_id) for i in range(self.parts.string_count))
		presses = ''.join(self.parts.press(i, press_ids[i]) for i in range(len(press_ids)) if press_ids[i] )
		markers = ''.join(self.parts.marker(i) for i in self.markers if i < max_fret_id)
		return f'''
			<svg width="{self.width}" height="{self.height}">
				<g transform="translate(0 0)">
					{frets + strings + presses + markers}
				</g>
			</svg>'''.replace('\n\t\t\t', '\n')

def chord(strum_code):
	if ',' in strum_code:
		return [(None if fret_id.lower() == 'x' else int(fret_id)) for fret_id in strum_code.split(',')]
	else:
		return [(None if fret_id.lower() == 'x' else int(fret_id)) for fret_id in strum_code]

class Tuning:
	def __init__(self, open_string_semitones, capo=0):
		self.open_string_semitones = open_string_semitones
		self.capo = capo
	def pluck(self, string, fret):
		return self.open_string_semitones[string]+min(fret, self.capo)

class Tab:
	def __init__(self, tuning, bar_length, characters_per_note=1, string_delimiter='\n', pluck_delimiter='', unplayed='-', bar='|'):
		self.tuning = tuning
		self.bar_length = bar_length
		self.bar = bar
		self.unplayed = unplayed
		self.string_delimiter = string_delimiter
		self.pluck_delimiter = pluck_delimiter
		self.characters_per_note = characters_per_note
	def parse(self, tab_code):
		strings = [line
			for line in tab_code.split(self.string_delimiter) 
			if len(line.strip()) > 0
		]
		print(strings)
		return [
			[(self.tuning.pluck(j, int(string[i])) if re.match('[0-9]+', string[i:i+self.characters_per_note]) else None)
				for i in range(0,len(string), self.characters_per_note)
				if string[i] != self.bar]
			for j, string in enumerate(strings)
		]
	def format(self, semitone_lists):
		return self.string_delimiter.join([
			self.pluck_delimiter.join([
				(self.unplayed if semitone is None else 
					self.bar if i%bar_length==0 else 
						str(semitone))
				for i,semitone in enumerate(semitones)
			])
			for semitones in semitone_lists
		])

voices1 = '''
|----------------|----------------|
|2-2--2--2--0----|3-3--0--2--2----|
|0-0--0--2--2----|2-2--2--0--0----|
|2-2--2--1--1----|0-0--0--2--2----|
|0-0000000000-00-|0-0000000000-00-|
|---------------0|---------------0|
'''

# # map to and from a list of semitone interval lists:
from pyaudio import PyAudio
import stored
import notated
import played
transposition = stored.Involution(lambda lists: list(map(list, zip(*lists))))
tab = stored.Composition(transposition, Tab(Tuning([notated.notes[note] for note in 'eadgbe']), 17, characters_per_note=2))
staff = lambda tab_semitones: [
	{semitone 
		for semitone in semitones 
		if semitone is not None}
	for semitones in tab_semitones
]

pyaudio = PyAudio()
play = played.sound(
    pyaudio.open(format=pyaudio.get_format_from_width(1), # open stream
        channels=1,
        rate=41900,
        output=True
    ), 41900
)

# print(strip(tab.parse(voices1)))
et12 = played.equal(432,12)
play(played.staff(et12, played.sine(0.1), 4) (staff(tab.parse(voices1))), 6)
