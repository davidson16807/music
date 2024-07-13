import os
import sys

# # map to and from a list of semitone interval lists:
from pyaudio import PyAudio

sys.path.append(os.path.realpath('..'))
import stored
import notated
import played
import fretted

staff = lambda tab_semitones: [
	{semitone 
		for semitone in semitones 
		if semitone is not None}
	for semitones in tab_semitones
]

chordtext = stored.Tokenization(sorted, '-', stored.ScientificPitch(notated.notes))
stafftext = stored.Tokenization(list, ' ', chordtext)
sequencer = stored.OnlineSequencer(1, 1)
standard_tuning = fretted.Tuning(chordtext.parse('e2-a2-d3-g3-b3-e4'))
et12 = played.equal(432,12)
transposition = stored.Involution(lambda lists: list(map(list, zip(*lists))))

clocks = stored.Composition(transposition, fretted.Tab(standard_tuning, 17, characters_per_note=3)).parse('''
|--11-------11-------11----|--9--------9--------9-----|--9--------9--------9-----|--8--------8--------8-----
|-----11-------11-------11-|-----11-------11-------11-|-----11-------11-------11-|-----9--------9--------9--
|--------12-------12-------|--------10-------10-------|--------10-------10-------|--------10-------10-------
|--------------------------|--------------------------|--------------------------|--------------------------
|--------------------------|--------------------------|--------------------------|--------------------------
|--------------------------|--------------------------|--------------------------|--------------------------
''')

histories_of_x_and_y = stored.Composition(transposition, fretted.Tab(standard_tuning, 17, characters_per_note=2)).parse('''
|---------|-0---------------------------0---|-----------------0-----------0---|---------------------------------
|-------3-|-----3-----------3---------------|-1-------------------1-----------|---------------------------------
|-----1---|---------1-----------1-----------|-----2---------------------------|-2-------------------2-----------
|---3-----|-------------3-----------3-------|---------2---------------2-------|-----1-----------1-------1-------
|-2-------|-----------------2---------------|-0-----------0-------------------|-------------0---------------0---
|---------|---------------------------------|---------------------------------|-2-------2-----------------------

|---------------------------------|---------------------------------|---------------------------------
|---------------------------------|---------------------------------|---------------------------------
|-0---------------0---------------|-0---------------0---------------|-0---------------0---------------
|-----2-------2-------2-------2---|-----2-------2-------2-------2---|-----2-------2-------2-------2---
|---------2---------------2-------|---------2---------------2-------|---------2---------------2-------
|-0-------------------------------|---------------------------------|---------------------------------

|---------------------------------|---------------------------------|---------------------------------
|---------------------------------|-1---------------1---------------|-0---------------0---------------
|-0---------------0---------------|-----0-------0-------0-------0---|-----0-------0-------0-------0---
|-----2-------2-------2-------2---|---------2---------------2-------|---------2---------------2-------
|---------2---------------2-------|---------------------------------|---------------------------------
|---------------------------------|---------------------------------|---------------------------------

|---------------------------------|---------------------------|---------------------------------
|-1---------------1---------------|-------------0-------------|-0-------------------------------
|-----0-------0-------0-------0---|-----------------0---------|-----0-------0-------0-------0---
|---------2---------------2-------|-----2---------------------|---------2---------------2-------
|---------------------------------|---------2-----------------|-----------------2---------------
|---------------------------------|-0-------------------------|-0-------------------------------

|---------------------------------|---------------------------------|---------------------------------
|-----------------0---------------|---------------------------------|---------------------0-----------
|-3-----------3-------3-------3---|-------------0---------------0---|-------------0-----------0-------
|-2---2-------------------2-------|-2---2-----------2---2-----------|-2---2-----------2---------------
|---------2-----------------------|---------2---------------2-------|---------2-------------------2---
|-0-------------------------------|-0---------------0---------------|-0---------------0---------------

|---------------------------------|---------------------------------|---------------------------------
|-0-------------------------------|-------------0---------------0---|-------------0-------------------
|-----3-----------3-----------3---|-1---------------1-------1-------|-3---------------3-----------3---
|---------2-----------2-----------|-----2---------------2-----------|-----2---------------2-----------
|-------------2-----------2-------|---------2-----------------------|---------2---------------2-------
|-0-------------------------------|-0-------------------------------|-0-------------------------------

|---------------------------------|---------------------------------|---------------------------------
|-----------------0---------------|---------------------------------|---------------------------------
|-1-----------1-------1-------1---|-0-----------0-----------0-------|-0-----------0-----------0-------
|-----2-------------------2-------|-----2-----------2-----------2---|-----2-----------2-----------2---
|---------2-----------------------|---------2-----------2-----------|---------2-----------2-----------
|-0-------------------------------|-0-------------------------------|-0-------------------------------

|---------------------------------|---------------------------------|---------------------------------
|---------------------------------|---------------------------------|---------------------------------
|---------------------------------|---------------------------------|-0---------------0---------------
|-2-----------2-----------2-------|-2---------------2-------2-------|-----2-------2-------2-------2---
|-----1-----------1-----------1---|-----2-------2-------2-------2---|---------2---------------2-------
|-2-------2-----------2-----------|-0-------0-----------------------|-3-------------------------------

|---------------------------------|---------------------------------|---------------------------------
|---------------------------------|---------------------------------|---------------------------------
|-0---------------0---------------|-0---------------0---------------|-0---------------0---------------
|-----2-------2-------2-------2---|-----2-------2-------2-------2---|-----2-------2-------2-------2---
|---------2---------------2-------|---------2---------------2-------|---------2---------------2-------
|-0-------------------------------|-3-------------------------------|-0-------------------------------

|---------------------------------|---------------------------------|---------------------------------
|---------------------------------|---------------------------------|---------------------------------
|-0---------------0---------------|-0---------------0---------------|-0---------------0---------------
|-----2-------2-------2-------2---|-----2-------2-------2-------2---|-----2-------2-------2-------2---
|---------2---------------2-------|---------2---------------2-------|---------2---------------2-------
|-3-------------------------------|-0-------------------------------|-3-------------------------------

|---------------------------------
|---------------------------------
|-0---------------0---------------
|-----2-------2-------2-------2---
|---------2---------------2-------
|-0-------------------------------
''')


