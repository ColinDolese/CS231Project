import random
from yattag import Doc


def generateHTML():
	doc, tag, text, line = Doc().ttl()
	model = random.randint(1,3)
	html = ''
	if model == 1:
		html = model1(doc, tag, text, line)
	elif model == 2:
		html = model2(doc, tag, text, line)
	elif model == 3:
		html = model3(doc, tag, text, line)

	return html



def htmlColor(r, g, b):
    def _chkarg(a):
        if isinstance(a, int): # clamp to range 0--255
            if a < 0:
                a = 0
            elif a > 255:
                a = 255
        elif isinstance(a, float): # clamp to range 0.0--1.0 and convert to integer 0--255
            if a < 0.0:
                a = 0
            elif a > 1.0:
                a = 255
            else:
                a = int(round(a*255))
        else:
            raise ValueError('Arguments must be integers or floats.')
        return a
    r = _chkarg(r)
    g = _chkarg(g)
    b = _chkarg(b)
    return '#{:02x}{:02x}{:02x}'.format(r,g,b)


def model1(doc, tag, text, line) :
	order = [1,2,3]
	random.shuffle(order)

	doc.asis('<!DOCTYPE html>')
	with tag('style'):
		doc.asis('* { box-sizing: border-box; }')
		doc.asis('body { display: flex; min-height: 100vh; flex-direction: column; margin: 0; }')
		doc.asis('#main { display: flex; flex: 1; }')
		doc.asis('#main > article { flex: 1; background:' 
			+ str(htmlColor(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
			+'; order:' + str(order[0]) + '; }')
		doc.asis('#main > nav { flex: 0 0 20vw; background:' 
			+ str(htmlColor(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
			+'; order: ' + str(order[1]) + ';}')
		doc.asis('#main > aside { flex: 0 0 20vw; background:' 
			+ str(htmlColor(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
			+'; order: ' + str(order[1]) + ';}')
		doc.asis('#main > nav { order:' + str(order[2]) + '; }')
		doc.asis('header {background: '  
			+ str(htmlColor(random.randint(0,255),random.randint(0,255),random.randint(0,255))) 
			+ '; height: 20vh; }')
		doc.asis('footer { background: '  
			+ str(htmlColor(random.randint(0,255),random.randint(0,255),random.randint(0,255))) 
			+ '; height: 20vh; }')
		doc.asis('header, footer, article, nav, aside { padding: 1em; }')

	with tag('body'):
		with tag('header'):
			text('Header')

		with tag('div', id='main'):
			with tag('article'):
				text('Article')
			with tag('nav'):
				text('Nav')
			with tag('aside'):
				text('Aside')

		with tag('footer'):
			text('Footer')

	return doc.getvalue()


def model2(doc, tag, text, line):
	directions = ['','', '']
	for i in range(len(directions)):
		rand = random.randint(0,1)
		if (rand == 0):
			directions[i] = 'row'
		else:
			directions[i] = 'column'

	with tag('style'):
		doc.asis('* { box-sizing: border-box; }')
		doc.asis('body { display: flex; min-height: 100vh; flex-direction:' + directions[0] + '; margin: 0; }')
		doc.asis('.col-1 { background:' 
			+ str(htmlColor(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
			+'; flex: 1; }')
		doc.asis('.col-2 { display:flex; flex-direction:' + directions[1] + '; flex: 5; }')
		doc.asis('.inner-row { display: flex; flex-direction: ' + directions[2] + '; }')
		doc.asis('.inner-col { flex:4; }')
		doc.asis('.inner-row article { min-height: 60vh; background:' 
			+ str(htmlColor(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
			+';}')
		doc.asis('.inner-row aside { background:' 
			+ str(htmlColor(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
			+'; flex: 1; }')
		doc.asis('header {background: '  
			+ str(htmlColor(random.randint(0,255),random.randint(0,255),random.randint(0,255))) 
			+ '; height: 20vh; }')
		doc.asis('footer { background: '  
			+ str(htmlColor(random.randint(0,255),random.randint(0,255),random.randint(0,255))) 
			+ '; height: 20vh; }')
		doc.asis('header, footer, article, nav, aside { padding: 1em; }')

	with tag('body'):
		with tag('nav', klass='col-1'):
			text('Nav')

		with tag('div', klass='col-2'):
			with tag('header'):
				text('Header')
			with tag('div', klass='inner-row'):
				with tag('div', klass='inner-col'):
					with tag('article'):
						text('Article')
					with tag('footer'):
						text('Footer')
				with tag('aside'):
					text('Aside')

	return doc.getvalue()


def addColumn(num, tag, text):
	with tag('div', klass='column'):
		for i in range(num):
			with tag('div'):
				text(i+1)


def addRow(num, tag, text):
	with tag('div', klass='wrapper'):
		for i in range(num):
			with tag('div'):
				text(i+1)


def model3(doc, tag, text, line):

	vertical = bool(random.getrandbits(1))
	horizontal = bool(random.getrandbits(1))


	doc.asis('<!DOCTYPE html>')
	with tag('style'):
		doc.asis('.wrapper { display: flex; }')
		if vertical:
			doc.asis('.column { display: flex; flex-direction: column; }')
			doc.asis('.column > div { font-size: 4vh; color: white; background: ' 
			+ str(htmlColor(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
			+'; margin: .1em; padding: .3em 1em; border-radius: 3px; flex: 1; }')
		if horizontal or not vertical:
			doc.asis('.wrapper > div { font-size: 4vh; color: white; background: ' 
			+ str(htmlColor(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
			+'; margin: .1em; padding: .3em; border-radius: 3px; flex: 1; }')

	if vertical:
		with tag('div', klass='wrapper'):

			for i in range(random.randint(0,10)):
				addColumn(i, tag, text)

			for i in reversed(range(random.randint(0,10))):
				addColumn(i, tag, text)

	if horizontal or not vertical:

		for i in range(random.randint(0,10)):
			addRow(i, tag, text)

		for i in reversed(range(random.randint(0,10))):
			addRow(i, tag, text)


	return doc.getvalue()









