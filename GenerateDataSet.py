from VectorHTMLGenerator import *
from HTMLToImage import *
import os

def normalizeVectorHTML(vectorHTML, ranges):
    vecCopy = np.copy(vectorHTML).astype(float)
    for i in range(vecCopy.shape[0]):
        vecCopy[i][0] = 0
        vecCopy[i][6] = 0
        for j, attr in enumerate(sorted(ranges.iterkeys())):
                vecCopy[i][j] /= (len(ranges[attr])-1)
    
    return vecCopy

def denormalizeVectorHTML(normVectorHTML, ranges):
    vecCopy = np.copy(normVectorHTML)
    for i in range(vecCopy.shape[0]):
        for j, attr in enumerate(sorted(ranges.iterkeys())):
                vecCopy[i][j] *= (len(ranges[attr])-1)
    
    return np.around(vecCopy).astype(int)


def getHTMLPages(numPagesGen, training, trainpath, testpath):
        htmlPages = []
        vectorHTMLs = []
        pageNames = []
        HTMLRanges = buildRangesDictionary()
        driver = open_driver()  #from HTMLToImage
        path = trainpath
        if training == False:
                path = testpath
        for i in range(numPagesGen):
                vectorHTML = generateVectorHTML(HTMLRanges)

                html = convertToHTML(vectorHTML, HTMLRanges)
                vectorHTMLs.append(vectorHTML)
                page = path+'/page' + str(i+1) + '.html'
                f = open(page,"w")
                f.write(html)
                f.close()
                htmlPages.append(page)
                #       Generate image from html
                url = 'file:///'+os.getcwd() +'/' + page
                url = url.replace('\\', '/')
                picName = path+'/page'+str(i+1)+'.png'
                save_html_into_image(driver, url, picName)
                pageNames.append(picName)
                #       Or get png data directly
                #screenshot = get_binary_data_from_url()
        quit_driver(driver)   #from HTMLToImage
        return htmlPages, vectorHTMLs, pageNames, HTMLRanges

##getHTMLPages(5)

##getHTMLPages(1, True, "test_data/","train_data/")
