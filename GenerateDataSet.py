from VectorHTMLGenerator import *
from HTMLToImage import *
import os

def getHTMLPages(numPagesGen):
        htmlPages = []
        vectorHTMLs = []
        pageNames = []
        HTMLRanges = buildRangesDictionary()
        driver = open_driver()  #from HTMLToImage
        for i in range(numPagesGen):
                vectorHTML = generateVectorHTML(HTMLRanges)
                vectorHTMLs.append(vectorHTML)
                html = convertToHTML(vectorHTML, HTMLRanges)
                page = 'page' + str(i+1) + '.html'
                f = open(page,"w")
                f.write(html)
                f.close()
                htmlPages.append(page)
                #       Generate image from html
                url = 'file:///'+os.getcwd() +'/' + page
                url = url.replace('\\', '/')
                picName = 'page'+str(i+1)+'.png'
                save_html_into_image(driver, url, picName)
                pageNames.append(picName)
                #       Or get png data directly
                #screenshot = get_binary_data_from_url()
        quit_driver(driver)   #from HTMLToImage
        return htmlPages, vectorHTMLs, pageNames

##getHTMLPages(5)
