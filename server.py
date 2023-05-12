import grpc
import fed_grpc_pb2
import fed_grpc_pb2_grpc
import random
import threading
import statistics
import numpy as np
from concurrent import futures
import queue


class FedServer(fed_grpc_pb2_grpc.FederatedServiceServicer):
    def __init__(self):
        self.clients = {}
        self.round = 0

    def __callClientLearning(self, client_ip, q):
        channel = grpc.insecure_channel(client_ip)
        client = fed_grpc_pb2_grpc.FederatedServiceStub(channel)

        weight_list = client.startLearning(fed_grpc_pb2.void()).weight
        sample_size = client.getSampleSize(fed_grpc_pb2.void()).size

        q.put([weight_list, sample_size])

    def __callModelValidation(self, client_ip, aggregated_weights):
        channel = grpc.insecure_channel(client_ip)

        client = fed_grpc_pb2_grpc.FederatedServiceStub(channel)
        acc = client.modelValidation(fed_grpc_pb2.weightList(weight = (aggregated_weights))).acc

        return acc

    def __FedAvg(self, n_clients, weights_clients_list, sample_size_list):
        aggregated_weights = []
        for j in range(len(weights_clients_list[0])):
            element = 0.0
            for i in range(n_clients):
                element += weights_clients_list[i][j]
            aggregated_weights.append(element/n_clients)  
        
        return aggregated_weights
    
    def __printClientList(self):
        print(self.clients[0])
        print(self.clients[1])

    def clientRegister(self, request, context):
        ip = request.ip
        port = request.port
        cid = int(request.cid)

        if cid in self.clients:
            print(f"Cound'not regist Client with ID {cid} - Duplicated Id")
            return fed_grpc_pb2.registerOut(connectedClient = (False), round = (self.round))
        
        self.clients[cid] = ip+port
        print(f"Client {cid} registed!")
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
            q = queue.Queue()
            for i in range(n_round_clients):
                thread = threading.Thread(target=self.__callClientLearning, args=(self.clients[cid_targets[i]], q))
                thread_list.append(thread)
                thread.start()
            for thread in thread_list:
                thread.join()

            weights_clients_list = []
            sample_size_list = []
            while not q.empty():
                thread_results = q.get()

                weights_clients_list.append(thread_results[0])
                sample_size_list.append(thread_results[1])
    

            aggregated_weights = self.__FedAvg(n_round_clients, weights_clients_list, sample_size_list)
            acc_list = []
            for i in range(n_round_clients):
                acc_list.append(self.__callModelValidation(self.clients[cid_targets[i]], aggregated_weights))
    
            self.round += 1
            acc_mean = sum(acc_list)/len(acc_list)
            print(f"Round: {self.round} / Accuracy Mean: {acc_mean}")
            if acc_mean >= acc_target:
                print("Accuracy Target as been Achieved! Ending process")
                break

if __name__ == "__main__":
    fed_server = FedServer()

    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fed_grpc_pb2_grpc.add_FederatedServiceServicer_to_server(fed_server, grpc_server)

    grpc_server.add_insecure_port('[::]:8080')
    grpc_server.start()
    fed_server.startServer(2,2,5,1.0,10)