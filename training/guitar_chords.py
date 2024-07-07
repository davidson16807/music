import drawn

def whitespace(text):
	return len(text.strip()) < 1

with open('guitar-chords.txt') as file:
	chord_pairs = [(line.split(':')[0].strip(), line.split(':')[1].strip()) 
		for line in file.readlines() 
		if not whitespace(line)]

# print(chord_template.replace('{{content}}', 
# 	drawn.FretSvg(drawn.FretPartSvg(6, 20, 30)).press_ids_to_diagram_svg(chord_string_to_press_ids('x83210'))))

view = drawn.FretSvg([5,7,9], drawn.FretPartSvg(6, 20, 30))
for name, string in chord_pairs:
	print(f'{name}\t{view.press_ids_to_diagram_svg(chord_string_to_press_ids(string))}')
