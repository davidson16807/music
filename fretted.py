
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
	def __init__(self, open_string_semitones):
		self.open_string_semitones = open_string_semitones
	def pluck(string, fret):
		return self.open_string_semitones[string]+fret

class Tab:
	def __init__(self, tuning, bar_length, string_delimiter='\n', strum_delimiter='', unplayed='-', bar='|'):
		self.tuning = tuning
		self.bar_length = bar_length
		self.bar = bar
		self.unplayed = unplayed
		self.string_delimiter = string_delimiter
		self.strum_delimiter = strum_delimiter
	def parse(tab_code):
		return [
			[(self.tuning.pluck(int(pluck)) if pluck != self.unplayed and i%bar_length!=0  else None) 
				for i, pluck in enumerate(string.split(self.strum_delimiter))] 
			for string in tab_code.split(self.string_delimiter)
		]
	def format(semitone_lists):
		return self.string_delimiter.join([
			self.strum_delimiter.join([
				(self.unplayed if semitone is None else 
					self.bar if i%bar_length==0 else 
						str(semitone))
				for i,semitone in enumerate(semitones)
			])
			for semitones in semitone_lists
		])

# # map to and from a list of semitone interval lists:
# transposition = stored.Involution(lambda lists: list(map(list, zip(*lists))))
# stored.Composition(
# 	Tab(...),
# 	transposition,
# )
