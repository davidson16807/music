
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

def chord(press_code):
	if ',' in press_code:
		return [(None if fret_id.lower() == 'x' else int(fret_id)) for fret_id in press_code.split(',')]
	else:
		return [(None if fret_id.lower() == 'x' else int(fret_id)) for fret_id in press_code]

def Tuning:
	def __init__(self, open_string_semitones):
		self.open_string_semitones = open_string_semitones

def tab(tab_string):
	pass