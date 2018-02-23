import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

#based on https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans/py_kmeans_opencv/py_kmeans_opencv.html#color-quantization


def extract_all_clusters(center, flat_label, img_small):
    original_flat_label = flat_label
    original_center = center.copy()
    segments = []
    for i in range(5):
##        print center
##        print i
##        print list(set(flat_label))
        #   Set every other cluster to one other cluster
        otherI = 0
        if i == 0:
            otherI = 1
        flat_label = np.where(flat_label < i, otherI, flat_label)
        flat_label = np.where(flat_label > i, otherI, flat_label)
        #   Set that other cluster to be white
        center[otherI] = [255,255,255]
        res = center[flat_label]
        res2 = res.reshape((img_small.shape))
        segments.append(res2)
##        cv2.imshow('res2',res2)
##        cv2.waitKey(0)
##        cv2.destroyAllWindows()
        flat_label = original_flat_label
        center = original_center

    #plot
    plt.subplot(231), plt.imshow(img_small), plt.title("Original")
    plt.subplot(232), plt.imshow(segments[0]), plt.title("segment 1")
    plt.subplot(233), plt.imshow(segments[1]), plt.title("segment 2")
    plt.subplot(234), plt.imshow(segments[2]), plt.title("segment 3")
    plt.subplot(235), plt.imshow(segments[3]), plt.title("segment 4")
    plt.subplot(236), plt.imshow(segments[4]), plt.title("segment 5")
    plt.show()


def k_cluster(img_path):
    img = cv2.imread(img_path)
    img_small = cv2.resize(img,(0,0), fx=0.5, fy=0.5)

    Z = img_small.reshape((-1,3))
    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS, 10, 10e-6)
    K = 5
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    flat_label = label.flatten()

    extract_all_clusters(center, flat_label, img_small)
                

k_cluster('page1.png')
k_cluster('page2.png')
k_cluster('page3.png')
