import itertools

import notated
import stored

quality_sequence = 'M m s2 s4 + - M7 m7 7 mM7 M9 m9 M6 m6 M11 m11 ∅7 +M7 -7 +7 add2 add4 add9 M79 m79 M911 m911 m3 M3 P4 P5 P1 '.split()

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

class Metric2:
	def __init__(self):
		pass
	def distance(self, u, v):
		xu,yu = u
		xv,yv = v
		return ((xu-xv)**2+(yu-yv)**2)**(1/2)
	def length(self, v):
		return self.distance((0,0), v)
	def normalize(self, v):
		length = self.length(v)
		return (v[0]/length, v[1]/length)

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


class ProgressionTableHtml:
	def __init__(self, tonnetz_view):
		self.tonnetz_view = tonnetz_view
	def color(self, response):
		return 'black'
	def cell(self, i, response):
		return f'''<td style="background: {self.color(response)}" onclick="click('{i}')">&nbsp;</td>'''
	def detail(self, i, first, second, response):
		tonnetz = self.tonnetz_view.tonnetz([notated.qualities[first], notated.qualities[second]], 400, 150, 2)
		return f'''<div id="{i}"><p><span style="color:black">{first}</span> → <span style="color:red">{second}</span>:</p><p>{response}:</p> {tonnetz}</div>'''
	def table(self, responses):
		cells = '\n'.join([
			'\n'.join([
				'<tr>', 
				*[self.cell(i*len(quality_sequence)+j, responses[(first, second)])
					if (first, second) in responses else ''
					for j, second in enumerate(quality_sequence)],
				'</tr>'
			])
			for i, first in enumerate(quality_sequence)
		])
		details = '\n'.join([
			self.detail(i, *progression, responses[progression])
			for i, progression in enumerate(itertools.product(quality_sequence, quality_sequence))
			if progression in responses
		])
		html = '''
		<!DOCTYPE html>
		<html>
		<head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
		<body style="display:flex">
			<!--<div><table>{{cells}}</table></div>-->
			<div>{{details}}</div>
			<script>
			details = undefined;
			function click(id) {
			  if(details){details.style.display = 'none';}
			  details = document.getElementById(id);
			  details.style.display = 'box';
			}
			</script>
		</body>
		</html>
		'''
		return (html
			.replace('{{cells}}', cells)
			.replace('{{details}}', details)
		)

qualities = 'qualities.tsv'
table = stored.DelimitedTable('\t')
with open(qualities, 'r') as file:
    data = {
    	(cells[1], cells[2]): cells[-1]
    	for cells in table.parse(file.read())
    	if len(cells) == 5
    }

# view = (TonnetzSvg(GraphSvg(5), Metric2(), 5, 3))
# print(view.table([[0,4,7,11], [0,4,7]], 500, 500, 5))
html = ProgressionTableHtml(TonnetzSvg(GraphSvg(5), Metric2(), 5, 3))
print(html.table(data))