bodysnatchers = stored.Composition(transposition, 
	fretted.Tab(
		fretted.Tuning(chordtext.parse('d2-a2-d3-g3-b3-e4'), capo=0), 
		17, characters_per_note=3
	)
).parse('''
|--------------------------------------------
|--------------------------------------------
|--------------------------------------------
|--------------------------------10-12-12----
|--9-----10----12----------10-12-------------
|--0-----0-----0-----10-12-------------------

|--------------------------------------------
|--------------------------------------------
|--------------------------------------------
|--------------------------------10-12-12----
|--9-----10----12----------10-12-------------
|--0-----0-----0-----10-12-------------------

|--------------------------------------------
|--------------------------------------------
|--------------------------------------------
|--------------------------------10-12-12----
|--9-----10----15----------10-12-------------
|--0-----0-----0-----10-12-------------------

|--------------------------------------------
|--------------------------------------------
|--------------------------------------------
|--------------------------------10-12-12----
|--9-----10----14----------10-12-------------
|--0-----0-----0-----10-12-------------------
''')

bodysnatchers2 = stored.Composition(transposition, 
	fretted.Tab(
		fretted.Tuning(chordtext.parse('d2-a2-d3-g3-b3-e4'), capo=0), 
		17, characters_per_note=2
	)
).parse('''
|-----------------------------
|-----------------------------
|-----------------------------
|----------2-0----------2-0---
|----0-2-3--------0-2-3-------
|--0-0---------0--0-----------
''')

airbag = stored.Composition(transposition, 
	fretted.Tab(
		fretted.Tuning(chordtext.parse('e2-a2-d3-g3-b3-e4'), capo=0), 
		17, characters_per_note=2
	)
).parse('''
|-------------|---------|-------------|-------------
|-------------|---------|-------------|-------------
|-------------|---------|-------------|-------------
|-------------|---------|-------------|-------------
|-------------|---------|-------------|-------------
|-0-1-8-7-9-5-|-0-1-8-7-|-5-9-12138-7-|-9-5-0-1-8-7-
''')

