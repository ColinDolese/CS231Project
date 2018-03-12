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

DATASAMPLES_TEST = 100
DATASAMPLES_TRAIN = 100

GENERATE_NEW_TEST = False

def formatVectorHTML(vectorHTMLEntry):
    vecCopy = np.copy(vectorHTMLEntry)
    # set "background" attribute to 0
    vecCopy[0] = 0
    # set "order" attribute to 0
    vecCopy[7] = 0
    return normalize(vecCopy.reshape(-1,1), axis=0, norm='l1').flatten()

     

def createData(numSamples, training = True):
    xSamples = []
    ySamples = []
    print "about to get HTML pages"
    _, vectorHTMLs, pageNames = getHTMLPages(numSamples, training, TRAINPATH, TESTPATH)

    print "finished getting HTML pages"
    print "start segmenting"
    i = 0
    for img in pageNames:
        real_segments = k_cluster(img) # unflattened segments
        segments = []
        for segment in real_segments:
            segments.append(segment.flatten())

##        #1. Turn the whole image black and white (test out if this makes sense
##        #for vector0 (body)
##        img_gray = cv2.imread(img, 0)
##        img_gray = cv2.resize(img_gray,(0,0), fx=0.5, fy=0.5)
##        (thresh, img_bw) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        
        #   Gridify? TODO: maybe
        
        #2. Match vectorHTMLs with segments
        #   Currently assuming that vec 2-4 are in random order
        xSamples.append(np.array(segments[0]))
        xSamples.append(np.array(segments[1]))

##        xEntry = [segments[0], segments[1]]
        ySamples.append(np.array(formatVectorHTML(vectorHTMLs[i][0])))
        ySamples.append(np.array(formatVectorHTML(vectorHTMLs[i][1])))
##        yEntry = [formatVectorHTML(vectorHTMLs[i][0]), formatVectorHTML(vectorHTMLs[i][1])]
        #go over middle vectors that are in random order
        addedVectors = 0
        while addedVectors < 3:
            for vec in vectorHTMLs[i][2:-1]:
                if vec[-2] == addedVectors + 1:
                    ySamples.append(np.array(formatVectorHTML(vec)))
##                    yEntry.append(formatVectorHTML(vec))
                    #-2 index is "order" according to generateVectorHTML
                    xSamples.append(np.array(segments[vec[-2]+1]))
##                    xEntry.append(segments[vec[-2]+1])
                    addedVectors += 1
            
        xSamples.append(np.array(segments[-1]))
        ySamples.append(np.array(formatVectorHTML(vectorHTMLs[i][-1])))
##        xEntry.append(segments[-1])
##        yEntry.append(formatVectorHTML(vectorHTMLs[i][-1]))

        #3. convert to numpy arrays
##        xEntry = np.array(xEntry)
##        yEntry = np.array(yEntry)

      

        #4. Add to xSamples and ySamples
##        xSamples.append(xEntry)
##        ySamples.append(yEntry)
##        print xEntry.shape, yEntry.shape
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
    np.save(TESTPATH+"/y_Test.dat", Y_test)
  
    filepath = FOLDERNAME+"/weights.{epoch:02d}.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose =1, save_best_only=True, mode='auto', period = 10)
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
