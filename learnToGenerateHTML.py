from GenerateDataSet import *
from KClusterBasedOnColor import *
import numpy as np
import keras

def createData(numSamples):
    xSamples = []
    ySamples = []
    print "about to get HTML pages"
    _, vectorHTMLs, pageNames = getHTMLPages(numSamples)
    print "finished getting HTML pages"
    print "start segmenting"
    i = 0
    for img in pageNames:
        segments = k_cluster(img)
        
##        #1. Turn the whole image black and white (test out if this makes sense
##        #for vector0 (body)
##        img_gray = cv2.imread(img, 0)
##        img_gray = cv2.resize(img_gray,(0,0), fx=0.5, fy=0.5)
##        (thresh, img_bw) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
        
        #   Gridify? TODO: maybe
        
        #2. Match vectorHTMLs with segments
        #   Currently assuming that vec 2-4 are in random order
        xEntry = [segments[0], segments[1]]
        yEntry = [vectorHTMLs[i][0], vectorHTMLs[i][1]]
        #go over middle vectors that are in random order
        addedVectors = 0
        while addedVectors < 3:
            for vec in vectorHTMLs[i][2:-1]:
                if vec[-2] == addedVectors + 1:
                    yEntry.append(vec)
                    #-2 index is "order" according to generateVectorHTML
                    xEntry.append(segments[vec[-2]+1])
                    addedVectors += 1
            
        
        xEntry.append(vectorHTMLs[-1])
        yEntry.append(segments[-1])

        #3. convert to numpy arrays
        xEntry = np.array(xEntry)
        yEntry = np.array(yEntry)

        #4. Normalize vectorHTMLs from 0-1
        

        #5. Add to xSamples and ySamples
        xSamples.append(xEntry)
        ySamples.append(yEntry)
        print xEntry.shape, yEntry.shape
        print ("segment " + str(i) + " done")

        i += 1
        
    print "all done with creating data"
    #   convert to numpy arrays
    xSamples = np.array(xSamples)
    ySamples = np.array(ySamples)
    print xSamples.shape, ySamples.shape
    return xSamples, ySamples

createData(2)
