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

#If the folders before datetime.now don't exist then create them manually. otherwise might encounter errors
#Might not have to do that, but if you get errors, then you know wazzupp
dateTimeNow = str(datetime.now().strftime("%Y_%m_%d-%H%M"))
FOLDERNAME = "experiment_models/"+dateTimeNow
TESTPATH ="test_data/"+dateTimeNow
TRAINPATH = "train_data/"+dateTimeNow

DATASAMPLES_TEST = 5
DATASAMPLES_TRAIN = 100

GENERATE_NEW_TEST = False


def formatVectorHTML(vectorHTML, ranges):
    vecCopy = np.copy(vectorHTML).astype(float)
    print(vecCopy)
    for i in range(vecCopy.shape[0]):
        vecCopy[i][0] = 0
        for j, attr in enumerate(sorted(ranges.iterkeys())):
                vecCopy[i][j] /= (len(ranges[attr])-1)
    
    return vecCopy
     

def createData(numSamples, training = True):
    xSamples = []
    ySamples = []
    print "about to get HTML pages"
    _, vectorHTMLs, pageNames, ranges = getHTMLPages(numSamples, training, TRAINPATH, TESTPATH)

    print "finished getting HTML pages"
    print "start segmenting"
    i = 0
    for img in pageNames:
        real_segments, _ = k_cluster(img) # unflattened segments
        if len(real_segments) < 6:
            print "clustering returned junk"
            i += 1
            continue
        segments = []
        for segment in real_segments:
            #gridify:
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
        #go over middle vectors that are in random order
        addedVectors = 0
        while addedVectors < 3:
            for vec in normVecHTML[2:-1]:
                if vec[-2] == addedVectors + 1:
                	vec[6] = 0
                    ySamples.append(np.array(vec))
                    #-2 index is "order" according to generateVectorHTML
                    xSamples.append(np.array(segments[vec[-2]+1]))
                    addedVectors += 1
            
        xSamples.append(np.array(segments[-1]))
        ySamples.append(np.array(normVecHTML[-1]))
        print ("segment " + str(i) + " done")

        i += 1
        
    print "all done with creating data"
    #   convert to numpy arrays
    xSamples = np.array(xSamples)
    ySamples = np.array(ySamples)
    print xSamples.shape, ySamples.shape
    return xSamples, ySamples
                                    
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
    X_test, Y_test = createData(DATASAMPLES_TEST, False)

    np.save(TESTPATH+"/x_Test.npy", X_test)
    np.save(TESTPATH+"/y_Test.npy", Y_test)
  
    filepath = FOLDERNAME+"/weights.{epoch:02d}.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose =1, save_best_only=True, mode='auto', period = 1)
    callbacks_list = [checkpoint]
    NUM_EPOCHS = 10
    epochCount = 0
    
    #   run forever basically
    for i in range(100000000):
        X_train, Y_train = createData(DATASAMPLES_TRAIN)
        model = larger_model(X_train[0], Y_train[0])

        history = model.fit(X_train,Y_train,validation_split=0.1, epochs = NUM_EPOCHS, batch_size = 10,
                  callbacks=callbacks_list, verbose = 0, initial_epoch = epochCount)
        epochCount +=NUM_EPOCHS
##        pyplot.plot(history.history['mean_squared_error'])
##        pyplot.show()
    return

if __name__ == '__main__':
    main()
