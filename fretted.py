import re

import stored
import notated

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
		self.string_count = len(open_string_semitones)
		self.capo = capo
	def semitone(self, string, fret):
		return self.open_string_semitones[self.string_count-1-string]+max(fret, self.capo)
	def fret(self, string, semitone):
		if semitone is None: return None
		return semitone
		fret = semitone - self.open_string_semitones[self.string_count-1-string]
		return fret# None if fret <= self.capo else fret

class Tab:
	def __init__(self, tuning, bar_length, characters_per_note=1, string_delimiter='\n', staff_delimiter='\n\n', unplayed='-', bar='|', string_count = 6):
		self.tuning = tuning
		self.bar_length = bar_length
		self.bar = bar
		self.unplayed = unplayed
		self.string_delimiter = string_delimiter
		self.staff_delimiter = staff_delimiter
		self.characters_per_note = characters_per_note
		self.string_count = string_count
	def parse(self, tab):
		staff_strings = [
			[line 
				for line in staff.split(self.string_delimiter)
				if len(line.strip()) > 0
			] for staff in tab.split(self.staff_delimiter)
		]
		string_staffs = list(map(list, zip(*staff_strings))) # transpose
		strings = [
			''.join(staffs)
			for staffs in string_staffs
		] # concatenate staffs
		return [
			[(self.tuning.semitone(j, int(string[i:i+self.characters_per_note].strip(self.unplayed))) if re.match('[0-9]+', string[i]) else None)
				for i in range(0, len(string), self.characters_per_note)
				if string[i] != self.bar]
			for j, string in enumerate(strings)
		]
	def format(self, string_semitones):
		fret_lists = [
			[self.tuning.fret(j, semitone)
				for semitone in semitones]
			for j, semitones in enumerate(string_semitones)
		]
		return self.string_delimiter.join([
			''.join([
				(self.unplayed if fret is None else 
					# self.bar if i%self.bar_length==0 else 
						str(fret))
				for fret in frets
			])
			for frets in fret_lists
		])

pitch = stored.ScientificPitch(notated.notes)
standard_guitar_tuning = Tuning([pitch.parse(note) for note in 'e2 a2 d3 g3 b3 e4'.split()])
standard_ukulele_tuning = Tuning([pitch.parse(note) for note in 'g4 c4 e4 a4'.split()])

standard_cello_tuning = Tuning([pitch.parse(note) for note in 'c2 g2 d3 a3'.split()])
standard_viola_tuning = Tuning([pitch.parse(note) for note in 'c3 g3 d4 a4'.split()])
standard_mandolin_tuning = Tuning([pitch.parse(note) for note in 'g3 d4 a4 e5'.split()])
standard_violin_tuning = Tuning([pitch.parse(note) for note in 'g3 d4 a4 e5'.split()])
