from imutils import paths
import numpy as np
import os
import cv2

def load_mnist_byCid(cid):
    data = []
    labels = []

    path = f"mnist_data/client_{cid}"
    img_paths = list(paths.list_images(path))

    for (i, imgpath) in enumerate(img_paths):
        # load the image and extract the class labels
        img_grayscale = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)

        #reshape in 1D array
        img = np.array(img_grayscale).flatten()

        #get label from img name based on the folder
        label = imgpath.split(os.path.sep)[-2]

        # normalizing img 
        data.append(img/255.0)
        labels.append(label)

    return data, labels

