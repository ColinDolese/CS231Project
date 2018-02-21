import random
from yattag import Doc


def generatePageHTML():
	return generateSections()

def convertToHTML(pageHTML):
	doc, tag, text, line = Doc().ttl()
	return parsePageHTML(doc, tag, text, line)


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


def generateBody():
	directions = ['row', 'column', 'column']
	random.shuffle(directions)
	body = 'body,'
	body += 'display: flex,'
	body += 'min-height: 100vh,'
	body += 'flex-direction: column,'
	body += 'margin: 0'
	body += '/'
	return body


def addClasses():
	classes = ''
	classes += '.class-'
	classes += 'article-'
	classes += 'nav-'
	classes += 'aside'
	classes += '/'
	classes += '.class,'
	classes += 'display:flex,'
	classes += 'flex:1'
	classes += '/'
	return classes

def generateSections():

	pageHTML = ''
	sectionTitles = ['header', 'article', 'aside', 'nav', 'footer']
	order = [1,2,3]
	random.shuffle(order)


	pageHTML += addClasses()
	pageHTML += generateBody()


	for i, item in enumerate(sectionTitles):
		pageHTML += str(item) + ','
		pageHTML += 'background:' + str(htmlColor(random.randint(0,255), 
					random.randint(0,255),random.randint(0,255))) + ','
		if item == 'header' or item == 'footer':
			pageHTML += 'height: ' + str(random.randint(1,25)) + 'vh' + ','
		else:
			pageHTML += 'height:,'
		if item == 'nav' or item == 'article' or item == 'aside':
			pageHTML += 'flex: ' + str(random.randint(1,25)) + ' '
			pageHTML += str(random.randint(1,25)) + ' ' + str(random.randint(1,25)) + 'vw,'
			pageHTML +=  'order:' + str(order[i % 3]) + ','
		else:
			pageHTML += 'flex:,'
			pageHTML +=  'order:;'


		pageHTML += 'padding: 1em'
		if i < len(sectionTitles)-1:
			pageHTML += '/'

	print(pageHTML)
	return pageHTML


def containedInClass(classes, section):
	for i in range(len(classes)):
		classInfo = classes[i].split('-')
		if section in classInfo:
			return i

	return -1

def parsePageHTML(pageHTML, doc, tag, text, line):
	sectionTitles = ['header', 'article', 'aside', 'nav', 'footer']
	sections = pageHTML.split('/')
	classes = sections[0].split(',')
	doc.asis('<!DOCTYPE html>')

	# parse CSS
	with tag('style'):
		doc.asis('* { box-sizing: border-box; }')
		for i in range(1, len(sections)):
			section = sections[i].split(',')

			for j in range(len(classes)):
				classInfo = classes[j].split('-')
				if (section[0] in classInfo) and (section[0] != classInfo[0]):
					section[0] = classInfo[0] +  ' > ' + section[0]


			doc.asis(str(section[0]) + '{')
			for j in range(1, len(section)):
				doc.asis(str(section[j]) + ';')

			doc.asis('}')
	
	# parse html

	index = 0

	with tag('body'):
		while(index < len(sectionTitles)):

			classIndex = containedInClass(classes, sectionTitles[index])
			if classIndex != -1:
				classInfo = classes[classIndex].split('-')
				with tag('div', klass=classInfo[0].split('.')[1]):
					while sectionTitles[index] in classInfo:
						with tag(sectionTitles[index]):
							text(sectionTitles[index])

						index += 1

			else:
				with tag(sectionTitles[index]):
					text(sectionTitles[index])
					index += 1


	return doc.getvalue()












