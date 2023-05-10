import grpc
import fed_grpc_pb2
import fed_grpc_pb2_grpc



class FedServer(fed_grpc_pb2_grpc.FederatedServiceServicer):
    def __init__(self):
        self.clients = {}
        self.round = 0


    def clientRegister(self, request, context):
        ip = request.ip
        port = request.port
        cid = request.cid
        
        if cid in self.clients:
            return fed_grpc_pb2.registerOut(connectedClient = (False), round = (self.round))
        
        self.clients[cid] = ip+port
        return fed_grpc_pb2.registerOut(connectedClient = (True), round = (self.round))




if __name__ == "__main__":
    fedServer = FedServer()