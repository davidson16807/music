import itertools
from typing import List

def svg(elements, width, height, scale):
	content = '\n'.join(elements)
	return f'''<svg width="{width}" height="{height}"> \n <g transform="translate({width/2} {height/2}) scale({scale})"> {content} \n</g> \n</svg>'''

class GraphSvg:
	def __init__(self, scale):
		self.scale = scale
	def node(self, point1, color='black', radius=1):
		return f'<circle cx="{self.scale*point1[0]}" cy="{self.scale*point1[1]}" r="{self.scale*radius}" style="fill:{color}; stroke:none;"/>'
	def edge(self, point1, point2, color='black', dasharray='0'):
		return f'<path d="M {self.scale*point1[0]} {self.scale*point1[1]} L {self.scale*point2[0]} {self.scale*point2[1]}" style="fill:none; stroke:{color}; stroke-width:2; stroke-dasharray:{dasharray}"/>'

class ChordTonnetzElements:
	def __init__(self, graph, metric, column_gap, row_gap):
		self.graph = graph
		self.metric = metric
		self.row_gap = row_gap
		self.column_gap = column_gap
		self.max_length = max(
			metric.length(self.position(0,-1)),
			metric.length(self.position(0, 1)),
			metric.length(self.position(1, 0)),
		)
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
	def draw(self, semitones:List[int], color='black', dasharray='0', radius=0):
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
			*[self.graph.node(position(*v), color=color, radius=radius) for v in nodes],
			*[self.graph.edge(position(*u), position(*v), color=color, dasharray=dasharray) for u,v in edges]
		]

class ProgressionTonnetzElements:
	def __init__(self, chord_tonnetz_elements, radii, colors, dasharrays):
		self.chord = chord_tonnetz_elements
		self.radii = radii
		self.colors = colors
		self.dasharrays = dasharrays
	def draw(self, chords:List[List[int]]):
		return [
			element
			for i, semitones in enumerate(chords)
			for element in self.chord.draw(semitones, color=self.colors[i], dasharray=self.dasharrays[i], radius=self.radii[i])
		]

class Storage:
    def __init__(self, drawing, storage):
        self.drawing = drawing
        self.stoage = stoage
    def draw(self, data):
        return self.drawing.draw(self.storage.parse(data))

class Notation:
    def __init__(self, drawing, notation):
        self.drawing = drawing
        self.notation = notation
    def draw(self, data):
        return self.drawing.draw(self.notation(data))
