from PageHTMLGenerator import *



def getHTMLPages():
	htmlPages = []
	for i in range(50):
		html = generateHTML()
		page = 'page' + str(i+1) + '.html'
		f = open(page,"w")
		f.write(html)
		f.close()
		htmlPages.append(page)

	return htmlPages


getHTMLPages()