import os
import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from matplotlib import pyplot as plt


def extract_all_clusters(center, flat_label, img_small):
    original_flat_label = flat_label
    original_center = center.copy()
    segments = []
    
    res = center[flat_label]
    
    original_image = res.reshape((img_small.shape))
    #get correct ordering from x to y
    ordering = []
    previous_label = -1
    label_index = 0
    labelToAdd = -1
    closestToWhite = []
    closestToWhiteDist = 255
    for c in center:
        dist = np.linalg.norm([255,255,255]-c)
        if dist < closestToWhiteDist:
            closestToWhite = [int (x) for x in c]

            closestToWhiteDist = dist
    for label in flat_label:
        if label != previous_label and label not in ordering and label != labelToAdd:
            upcoming_center_color = center[label]
            #if the colors are close enough - epsilon 5
            if np.linalg.norm(res[label_index]-upcoming_center_color) == 0:
                if np.linalg.norm(closestToWhite-upcoming_center_color) > 10:    #if not all white
                    ordering.append(label)
                else:
                    labelToAdd = label
                previous_label = label
        label_index += 1
    
    #reorder ordering to have body as the first element and set color ordering
    ordering.insert(0,labelToAdd)
    center_colors_ordered = []
    for centerColorLabel in ordering:
        center_colors_ordered.append(center[centerColorLabel].copy())
        
    # Something went wrong
    if len(ordering) < 6:
        print "couldn't find 6 clusters that are different from one another"
        return [], [], []
    for i in range(len(ordering)):
        #   Set every other cluster to one other cluster
        otherI = 0
        if i == 0:
            otherI = 1
        flat_label = np.where(flat_label < i, otherI, flat_label)
        flat_label = np.where(flat_label > i, otherI, flat_label)
        #   Set all clusters to be black-white depending on their belonging
        #if body set it to be some other color, else set it to black
        centerComparison = [int(x) for x in center[i]]
        centerDistance = np.array(closestToWhite)-np.array(centerComparison)
        if np.linalg.norm(centerDistance) == 0:    #if all white
            center[i] = [127, 127, 127]
        else:
            center[i]= [0,0,0]
        center[otherI] = [255,255,255]
        res = center[flat_label]
        res2 = res.reshape((img_small.shape))
        segments.append(res2)
        flat_label = original_flat_label
        center = original_center

    #plot
##    plt.subplot(331), plt.imshow(img_small), plt.title("Original")
##    pltNumber = 331
##    for i in range(len(ordering)):
##        pltNumber += 1
##        plt.subplot(pltNumber), plt.imshow(segments[ordering[i]]), plt.title("segment " + str(i))
##    plt.show()
##    
    
    return segments, ordering, center_colors_ordered


#input: img_path - 'page1.png'
#output: output - ordered list of segments
#       ordered_colors - use in testing to get real test colors
def k_cluster(img_path):
    img = cv2.imread(img_path)
    img_small = cv2.resize(img,(200,200))

    Z = img_small.reshape((img_small.shape[0]*img_small.shape[1],3))
    clt = MiniBatchKMeans(n_clusters=6)
    flat_label = clt.fit_predict(Z)
    center = clt.cluster_centers_.astype("uint8")
   
    segments, ordering, ordered_colors = extract_all_clusters(center, flat_label, img_small)
    output = []
    for i in range(len(ordering)):
        output.append(segments[ordering[i]])
    return output, ordered_colors    

##segments, ordered_colors = k_cluster('test_data/2018_03_18-1114/page1.png')


