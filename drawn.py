import itertools

class GraphSvg:
	def __init__(self, scale):
		self.scale = scale
	def node(self, point1, color='black', radius=1):
		return f'<circle cx="{self.scale*point1[0]}" cy="{self.scale*point1[1]}" r="{self.scale*radius}" style="fill:{color}; stroke:none;"/>'
	def edge(self, point1, point2, color='black', dasharray='0'):
		return f'<path d="M {self.scale*point1[0]} {self.scale*point1[1]} L {self.scale*point2[0]} {self.scale*point2[1]}" style="fill:none; stroke:{color}; stroke-width:2; stroke-dasharray:{dasharray}"/>'
	def graph(self, elements, width, height, scale):
		content = '\n'.join(elements)
		return f'''<svg width="{width}" height="{height}"> \n <g transform="translate({width/2} {height/2}) scale({scale})"> {content} \n</g> \n</svg>'''

class TonnetzSvg:
	def __init__(self, view, metric, column_gap, row_gap):
		self.view = view
		self.metric = metric
		self.row_gap = row_gap
		self.column_gap = column_gap
		self.max_length = max(
			metric.length(self.position(0,-1)),
			metric.length(self.position(0, 1)),
			metric.length(self.position(1, 0)),
		)
		self.radii = [1,0.8]
		self.colors = 'black red green blue yellow magenta cyan'.split()
		self.dasharray = ['0', '3 2']
		self.lookup = {
			0: (0, 0),
			1: (-2,-1),
			2: (2, 0),
			3: (0,-1),
			4: (0, 1),
			5: (-1,0),
			6: (0,-2),
			7: (1, 0),
			8: (-1,-1), # or (0, 2)
			9: (-1,1),
			10:(1,-1), # or (-2,0)
			11:(1, 1),
		}
	def position(self, x,y):
		return (
			7*x + (4 if y>0 else -3)*y, 
			y*self.row_gap
		)
	def chord(self, semitones, color='black', dasharray='0', radius=0):
		normalized = [semitone%12 for semitone in semitones]
		root = min(normalized)
		nodes = {self.lookup[semitone-root] for semitone in normalized}
		position = self.position
		edges = {
			tuple(sorted(pair))
			for pair in itertools.product(nodes, repeat=2)
			if self.metric.distance(position(*pair[0]), position(*pair[1])) <= self.max_length
		}
		return [
			*[self.view.node(position(*v), color=color, radius=radius) for v in nodes],
			*[self.view.edge(position(*u), position(*v), color=color, dasharray=dasharray) for u,v in edges]
		]
	def tonnetz(self, chords, width, height, scale):
		return self.view.graph([
			element
			for i, semitones in enumerate(chords)
			for element in self.chord(semitones, color=self.colors[i], dasharray=self.dasharray[i], radius=self.radii[i])
		], width, height, scale)

class FretPartSvg:
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
	def __init__(self, markers, parts):
		self.parts = parts
		self.markers = markers
	def press_ids_to_diagram_svg(self, press_ids):
		max_fret_id = max([press_id for press_id in press_ids if press_id] + [4])
		frets = ''.join(self.parts.fret(i) for i in range(max_fret_id))
		strings = ''.join(self.parts.string(i, max_fret_id) for i in range(self.parts.string_count))
		presses = ''.join(self.parts.press(i, press_ids[i]) for i in range(len(press_ids)) if press_ids[i] )
		markers = ''.join(self.parts.marker(i) for i in self.markers if i < max_fret_id)
		return ('''
			<svg width="500" height="500">
				<g transform="translate(0 0)">
					{{content}}
				</g>
			</svg>
			'''
			.replace('\n\t\t\t', '\n')
			.replace('content', frets + strings + presses + markers)
		)

def chord_string_to_press_ids(chord_string):
	if ',' in chord_string:
		return [(None if fret_id.lower() == 'x' else int(fret_id)) for fret_id in chord_string.split(',')]
	else:
		return [(None if fret_id.lower() == 'x' else int(fret_id)) for fret_id in chord_string]