far_leys = stored.Composition(transposition, 
	fretted.Tab(
		fretted.Tuning(chordtext.parse('d3-a3-d4-g4-a4-d5'), capo=0), 
		17, characters_per_note=1
	)
).parse('''
|-4-----2|-----0--|--------|--0-----|
|----0---|---0----|-0--0--0|--------|
|--0--0--|-0-----0|--2-44-4|7--7-0-0|
|---0--0-|--0---0-|---0--0-|-0--0-0-|
|2-------|2-------|--------|------0-|
|--------|--------|0-------|--------|

|-4-----0|-----0--|--------|--0-----|
|----0---|---45---|-0--0--0|--------|
|--0--0--|-0-----0|--2-44-s|7--7-0-0|
|---0--0-|--0---0-|---0--0-|-0--0-0-|
|2-------|2-------|--------|-----(0)|
|--------|--------|0-------|--------|

|-4-----2|-----0--|--------|--0-----|
|----0---|---0----|-0--0--0|--------|
|--0--0--|-0-----0|--2-44-4|7--7-0-0|
|---0--0-|--0---0-|---0--0-|-0--0-0-|
|2-------|2-------|--------|------0-|
|--------|--------|0-------|--------|

|-4-----0|-----0--|--------|--0-----|
|----0---|---45---|-0--0--0|--------|
|--0--0--|-0-----0|--2-44-s|7--7-0-0|
|---0--0-|--0---0-|---0--0-|-0--0-0-|
|2-------|2-------|--------|-----(0)|
|--------|--------|0-------|--------|

|-4-----2|-----0--|--------|--0-----|
|----0---|---0----|-0--0--0|--------|
|--0--0--|-0-----0|--2-44-4|7--7-0-0|
|---0--0-|--0---0-|---0--0-|-0--0-0-|
|2-------|2-------|--------|------0-|
|--------|--------|0-------|--------|

|----0---|--------|--------|----0---|
|--------|----0---|-0--0--0|-0------|
|-0------|-0------|--2--0--|--2-----|
|--0--0-0|--4--0-0|---0----|---0----|
|2--2--0-|---0--0-|------2-|--------|
|--------|2-------|0-------|0-------|

|-------7|--------|--------|--------|
|----7---|--------|----0---|-0--0---|
|-7------|---7--7-|-0-----0|--------|
|--t--t--|-t---t-t|--t--0--|--4--0-0|
|---7--7-|--7-----|---0--0-|---0--0-|
|7-------|7---7---|0-------|0-------|

|-------7|--------|--------|--------|
|----7---|--------|----0---|-0--0---|
|-7------|---7--7-|-0-----0|--------|
|--t--t--|-t---t-t|--t--0--|--4--0-0|
|---7--7-|--7-----|---0--0-|---0--0-|
|7-------|7---7---|0-------|0-------|

|-------7|--------|--------|--------|
|----7---|--------|----0---|-0--0---|
|-7------|---7--7-|-0-----0|--------|
|--t--t--|-t---t-t|--t--0--|--4--0-0|
|---7--7-|--7-----|---0--0-|---0--0-|
|7-------|7---7---|0-------|0-------|

|-------7|--------|--------|--------|
|----7---|--------|----0---|-0--0---|
|-7------|---7--7-|-0-----0|--------|
|--t--t--|-t---t-t|--t--0--|--4--0-0|
|---7--7-|--7-----|---0--0-|---0--0-|
|7-------|7---7---|0-------|0-------|

|-4-----2|-----0--|--------|--0-----|
|----0---|---0----|-0--0--0|--------|
|--0--0--|-0-----0|--2-44-4|7--7-0-0|
|---0--0-|--0---0-|---0--0-|-0--0-0-|
|2-------|2-------|--------|------0-|
|--------|--------|0-------|--------|

|-4-----0|-----0--|--------|--0-----|
|----0---|---45---|-0--0--0|--------|
|--0--0--|-0-----0|--2-44-s|7--7-0-0|
|---0--0-|--0---0-|---0--0-|-0--0-0-|
|2-------|2-------|--------|-----(0)|
|--------|--------|0-------|--------|

|-4-----2|-----0--|--------|--0-----|
|----0---|---0----|-0--0--0|--------|
|--0--0--|-0-----0|--2-44-4|7--7-0-0|
|---0--0-|--0---0-|---0--0-|-0--0-0-|
|2-------|2-------|--------|------0-|
|--------|--------|0-------|--------|

|-4-----0|-----0--|--------|--0-----|
|----0---|---45---|-0--0--0|--------|
|--0--0--|-0-----0|--2-44-s|7--7-0-0|
|---0--0-|--0---0-|---0--0-|-0--0-0-|
|2-------|2-------|--------|-----(0)|
|--------|--------|0-------|--------|

|----0---|--------|--------|--------|--------|--------|
|--------|----0---|-0--0--0|--0--0--|-0--0--0|-----0--|
|-0------|-0------|--2-s4--|7--6---0|--2-s4--|0-0----0|
|--0--0-0|--4--0-0|---0--0-|-0--0-0-|---0--0-|-4--0---|
|2--2--0-|---0--0-|--------|-----(0)|--------|---5--5-|
|--------|2-------|0-------|--------|0-------|--------|

|--------|--------|--------|--------|
|-0--0--0|--0--0--|-0--0--0|-----0--|
|--2-s4--|7--6---0|--2-s4--|0-0----0|
|---0--0-|-0--0-0-|---0--0-|-4--0---|
|--------|-----(0)|--------|---5--5-|
|0-------|--------|0-------|--------|

|--------|--------|--------|-----0--|
|----0---|----0---|----0---|---0----|
|-0-----0|-0-----0|-0-----0|--0----0|
|--0--0--|--0--0--|--0--0--|-4----4-|
|---4--4-|---4--4-|---4--4-|----0---|
|2-------|2-------|2-------|0-------|

|--------|--------|--------|-----0--|
|----0---|----0---|----0---|---0----|
|-0-----0|-0-----0|-0-----0|--0----0|
|--0--0--|--0--0--|--0--0--|-4----4-|
|---4--4-|---4--4-|---4--4-|----0---|
|2-------|2-------|2-------|0-------|

|--------|--------|--------|-----0--|
|----0---|----0---|----0---|---0----|
|-0-----0|-0-----0|-0-----0|--0----0|
|--0--0--|--0--0--|--0--0--|-4----4-|
|---4--4-|---4--4-|---4--4-|----0---|
|2-------|2-------|2-------|0-------|

|-4-----2|-----0--|----0---|--------|
|----0---|---0----|-0-----0|--0--0--|
|--0--0--|-0-----0|--2--2--|2--2----|
|---0--0-|--0---0-|---0--0-|-0--0--0|
|2-------|2-------|--------|------0-|
|--------|--------|0-------|--------|
                   
|-4-----0|-----0--|--------|--------|
|----0---|---4b---|-0--0--0|--0--0--|
|--0--0--|-0-----0|--2--4--|0--2----|
|---0--0-|--0---0-|---0--0-|-0--0--0|
|2-------|2-------|--------|------0-|
|--------|--------|0-------|--------|

|-4-----2|-----0--|----0---|--------|
|----0---|---0----|-0-----0|-0--0---|
|--0--0--|-0-----0|--2--0--|--2--2-0|
|---0--0-|--0---0-|---0----|---0--0-|
|2-------|2-------|------2-|--------|
|--------|--------|0-------|0-------|

|----0---|--------|----0---|----0---|----0---|----0---|
|--------|----0---|-0-----0|-0-----0|-0-----0|-0------|
|-0------|-0------|--2--2--|--2--2--|--2--2--|--2--0-0|
|--0--0-0|--4--0-0|---0--0-|0--0--0-|0--0--0-|0--0--0-|
|2--2--0-|---0--0-|--------|--------|--------|--------|
|--------|2-------|0-------|--------|--------|--------|

|----t---|---t----|----4---|---4----|
|-0-----0|------(0)-0-----0|------(0)
|--0--0--|-0---0-0|--0--0--|-0---0-0|
|---t--t-|--t---t-|---4--4-|--4---0-|
|--------|--------|--------|--------|
|0-------|--------|0-------|--------|

|----t---|---t----|----4---|---4----|
|-0-----0|------(0)-0-----0|------(0)
|--0--0--|-0---0-0|--0--0--|-0---0-0|
|---t--t-|--t---t-|---4--4-|--4---0-|
|--------|--------|--------|--------|
|0-------|--------|0-------|--------|

|----t---|---t----|----4---|---4----|
|-0-----0|------(0)-0-----0|------(0)
|--0--0--|-0---0-0|--0--0--|-0---0-0|
|---t--t-|--t---t-|---4--4-|--4---0-|
|--------|--------|--------|--------|
|0-------|--------|0-------|--------|

|-4-----4|--------|----4
|----0---|---0----|-0---
|--0--0--|-0---0-0|--2--
|---0----|--0---0-|---0-
|2-----2-|--------|-----
|--------|--------|0----

|----79--|4-------|----20--|2-------|
|-0------|--0--0--|-0------|---0----|
|--7---7-|---7---0|--1---1-|-1---1-1|
|---0---0|-0----0-|---0---0|--0---0-|
|--------|--------|--------|--------|
|0-------|--------|0-------|--------|

|----20--|----40--|--------|--------|
|-0------|-0------|-0--0--0|--------|
|--1----0|--0----0|--2-s4--|7-------|
|---0--0-|---0--0-|---0--0-|--------|
|2-------|2-------|--------|--------|
|--------|--------|0-------|--------|

|----79--|4-------|----20--|2-------|
|-0------|--0--0--|-0------|---0----|
|--7---7-|---7---0|--1---1-|-1---1-1|
|---0---0|-0----0-|---0---0|--0---0-|
|--------|--------|--------|--------|
|0-------|--------|0-------|--------|

|----20--|----40--|--------|--------|
|-0------|-0------|-0--0--0|--------|
|--1----0|--0----0|--2-s4--|7-------|
|---0--0-|---0--0-|---0--0-|--------|
|2-------|2-------|--------|--------|
|--------|--------|0-------|--------|

|--------|--------|--------|----0---|
|-0--0--0|--0--0--|-0--0---|-0------|
|--5--4--|5--4--5-|--5-45-0|--0----0|
|---4--3-|-4--3--4|---434--|---2--0-|
|--------|--------|--------|2-------|
|0-------|--------|0-------|--------|

|--------|--------|--------|2----530|
|-0--0--0|--0--0--|-0--0---|2----530|
|--5--4--|5--4--5-|--5-45-0|2----530|
|---4--3-|-4--3--4|---434--|0----002|
|--------|--------|--------|0----000|
|0-------|--------|0-------|0----000|
''')

