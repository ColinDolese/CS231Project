from GenerateDataSet import *
from KClusterBasedOnColor import *
from sklearn.preprocessing import normalize
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint
from keras.wrappers.scikit_learn import KerasRegressor
from keras.models import load_model
from matplotlib import pyplot
import pickle
import os
from datetime import datetime
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import GradientBoostingRegressor

#   SET MODEL HERE
# ------------------
#0 - keras neural network
#1 - SVM
LEARNING_MODEL = 1 

#If the folders before datetime.now don't exist then create them manually. otherwise might encounter errors
#Might not have to do that, but if you get errors, then you know wazzupp
dateTimeNow = str(datetime.now().strftime("%Y_%m_%d-%H%M"))
FOLDERNAME = "experiment_models/"+dateTimeNow
TESTPATH ="test_data/"+dateTimeNow
TRAINPATH = "train_data/"+dateTimeNow

DATASAMPLES_TEST = 50
DATASAMPLES_TRAIN = 500

GENERATE_NEW_TEST = False




def formatVectorHTML(vectorHTML, ranges):
    vecCopy = np.copy(vectorHTML).astype(float)
##    print(vecCopy)
    for i in range(vecCopy.shape[0]):
        vecCopy[i][0] = 0
        vecCopy[i][6] = 0
        for j, attr in enumerate(sorted(ranges.iterkeys())):
                vecCopy[i][j] /= (len(ranges[attr])-1)
    
    return vecCopy
     

def createData(numSamples, training = True):
    xSamples = []
    ySamples = []
    sampleColors = []
    print "about to get HTML pages"
    _, vectorHTMLs, pageNames, ranges = getHTMLPages(numSamples, training, TRAINPATH, TESTPATH)

    print "finished getting HTML pages"
    print "start segmenting"
    i = 0
    for img in pageNames:
        real_segments, ordered_center_colors = k_cluster(img) # unflattened segments
        if len(real_segments) < 6:
            print "clustering returned junk"
            i += 1
            continue

        #1. Gridify
        segments = []
        for segment in real_segments:
            OneDSegment = []
            flatSegment = segment.flatten()
            for seg_i in range(0,len(segment.flatten()), 3):
                #white
                if flatSegment[seg_i] == 255:
                    OneDSegment.append(1)
                #black
                elif flatSegment[seg_i] == 0:
                    OneDSegment.append(0)
                #gray
                elif flatSegment[seg_i] == 127:
                    OneDSegment.append(2)
            segments.append(OneDSegment)

        
        #2. Match vectorHTMLs with segments
        #   Currently assuming that vec 2-4 are in random order

        normVecHTML = formatVectorHTML(vectorHTMLs[i], ranges)

        xSamples.append(np.array(segments[0]))
        xSamples.append(np.array(segments[1]))

        ySamples.append(np.array(normVecHTML[0]))
        ySamples.append(np.array(normVecHTML[1]))

        sampleColors.append(ordered_center_colors[0])
        sampleColors.append(ordered_center_colors[1])
        #go over middle vectors that are in random order
        addedVectors = 0
        while addedVectors < 3:
            for vectorHTMLIndex in range(2,5):#vectorHTMLs[2:-1]:
                vec = vectorHTMLs[i][vectorHTMLIndex]
                normVec = normVecHTML[vectorHTMLIndex]
##                print vec
                if int(vec[-2]) == addedVectors + 1:
                    #-2 index is "order" according to generateVectorHTML
                    xSamples.append(np.array(segments[int(vec[-2]+1)]))
                    
                    ySamples.append(np.array(normVec))
                    
                    sampleColors.append(ordered_center_colors[int(vec[-2]+1)])
                    addedVectors += 1
            
        xSamples.append(np.array(segments[-1]))
        ySamples.append(np.array(normVecHTML[-1]))
        sampleColors.append(ordered_center_colors[-1])
        print ("segment " + str(i) + " done")

        i += 1
        
    print "all done with creating data"
    #   convert to numpy arrays
    xSamples = np.array(xSamples)
    ySamples = np.array(ySamples)
    sampleColors = np.array(sampleColors)
    print xSamples.shape, ySamples.shape, sampleColors.shape
    return xSamples, ySamples, sampleColors
                                    
def larger_model(sample_input, sample_output):
    model = Sequential()
    model.add(Dense(input_dim=len(sample_input), units=60, kernel_initializer='random_normal',activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(units=1000, kernel_initializer='random_normal',activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(units=100, kernel_initializer='random_normal',activation='relu'))
    model.add(Dense(units=len(sample_output), kernel_initializer='random_normal'))
    model.compile(loss='mse', optimizer='adam', metrics=['mse'])
    return model
                                                     

def main():
    #create necessary folders
    if not os.path.exists(FOLDERNAME):
        os.makedirs(FOLDERNAME)
    if not os.path.exists(TRAINPATH):
        os.makedirs(TRAINPATH)
    if not os.path.exists(TESTPATH):
        os.makedirs(TESTPATH)

    #   Unnecessary right now. just set to false. This is to create test data, but we do it in test
    if GENERATE_NEW_TEST:
        print "Generating test data" 

        X_test, Y_test, _ = createData(DATASAMPLES_TEST, False)

        np.save(TESTPATH+"/x_Test.npy", X_test)
        np.save(TESTPATH+"/y_Test.npy", Y_test)
        print "Done with test data"
  


    #   Get train data
    print "Generating train data"
    X_train, Y_train, _ = createData(DATASAMPLES_TRAIN)
    print "Done with train data"

    #Not working
    if LEARNING_MODEL == 0:
        filepath = FOLDERNAME+"/weightsBest.hdf5"
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose =1, save_best_only=True, mode='auto', period = 1)
        callbacks_list = [checkpoint]
        NUM_EPOCHS = 100000
        epochCount = 0
        model = larger_model(X_train[0], Y_train[0])
        history = model.fit(X_train,Y_train,validation_split=0.1, epochs = NUM_EPOCHS, batch_size = 10,
                  callbacks=callbacks_list, verbose = 0, initial_epoch = epochCount)
                                      
        epochCount +=NUM_EPOCHS
##    pyplot.plot(history.history['mean_squared_error'])
##    pyplot.show()
    elif LEARNING_MODEL == 1:
        print "Start SVM learn"
        model = MultiOutputRegressor(GradientBoostingRegressor(random_state=0)).fit(X_train, Y_train)
        print "SVM learn done"
        print "Score on train: "
        print model.score(X_train, Y_train)
        print "Start saving model"
        dumpPath = FOLDERNAME+'/svmModel.sav'
        pickle.dump(model, open(dumpPath, 'wb'))
        print "Saved model to: " + dumpPath
    return

if __name__ == '__main__':
    main()
