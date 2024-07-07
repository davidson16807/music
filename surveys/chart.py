import itertools
import os
import sys

sys.path.append(os.path.realpath('..'))
import notated
import stored
import drawn

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

class ProgressionTableHtml:
	def __init__(self, tonnetz_view, quality_sequence):
		self.tonnetz_view = tonnetz_view
		self.quality_sequence = quality_sequence
	def color(self, response):
		return 'black'
	def cell(self, first, second, response):
		return f'''
		<td style="background: {self.color(response)}" onclick="details('1{first} 1{second}')">&nbsp;</td>
		'''
	def detail(self, first, second, harmonic, melodic):
		return f'''
		<div id="1{first} 1{second}">
			<p><span style="color:black">{first}</span> → <span style="color:red">{second}</span>:</p>
			<p onclick="test('1{first} 1{second}', 0)">▶ harmonic: {harmonic}</p> 
			<p onclick="test('1{first} 1{second}', 1)">▶ melodic: {melodic}</p> 
			<p>tonnetz diagram:</p> 
			{self.tonnetz_view.tonnetz([notated.qualities[first], notated.qualities[second]], 300, 150, 2)}
		</div>
		'''
	def table(self, responses):
		cells = '\n'.join([
			'\n'.join([
				'<tr>', 
				*[self.cell(first, second, responses[(first, second, 'True')])
					if (first, second) in responses else ''
					for second in quality_sequence],
				'</tr>'
			])
			for first in quality_sequence
		])
		details = '\n'.join([
			self.detail(first, second, responses[first, second, 'False'], responses[first, second, 'True'])
			for first, second in itertools.product(quality_sequence, quality_sequence)
			if (first, second, 'False') in responses and (first, second, 'True') in responses
		])
		html = '''
		<!DOCTYPE html>
		<html>
		<head>
			<meta name="viewport" content="width=device-width, initial-scale=1">
			<script src="../played.js"></script>
			<script src="../notated.js"></script>
			<script>
			const et12 = style(equal(432,12), sine(0.1));
			const key = chord(major7(0));
			const range = length => [...Array(length)].map((_,i) => i)
			const AudioContext = window.AudioContext || window.webkitAudioContext;
			function test(progression_string, is_arpeggio){
				const play = sound(new AudioContext(), 41900);
				const note_count = Math.max(...progression_string.split(' ').map(chord_string => qualities[quality(chord_string)].length));
				const combination = is_arpeggio? series(note_count) : mix;
				play(progression(et12(combination, range(note_count)), key, 1, progression_string), 2);
			}
			</script>
		</head>
		<body style="display:flex">
			<!--<div><table>{{cells}}</table></div>-->
			<div>{{details}}</div>
		</body>
		</html>
		'''
		unused = '''
			<script>
			details = undefined;
			function details(id) {
			  if(details){details.style.display = 'none';}
			  details = document.getElementById(id);
			  details.style.display = 'box';
			}
			</script>
		'''
		return (html
			.replace('{{cells}}', cells)
			.replace('{{details}}', details)
		)

qualities = 'qualities.tsv'
table = stored.DelimitedTable('\t')
with open(qualities, 'r') as file:
    data = {
    	(cells[1], cells[2], cells[3]): cells[4]
    	for cells in table.parse(file.read())
    	if len(cells) == 5
    }

# view = (drawn.TonnetzSvg(drawn.GraphSvg(5), Metric2(), 5, 3))
# print(view.table([[0,4,7,11], [0,4,7]], 500, 500, 5))
quality_sequence = 'M m s2 s4 + - M7 m7 Mm7 mM7 M9 m9 M6 m6 M11 m11 ∅7 +M7 -7 +7 add2 add4 add9 M79 m79 M911 m911 m3 M3 P4 P5 P1 '.split()
html = ProgressionTableHtml(drawn.TonnetzSvg(drawn.GraphSvg(5), Metric2(), 5, 3), quality_sequence)
print(html.table(data))