parasite = stored.Composition(transposition, 
	fretted.Tab(
		fretted.Tuning(chordtext.parse('c2-g2-c3-f3-c4-e4'), capo=3), 
		17, characters_per_note=1
	)
).parse('''
|------0-----|------0-----|------0-----|------0-----|------0-----| 
|---0-----0--|---0-----0--|---0-----0--|---0-----0--|---0-----0--| 
|5-----5-----|4-----4-----|3-----3-----|02----2-----|02----2-----| 
|---0-----0--|---0-----0--|---0-----0--|---0-----0--|---0-----0--| 
|--0---0-0-0-|--0---0-0-0-|--0---0-0-0-|--0---0-0-0-|--0---0-0-0-| 
|0---0-------|0---0-------|0---0-------|0---0-------|0---0-------|
''')

three_hours = stored.Composition(transposition, 
	fretted.Tab(
		fretted.Tuning(chordtext.parse('b1-b2-d3-g3-b3-e4'), capo=0), 
		17, characters_per_note=1
	)
).parse('''
|--0---0---0-------
|4---4---4-------0-
|--0---0---0----4--
|4---4---4-----4---
|0------------0----
|------------0-----
''')
('''

|----2-----2---------------------
|----0-----0-----3-----2---0-----
|----4-----4-----4-----4---4-----
|----4--4--4--4--4--4--4---4-----
|0-----0-----0-----0-----0---0---
|--0-----0-----0-----0---------0-

|------0---------|------0---------|------1---------|------1---------| 
|0-----0---------|2-----2---------|3-----3---------|3-----3-----3---| 
|2-----2---------|0-----0---------|0-----0---------|0-----0-----0---| 
|2--2------2-----|2--2------2-----|3--3------3-----|3--3------3-3---| 
|0-0-0-0-0---0---|0-0-0-0-0---0---|0-0-0-0-0---0---|0-0-0-0-0---0---| 
|--------------0-|--------------0-|--------------0-|--------------0-|

|----2----(2)---(2)---(2)--------|
|----0-----0-----0-----0---------|
|----4-----4-----4-----4---2-----|
|----4--4--4--4--4--4--4-----0---|
|0-----0-----0-----0-----02------|
|--0-----0-----0-----0---------0-|

|-----2---0-2-------0-------------|------------------0-------2-----
|-0---0---0-0---3-----2---0-------|0-----2---2-----4---4-0---0-0---
|-4---4---4-4---4---4-4---4-------|2-----0---0-------0---4---4-4---
|-4-------------4-----4---4-------|2--2--2---2-----4---4-4-----4---
|---0---0-----0---0-----0---0---0-|--0---------0---0-------0---0---
|-----------------------------0---|----0---0-----0---------------0-

|------0--2--0-----
|---4-----------4--
|--4-4---4-4---4-4-
|-4---4-4---4-4---4
|0-----------------
|------------------

|------1--
|---3-----
|--0-0--0-
|-3---3--3
|0--------
|---------

|-----(0)-
|---0--0--
|--1-1--1-
|-2---2--2
|0--------
|---------

|---------
|---0--0--
|--2-2--2-
|-4---4--4
|0--------
|---------

|------0--7--0-----
|---7-----7-----7--
|--7-7---7-7---7-7-
|-7---7-7---7-7---7
|0-----0-----0-----
|------------------

|------0-----0-----
|---7-----7-----7--
|--6-6---6-6---6-6-
|-5---5-5---5-5---5
|0-----0-----0-----
|------------------

|------0-----0-----
|---7-----7-----7--
|--7-7---7-7---7-7-
|-6---6-6---6-6---6
|0-----0-----0-----
|------------------

|------0-----0-----
|---7-----7-----7--
|--6-6---6-6---6-6-
|-5---5-5---5-5---5
|0-----0-----0-----
|------------------

|------0-----0-----
|---7-----7-----7--
|--7-7---7-7---7-7-
|-7---7-7---7-7---7
|0-----0-----0-----
|------------------

|---------|---------
|---0--0--|---0--0--
|--4-4--2-|--4-4--4-
|-4---4--2|-4---4--4
|0--------|0--------
|---------|---------


|------2--0--------
|---0--------3--2--
|--4-4--4--4--4--4-
|-4---4--4--4--4--4
|0-----0--0--0--0--
|------------------

|------0-----------|------2--0--------
|---0--0-----0--0--|---0--------3--2--
|--2-2--2---2-2--2-|--4-4--4--4--4--4-
|-2---2--2-2---2--2|-4---4--4--4--4--4
|0-----0--0--------|0-----0--0--0--0--
|------------------|------------------

|-----(0)-
|---0--0--
|--1-1--1-
|-2---2--2
|0--------
|---------

|---------
|---0--0--
|--2-2--2-
|-4---4--4
|0--------
|---------


|---------
|---0--0--
|--4-4--4-
|-4---4--4
|0--------
|---------

|------2-----2-----
|---0-----0-----0--
|--4-4---4-4---4-2-
|-4---4-4---4-4---2
|0-----0-----0-----
|------------------

|----------------|----------------
|--2--4-5-4-2-4--|--2--5--4--4----
|----------------|----------------
|--2--4-5-4-2-4--|--2--5--4--4----
|--0---0-0-0-0-0-|--0---0-0-0-0-0-
|0---0-----------|0---0-----------

|---0-------2-----|---0-------2-----|---------0-----0-|---0-------2-----
|-4---4-0---0-0---|-4---4-0---0-0---|-0-----2-----3---|-4---4-0---0-0---
|---0---4---4-4---|---0---4---4-4---|-2-2-----0-----0-|---0---4---4-4---
|-4---4-4-----4---|-4---4-4-----4---|-----2-2---2-3---|-4---4-4-----4---
|-0-------0-------|-0-------0-------|-0-----0-----0---|-0-------0-------
|---------------0-|---------------0-|-----------------|---------------0-

|-----------------|-----------------
|---2--4-5-4-2-4--|---2--5--4--4----
|-----------------|-----------------
|---2--4-5-4-2-4--|---2--5--4--4----
|---0---0-0-0-0-0-|---0---0-0-0-0-0-
|-0---0-----------|-0---0-----------


|-2-----0-------------------------|-------0---------
|---0-----0---3-----2-----0-------|-0-------2-------
|-----4-----4---4-----4-----4-----|---2-------0-----
|-----------------4-----4-----4---|-----2-------2---
|-0-----0-----0-----0-----0-----0-|-0-----0-------0-
|---------------------------------|-----------------

|-----2-----2-----2-----2---------
|-----0-----0-----0-----0---------
|-----4-----4-----4-----4---2-----
|-----4--4--4--4--4--4--4-----0---
|-0-----0-----0-----0-----02------
|---0-----0-----0-----0---------0-

|---2---0-2-----|---0-------------|---------------|---0-----2-------
|---0---0-0-0---|-3---2-0---------|---0-----2-----|-4---4---------0-
|---4---4-4-----|-4-4-4-4-----4---|---2-----0-----|---0-----4---4---
|-----------4---|-4---4-4-----4---|---2-----2-----|-4---4-----------
|-0---0-------0-|-----------------|-0---0-----0---|-0-----0---0-----
|---------------|---------------0-|-------0-----0-|-----------------

|-2--2--2-0-2-----|---0-------------|-----------------|-----
|----0--0-0-0---3-|-----2---0-------|-----0-------2---|-----
|----4--4-4-4---4-|---4-4---4-------|-----2-------0---|-----
|---------------4-|-----4---4---4---|-----2-------2---|---2-
|------0-0----0---|-0-----0-------0-|---0---0---0-----|-----
|-----------------|-----------------|-0-------0-------|-----


|---2---0-2-----|---0-------------|---------------|---0-----2-------
|---0---0-0-0---|-3---2-0---------|---0-----2-----|-4---4---------0-
|---4---4-4-----|-4-4-4-4-----4---|---2-----0-----|---0-----4---4---
|-----------4---|-4---4-4-----4---|---2-----2-----|-4---4-----------
|-0---0-------0-|-----------------|-0---0-----0---|-0-----0---0-----
|---------------|---------------0-|-------0-----0-|-----------------

|-2--2--2-0-2-----|---0-------------|-----------------|------
|----0--0-0-0---3-|-----2---0-------|-----0-------2---|------
|----4--4-4-4---4-|---4-4---4-------|-----2-------0---|------
|---------------4-|-----4---4---4---|-----2-------2---|----2-
|------0-0----0---|-0-----0-------0-|---0---0---0-----|------
|-----------------|-----------------|-0-------0-------|------
''')

