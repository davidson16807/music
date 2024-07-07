import fretted

def whitespace(text):
	return len(text.strip()) < 1

with open('ukulele-chords.txt') as file:
	chord_pairs = [(line.split(':')[0].strip(), line.split(':')[1].strip()) 
		for line in file.readlines() 
		if not whitespace(line)]

board = fretted.BoardSvg(
	fretted.PartSvg(4, 20, 30),
	[5,7,10], 500, 500)
for name, string in chord_pairs:
	print(f'{name}\t{board.draw(chord(string))}')
