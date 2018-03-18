import os
import pickle
import numpy as np
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import GradientBoostingRegressor
from learnToGenerateHTML import *
from VectorHTMLGenerator import *
from HTMLToImage import *

#0 - neural network
#1 - SVM
TEST_MODEL = 1
DATETIME = '2018_03_16-1244' #  Set this for the folder where your model resides
FILENAME = "experiment_models/"+DATETIME+'/svmModel.sav'

dateTimeNow = str(datetime.now().strftime("%Y_%m_%d-%H%M"))
TESTPATH ="test_data/"+dateTimeNow

NUM_TEST_SAMPLES_TO_CREATE = 1

def main():
    #set filename(for model) manually
    ranges = buildRangesDictionary()
    if TEST_MODEL == 1:
        X_test, Y_test, segment_colors = createData(NUM_TEST_SAMPLES_TO_CREATE, False)
        loaded_model = pickle.load(open(FILENAME, 'rb'))
        score = loaded_model.score(X_test, Y_test)
        print "Score of the model on the test: "
        print score
        #   example for test prediction output:
        #get first 6 segments from test:
        oneHTML_X = X_test[0:6]
        oneHTML_Y = Y_test[0:6]
        pred_VectorHTML = []
        for i in range(len(oneHTML_X)):
            seg = oneHTML_X[i]
            true_Y = oneHTML_Y[i]
            #   Reshape for one input
            reshapedSeg = seg.reshape(1,-1)
            #   Predict on one segment
            pred_Y = loaded_model.predict(reshapedSeg)

            #   post processing:
            #for body:
            if i == 0:
                pred_Y[0][0] = pred_Y[0][2] = pred_Y[0][-2] = pred_Y[0][-1] = 0
            #for header and footer:
            elif i ==1 or i == 5:
                pred_Y[0][1] = pred_Y[0][2] = pred_Y[0][3] = pred_Y[0][5] = pred_Y[0][6] = 0
            else:
                pred_Y[0][1] = pred_Y[0][3] = pred_Y[0][4] = pred_Y[0][5] = 0
            pred_VectorHTML.append(pred_Y)


        pred_VectorHTML = np.squeeze(np.array(pred_VectorHTML))

        pred_norm_VectorHTML = denormalizeVectorHTML(pred_VectorHTML, ranges)
        for i in range(1,6):
            #put back color
            #segment_colors comes in order bgr that's why we access differently
            r = int(segment_colors[i][2])
            g = int(segment_colors[i][1])
            b = int(segment_colors[i][0])
            pred_norm_VectorHTML[i][0] = r*256**2 + g*256 + b + 1
            #put back order
            if i >= 2 and i <= 4:
                pred_norm_VectorHTML[i][-2] = i-1
            
        html = convertToHTML(pred_norm_VectorHTML, ranges)
        page = TESTPATH+'/page' + str(1) + 'PREDICTED.html'
        f = open(page,"w")
        f.write(html)
        f.close()

            

if __name__ == '__main__':
    #create necessary folders
    if not os.path.exists(TESTPATH):
        os.makedirs(TESTPATH)
    main()
