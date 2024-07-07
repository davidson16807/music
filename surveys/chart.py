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
	def __init__(self, tonnetz_svg, quality_sequence, combination_sequence):
		self.tonnetz = tonnetz_svg
		self.quality_sequence = quality_sequence
		self.combination_sequence = combination_sequence
	def color(self, response):
		return 'black'
	def cell(self, first, second, response):
		return f'''
		<td style="background: {self.color(response)}" onclick="details('{first} {second}')">&nbsp;</td>
		'''
	def detail(self, first, second, responses):
		samples = '\n'.join([
			f'''<p onclick="test('{first}', '{second}', '{combination}')">▶ {combination}: {response}</p>''' 
			for combination, response in responses
		])
		return f'''
		<div id="{first} {second}">
			<p><span style="color:black">{first}</span> → <span style="color:red">{second}</span>:</p>
			{samples}
			<p>tonnetz diagram:</p> 
			{drawn.svg(self.tonnetz.draw([notated.qualities[notated.quality(first)], notated.qualities[notated.quality(second)]]), 300, 150, 2)}
		</div>
		'''.replace('\n\t\t','')
	def table(self, responses):
		cells = '\n'.join([
			'\n'.join([
				'<tr>', 
				*[self.cell(first, second, responses[(first, second, 'harmonic')])
					if (first, second) in responses else ''
					for second in self.quality_sequence],
				'</tr>'
			])
			for first in self.quality_sequence
		])
		details = '\n'.join([
			self.detail(first, second, 
				[(combination, responses[first, second, combination])
				 for combination in self.combination_sequence 
				 if (first, second, combination) in responses])
			for first, second in itertools.product([f'1{quality}' for quality in self.quality_sequence], repeat=2)
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
			const AudioContext = window.AudioContext || window.webkitAudioContext;
			const sequences = {
				'harmonic':   count => [...Array(count)].map((_,i) => i),
				'ascending':  count => [...Array(count)].map((_,i) => i),
				'descending': count => [...Array(count)].map((_,i) => count-i-1),
			};
			function test(first, second, combination){
				const play = sound(new AudioContext(), 41900);
				const note_count = Math.max(...[first, second].map(chord_string => qualities[quality(chord_string)].length));
				play(
					progression(
						et12(combination=='harmonic'? mix : series(note_count), sequences[combination](note_count)), 
						key, 1, [first, second]), 
					2);
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

chords_filename = 'chords.tsv'
storage = stored.DelimitedLookup('\t')
with open(chords_filename, 'r') as file:
    data = storage.parse(file.read())

# view = (drawn.TonnetzSvg(drawn.GraphSvg(5), Metric2(), 5, 3))
# print(view.table([[0,4,7,11], [0,4,7]], 500, 500, 5))
html = ProgressionTableHtml(
	drawn.ProgressionTonnetzElements(
		drawn.ChordTonnetzElements(
			drawn.GraphSvg(5), 
			Metric2(), 5, 3),
		[1,0.8], 
		'black red green blue yellow magenta cyan'.split(), 
		['0', '3 2']), 
	'M m s2 s4 + - M7 m7 Mm7 mM7 M9 m9 M6 m6 M11 m11 ∅7 +M7 -7 +7 add2 add4 add9 M79 m79 M911 m911 m3 M3 P4 P5 P1 '.split(),
	'harmonic ascending descending'.split())
# print(data)
print(html.table(data))

