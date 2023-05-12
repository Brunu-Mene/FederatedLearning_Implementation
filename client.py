import aux
import sys
import grpc
import fed_grpc_pb2_grpc
import fed_grpc_pb2
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import random
import numpy as np
from concurrent import futures


class FedClient(fed_grpc_pb2_grpc.FederatedServiceServicer):
    def __init__(self, cid, x_train, x_test, y_train, y_test, model, server_adress):
        self.cid = cid
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.model = model
        self.server_adress = server_adress

    def startLearning(self, request, context):
        self.model.fit(x_train, y_train, epochs=1, verbose=2)

        weights_list = aux.setWeightSingleList(self.model.get_weights())

        return fed_grpc_pb2.weightList(weight = (weights_list))
    
    def getSampleSize(self, request, context):
        return fed_grpc_pb2.sampleSize(size = (len(self.x_train)))

    def modelValidation(self, request, context):
        server_weight = request.weight
        self.model.set_weights(aux.reshapeWeight(server_weight, self.model.get_weights()))
        accuracy = self.model.evaluate(self.x_test, self.y_test, verbose=0)[1]

        print(f"Local accuracy with global weights: {accuracy}")

        return fed_grpc_pb2.accuracy(acc = (accuracy))
    
    def runClient(self):
        channel = grpc.insecure_channel(server_adress)
        client = fed_grpc_pb2_grpc.FederatedServiceStub(channel)

        port = server_adress.split(':')[1]
        port = port[:len(port)-1] + str(int(cid)+1)

        register_out = client.clientRegister(fed_grpc_pb2.registerArgs(ip='[::]:', port=port, cid=self.cid))
        print(register_out.connectedClient)
        print(register_out.round)



        grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        fed_grpc_pb2_grpc.add_FederatedServiceServicer_to_server(self, grpc_server)

        client_ip = "[::]:"+port
        grpc_server.add_insecure_port(client_ip)
        grpc_server.start()
        grpc_server.wait_for_termination()


if __name__ == '__main__':
    cid = -1
    input_shape = (28, 28, 1)
    num_classes = 10
    server_adress = 'localhost:8080'

    try:
        cid = sys.argv[1]
    except IOError:
        print("Missing argument! You need to pass: Client ServerAdress...")
        exit()

    x_train, y_train = aux.load_mnist_byCid(cid)
    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

    # one-hot encode the labels
    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)

    model = aux.define_model(input_shape,num_classes)

    fed_client = FedClient(cid, x_train, x_test, y_train, y_test, model, server_adress)
    fed_client.runClient()
