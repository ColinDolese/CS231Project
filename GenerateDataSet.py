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

from HTMLGenerator import *
from HTMLToImage import *
import os

def getHTMLPages():
        htmlPages = []
        driver = open_driver()  #from HTMLToImage
        for i in range(10):
                html = generateHTML()
                page = 'page' + str(i+1) + '.html'
                f = open(page,"w")
                f.write(html)
                f.close()
                htmlPages.append(page)
                #       Generate image from html
                url = 'file:///'+os.getcwd() +'/' + page
                url = url.replace('\\', '/')
                save_html_into_image(driver, url, 'page'+str(i+1)+'.png')
                #       Or get png data directly
                #screenshot = get_binary_data_from_url()
        quit_driver(driver)   #from HTMLToImage
        return htmlPages

getHTMLPages()