introduction = stored.Composition(transposition, 
	fretted.Tab(
		fretted.Tuning(chordtext.parse('d2-a2-d3-g3-b3-e4'), capo=0), 
		17, characters_per_note=3
	)
).parse('''
|--------------------------2------------------------
|-----------------3-----------3---------------------
|--------------5-----5-----------5------------------
|-----------0-----------0-----------0---------------
|--------0-----------------------------0-----0------
|--0------------------------------------------------

--------------------------2------------------------
-----------------3-----------------3---------------
--------------4--------4--------4-----4------------
-----------0--------0--------0-----------0---------
--------0-----------------------------------0------
--0------------------------------------------------

--------------------------2------------------------
-----------------3-----------------3---------------
--------------0--------0--------0-----0------------
-----------4--------4--------4-----------4---------
--------0-----------------------------------0------
--0------------------------------------------------

--------------------------2------------------------
-----------------3-----------------3---------------
--------------2--------2--------2-----2------------
-----------0--------0--------0-----------0---------
--------0-----------------------------------0------
--0------------------------------------------------

--------------------------3------------------------
-----------------3-----------------3---------------
--------------4--------4--------4-----4------------
-----------0--------0--------0-----------0---------
--------0-----------------------------------0------
--0------------------------------------------------

--------------------------2------------------------
-----------------3-----------------3---------------
--------------4--------4--------2-----2------------
-----------0--------0--------0-----------0---------
--------0-----------------------------------0------
--0------------------------------------------------

--------------------------2--------0---------------
-----------------3--------------------------3------
--------------0--------0--------0--------0---------
-----------4--------4--------4--------4------------
--------0------------------------------------------
--0------------------------------------------------

--------------------------2------------------------
-----------------3-----------3-----3---------------
--------------2--------2--------2-----2------------
-----------0--------0--------------------0---------
--------0-----------------------------------0------
--0------------------------------------------------
''')

pyaudio = PyAudio()
play = played.sound(
    pyaudio.open(format=pyaudio.get_format_from_width(1), # open stream
        channels=1,
        rate=41900,
        output=True
    ), 41900
)

staffed = staff(far_leys)
print(stafftext.format(staffed))
print(sequencer.format(staffed))
play(played.staff(et12, played.sine(0.1), 4) (staffed), len(staffed)/4)
