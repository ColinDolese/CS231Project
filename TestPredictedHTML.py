import os
import pickle
import numpy as np
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import GradientBoostingRegressor
from learnToGenerateHTML import *

#0 - neural network
#1 - SVM
TEST_MODEL = 1
DATETIME = '2018_03_16-1244'
FILENAME = "experiment_models/"+DATETIME+'/svmModel.sav'

dateTimeNow = str(datetime.now().strftime("%Y_%m_%d-%H%M"))
TESTPATH ="test_data/"+dateTimeNow
TRAINPATH = "train_data/"+dateTimeNow

def main():
    #set filename(for model) manually
    if TEST_MODEL == 1:
        X_test, Y_test, segment_colors = createData(1, False)
        loaded_model = pickle.load(open(FILENAME, 'rb'))
        score = loaded_model.score(X_test, Y_test)
        print "Score of the model on the test: "
        print score
        #   example for test prediction output:
        #get first 6 segments from test:
        oneHTML_X = X_test[0:6]
        oneHTML_Y = Y_test[0:6]
        for i in range(len(oneHTML_X)):
            seg = oneHTML_X[i]
            true_Y = oneHTML_Y[i]
            reshapedSeg = seg.reshape(1,-1)
            pred_Y = loaded_model.predict(reshapedSeg)
            #   TODO: DENORMALIZE SO WE CAN COMPARE!!!!!
            #See how we access the color and order
            print "PREDICT: "
            print pred_Y
            print "Center color: "
            print segment_colors[i]
            print "Order (only 1-3 matter): "
            print i-1
            print "Actual: "
            print true_Y
            

if __name__ == '__main__':
    #create necessary folders
    if not os.path.exists(TRAINPATH):
        os.makedirs(TRAINPATH)
    if not os.path.exists(TESTPATH):
        os.makedirs(TESTPATH)
    main()
