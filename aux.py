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

def load_mnist_bypath(paths, verbose = -1):
    data = []
    labels = []

    for (i, imgpath) in enumerate(paths):
        # load the image and extract the class labels
        im_gray = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)
        image = np.array(im_gray).flatten()
        label = imgpath.split(os.path.sep)[-2]

        # aqui é feita a escala da img para [0, 1] para diminuir o impacto do brilho de cada pixel
        data.append(image/255)
        labels.append(label)
        # show an update every `verbose` images
        if verbose > 0 and i > 0 and (i + 1) % verbose == 0:
            print("[INFO] processed {}/{}".format(i + 1, len(paths)))
    # return a tuple of the data and labels
    return data, labels


def loadClientData(cid):      
    img_path = 'mnist_data/'
    image_paths = list(paths.list_images(img_path))

