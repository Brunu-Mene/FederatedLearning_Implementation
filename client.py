import aux
import sys
from sklearn.model_selection import train_test_split



if __name__ == '__main__':
    cid = -1

    try:
        cid = sys.argv[1]
    except IOError:
        print("Missing argument! Client Id...")
        exit()

    image_list, label_list = aux.load_mnist_byCid(cid)
    x_train, x_test, y_train, y_test = train_test_split(image_list, label_list, test_size=0.2, random_state=42)


    