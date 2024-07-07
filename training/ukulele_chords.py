import drawn

def whitespace(text):
	return len(text.strip()) < 1

with open('ukulele-chords.txt') as file:
	chord_pairs = [(line.split(':')[0].strip(), line.split(':')[1].strip()) 
		for line in file.readlines() 
		if not whitespace(line)]

view = drawn.FretSvg([5,7,10], drawn.FretPartSvg(4, 20, 30))
for name, string in chord_pairs:
	print(f'{name}\t{view.press_ids_to_diagram_svg(chord_string_to_press_ids(string))}')
