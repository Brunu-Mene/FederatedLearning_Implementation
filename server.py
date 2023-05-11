import grpc
import fed_grpc_pb2
import fed_grpc_pb2_grpc
import random
import threading
import numpy as np


class FedServer(fed_grpc_pb2_grpc.FederatedServiceServicer):
    def __init__(self):
        self.clients = {}
        self.round = 0

    def _callClientLearning(client_ip):
        channel = grpc.insecure_channel(client_ip)

        client = fed_grpc_pb2_grpc.FederatedServiceServicer(channel)
        learning_weight, sample_size = client.startLearning(fed_grpc_pb2.void()).result

        return learning_weight, sample_size

    def _FedAvg(n_clients, weights_clients_list, sample_size_list):
        total_sample = np.sum(sample_size_list)

        # Compute weighted average of the client weights
        aggregated_weights = np.zeros_like(weights_clients_list[0])
        for i in range(n_clients):
            aggregated_weights += (weights_clients_list[i] * sample_size_list[i])

        aggregated_weights /= total_sample
        
        return aggregated_weights

    def clientRegister(self, request, context):
        ip = request.ip
        port = request.port
        cid = request.cid
        
        if cid in self.clients:
            return fed_grpc_pb2.registerOut(connectedClient = (False), round = (self.round))
        
        self.clients[cid] = ip+port
        return fed_grpc_pb2.registerOut(connectedClient = (True), round = (self.round))
    
    def startServer(self, n_round_clients, min_clients, max_rounds, acc_target, timeout):
        acc_global = 0.0
        while self.round < max_rounds and acc_global < acc_target:
            if len(self.clients) < min_clients:
                print("Waiting for the minimun number of clients to connect...")
                while len(self.clients) < min_clients:
                    continue

                print("The minimum number of clients has been reached, starting learning...")

            cid_targets = []
            clients = [w for w in range(len(self.clients))]

            while len(cid_targets) < n_round_clients:
                tr = random.choice(clients)
                cid_targets.append(tr)
                clients.remove(tr)

            thread_list = []
            for i in range(0,len(cid_targets)):
                thread = threading.Thread(target=self._callClientLearning, args=(self.clients[cid_targets[i]],))
                thread_list.append(thread)
                thread.start()

            weights_clients_list = []
            sample_size_list = []
            for thread in thread_list:
                thread.join()
                weight, sample_size = thread.result
                weights_clients_list.append(weight)
                sample_size_list.append(sample_size)

if __name__ == "__main__":
    fed_server = FedServer()