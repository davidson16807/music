import itertools

# chords: picking semitones to play together
chords = {
    'P1'   : [0], 
    'm3'   : [0,3],
    'M3'   : [0,4],
    'P4'   : [0,5],
    'P5'   : [0,7],
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
    '7'    : [0,4,7,10], # dominant 7 / major minor 7
    '-7'   : [0,3,6,9 ], # diminished 7
    'mM7'  : [0,3,7,11], # minor major 7
    '+M7'  : [0,4,8,11], # augmented major
    '+7'   : [0,4,8,11], # augmented
    'add2' : [0,2,4,7],  # added 2nd
    'add4' : [0,4,5,7],  # added 4th
    'add9' : [0,4,7,14], # added 9th
}

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
			8: (0, 2), # or (-1,-1)
			9: (-1,1),
			10:(-2,0), # or (1,-1)
			11:(1, 1),
		}
	def position(self, x,y):
		return (
			7*x + (4 if y>0 else -3)*y, 
			y*self.row_gap
		)
	def chord(self, semitones, color='black', dasharray='0'):
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
			*[self.view.node(position(*v), color=color) for v in nodes],
			*[self.view.edge(position(*u), position(*v), color=color, dasharray=dasharray) for u,v in edges]
		]
	def tonnetz(self, chords, width, height, scale):
		return self.view.graph([
			element
			for i, semitones in enumerate(chords)
			for element in self.chord(semitones, color=self.colors[i], dasharray=self.dasharray[i])
		], width, height, scale)


class ProgressionTableHtml:
	def __init__(self, tonnetz_view):
		self.tonnetz_view = tonnetz_view
	def color(self, response):
		return 'black'
	def cell(self, i, response):
		return f'''<td style="background: {self.color(response)}" onclick="click('{i}')">&nbsp;</td>'''
	def detail(self, i, first, second, response):
		tonnetz = self.tonnetz_view.tonnetz([chords[first], chords[second]], 400, 150, 2)
		return f'''<div id="{i}"><p>{first} {second}:</p><p>{response}:</p> {tonnetz}</div>'''
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

class Serialization:
    def __init__(self, delimiter):
        self.delimiter = delimiter
    def format(self, data):
        return '\n'.join([
            self.delimiter.join([str(cell) for cell in row]) 
            for row in data
        ])
    def parse(self, text):
        return [line.split(self.delimiter) for line in text.split('\n')]

qualities = 'qualities.tsv'
serialization = Serialization('\t')
with open(qualities, 'r') as file:
    data = {
    	(cells[1], cells[2]): cells[-1]
    	for cells in serialization.parse(file.read())
    	if len(cells) == 5
    }

# view = (TonnetzSvg(GraphSvg(5), Metric2(), 5, 3))
# print(view.table([[0,4,7,11], [0,4,7]], 500, 500, 5))
view = ProgressionTableHtml(TonnetzSvg(GraphSvg(5), Metric2(), 5, 3))
print(view.table(data))

