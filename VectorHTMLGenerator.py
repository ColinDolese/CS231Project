import random
import numpy as np
from yattag import Doc


def buildRangesDictionary():

	minHeightRange = ['']
	for i in range(50, 100):
		minHeightRange.append(str(i) + 'vh')

	marginRange = ['']
	for i in range(20):
		marginRange.append(str(i))

	heightRange = ['']
	for i in range(1, 25):
		heightRange.append(str(i) + 'vh')

	flexRange = ['']
	for i in range(1,25):
		for j in range(1,25):
			for k in range(1,25):
				flexRange.append(str(i) + ' ' + str(j) + ' ' + str(k) + 'vw')

	colorRange = ['']
	for i in range(0,255):
		for j in range(0,255):
			for k in range(0,255):
				colorRange.append(str(htmlColor(i,j,k)))


	ranges = {}
	ranges['background'] = colorRange
	ranges['display'] = ['', 'flex']

	ranges['min-height'] = minHeightRange

	ranges['flex-direction'] = ['', 'column']

	ranges['margin'] = marginRange

	ranges['height'] = heightRange


	ranges['order'] = ['', '1', '2', '3']

	ranges['flex'] = flexRange

	ranges['padding'] = ['', '1em']

	return ranges





def generateVectorHTML(HTMLRanges):
	order = [1,2,3]
	random.shuffle(order)
	vector = np.zeros((6,len(HTMLRanges)), dtype=int)

	# vector: [display, flex, flex-direction, height, margin, min-height, order, padding]
	vector[0] = np.array([0,1,0 ,1, 0,  random.randint(1,len(HTMLRanges['margin'])-1), random.randint(1,len(HTMLRanges['min-height'])-1), 0, 0])
	vector[1] = np.array([random.randint(1, len(HTMLRanges['background'])-1),0, 0, 0, random.randint(1,len(HTMLRanges['height'])-1),  0, 0, 0, 1])
	vector[2] = np.array([random.randint(1, len(HTMLRanges['background'])-1),0, random.randint(1, len(HTMLRanges['flex'])-1), 0, 0, 0, 0, order[0], 1])
	vector[3] = np.array([random.randint(1, len(HTMLRanges['background'])-1),0, random.randint(1, len(HTMLRanges['flex'])-1), 0, 0, 0, 0, order[1], 1])
	vector[4] = np.array([random.randint(1, len(HTMLRanges['background'])-1),0, random.randint(1, len(HTMLRanges['flex'])-1), 0, 0, 0, 0, order[2], 1])
	vector[5] = np.array([random.randint(1, len(HTMLRanges['background'])-1),0, 0, 0, random.randint(1,len(HTMLRanges['height'])-1),  0, 0, 0, 1])
	return vector
	
def convertToHTML(vectorHTML, ranges):
	doc, tag, text, line = Doc().ttl()
	return parseVectorHTML(vectorHTML, ranges, doc, tag, text, line)


def parseVectorHTML(vectorHTML, ranges, doc, tag, text, line):
	doc.asis('<!DOCTYPE html>')
	sectionTitles = ['body', 'header', '.class > article', '.class > aside', '.class > nav', 'footer']

	with tag('style'):
		doc.asis('* { box-sizing: border-box; }')
		doc.asis('.class { display: flex; flex:1; }')
		for i, title in enumerate(sectionTitles):
			background = str(htmlColor(random.randint(0,255), 
				random.randint(0,255),random.randint(0,255)))
			section = title + '{'
			for j, attr in enumerate(sorted(ranges.iterkeys())):
				section += attr + ':' + ranges[attr][vectorHTML[i][j]] + ';'

			section += '}'
			doc.asis(section)


	with tag('body'):
		with tag('header'):
##			text('vector1')
                        text('')
		with tag('div', klass='class'):
			with tag('article'):
##				text('vector2')
                                text('')
			with tag('nav'):
##				text('vector4')
                                text('')
			with tag('aside'):
##				text('vector3')
                                text('')
		with tag('footer'):
##			text('vector5')
                        text('')


	return doc.getvalue()


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












