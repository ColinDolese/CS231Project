import os
from learnToGenerateHTML import *

def generate_outputs(nn, x_test,y_test):
    for i in range(2):
        test = x_test[i].reshape(1,-1)
        prediction = nn.predict(test)
        print prediction
        print y_test[i]

def main():
    #set filename(for model) manually
    filename =
   
    print(filename)
  
    model.load_weights(filename)
    generate_outputs(model, x_test,y_test)
##    lst = sorted(os.listdir("experiment_models")[1:], key=lambda x:int(x.split('.')[1]))
##    #   Need to get x_test, y_test still and also set the folder
##    for filename in lst:
##        if filename.endswith(".hdf5"):
##            print(filename)
##            model = larger_model()
##            model.load_weights("experiment_models/%s" % filename)
##            generate_outputs(nn, x_test,y_test, filename, iteration = 0)
