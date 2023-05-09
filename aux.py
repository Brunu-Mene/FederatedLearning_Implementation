from imutils import paths
import numpy as np
import os
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D,Flatten,Dense
from tensorflow.keras.optimizers import SGD

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

def define_model(input_shape,num_classes):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=input_shape))
    model.add(MaxPool2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(num_classes, activation='softmax'))
    # compile model
    opt = SGD(learning_rate=0.01, momentum=0.9)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model