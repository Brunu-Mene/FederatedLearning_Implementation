import aux
import sys
import grpc
import fed_grpc_pb2_grpc
import fed_grpc_pb2
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical


class FedClient(fed_grpc_pb2_grpc.FederatedServiceServicer):
    def __init__(self, x_train, x_test, y_train, y_test, model, server_adress):
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.model = model
        self.server_adress = server_adress

    def startLearning(self, request, context):
        self.model.fit(x_train, y_train, epochs=1, verbose=2)

        return fed_grpc_pb2.learningResults(learningWeight = (aux.setWeightSingleList(self.model.get_weights())), sampleSize = (len(self.x_train)))


    # def modelValidation(self, request, context): 
    
    #     return (accuracy)

if __name__ == '__main__':
    cid = -1
    input_shape = (28, 28, 1)
    num_classes = 10

    try:
        cid = sys.argv[1]
    except IOError:
        print("Missing argument! Client Id...")
        exit()

    x_train, y_train = aux.load_mnist_byCid(cid)
    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)
    # one-hot encode the labels
    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)

    model = aux.define_model(input_shape,num_classes)
    model.fit(x_train, y_train, epochs=1, verbose=2)
