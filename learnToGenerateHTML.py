from GenerateDataSet import *
from KClusterBasedOnColor import *
import keras

def createData(numSamples):
    xSamples = numpy.array([])
    ySamples = numpy.array([])

    _, vectorHTMLs, pageNames = getHTMLPages(numSamples)
    for img in pageNames:
        segments = k_cluster(img)
        #   Gridify?

        #   Match vectorHTMLs with segments

        #   Normalize vectorHTMLSs from 0-1

        #   Add to xSamples and ySamples

    return xSamples, ySamples
