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

    def _callClientLearning(self, client_ip):
        channel = grpc.insecure_channel(client_ip)
        client = fed_grpc_pb2_grpc.FederatedServiceStub(channel)

        returns = client.startLearning(fed_grpc_pb2.void())
        learning_weight = returns.learningWeight
        sample_size = returns.sampleSize
    
        print(learning_weight)
        # q.put([learning_weight, sample_size])

    def __callModelValidation(self, client_ip, aggregated_weights):
        channel = grpc.insecure_channel(client_ip)

        client = fed_grpc_pb2_grpc.FederatedServiceServicer(channel)
        acc = client.modelValidation(fed_grpc_pb2.aggregationWeight(weight = (aggregated_weights))).acc

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

            ip = self.clients[cid_targets[0]]
            self._callClientLearning(str(ip))
            # thread_list = []
            # for i in range(n_round_clients):
            #     thread = threading.Thread(target=self.__callClientLearning, args=(self.clients[cid_targets[i]], q))
            #     thread_list.append(thread)
            #     thread.start()
            # for thread in thread_list:
            #     thread.join()

            # weights_clients_list = []
            # sample_size_list = []
            # while not q.empty():
            #     thread_results = q.get()

            #     weights_clients_list.append(thread_results[0])
            #     sample_size_list.append(thread_results[1])

            # print(weights_clients_list)
            # print(weights_clients_list[1][:5])


            # aggregated_weights = self.__FedAvg(n_round_clients, weights_clients_list, sample_size)
            # thread_list = []
            # for i in range(n_round_clients):
            #     thread = threading.Thread(target=self.__callModelValidation, args=(self.clients[cid_targets[i]],aggregated_weights, ))
            #     thread_list.append(thread)
            #     thread.start()
            
            # acc_list = []
            # for thread in thread_list:
            #     thread.join()
            #     acc_list.append(thread.result)

            self.round += 1
            # acc_mean = sum(acc_list)/len(acc_list)
            # print(f"Round: {self.round} / Accuracy Mean: {acc_mean}")
            # if acc_mean >= acc_target:
            #     print("Accuracy Target as been Achieved! Ending process")
            #     break

if __name__ == "__main__":
    fed_server = FedServer()

    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fed_grpc_pb2_grpc.add_FederatedServiceServicer_to_server(fed_server, grpc_server)

    grpc_server.add_insecure_port('[::]:8080')
    grpc_server.start()
    fed_server.startServer(2,2,1,0.80,10)