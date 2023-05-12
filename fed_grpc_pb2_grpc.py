# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import fed_grpc_pb2 as fed__grpc__pb2


class FederatedServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.clientRegister = channel.unary_unary(
                '/main.FederatedService/clientRegister',
                request_serializer=fed__grpc__pb2.registerArgs.SerializeToString,
                response_deserializer=fed__grpc__pb2.registerOut.FromString,
                )
        self.startLearning = channel.unary_unary(
                '/main.FederatedService/startLearning',
                request_serializer=fed__grpc__pb2.void.SerializeToString,
                response_deserializer=fed__grpc__pb2.weightList.FromString,
                )
        self.getSampleSize = channel.unary_unary(
                '/main.FederatedService/getSampleSize',
                request_serializer=fed__grpc__pb2.void.SerializeToString,
                response_deserializer=fed__grpc__pb2.sampleSize.FromString,
                )
        self.modelValidation = channel.unary_unary(
                '/main.FederatedService/modelValidation',
                request_serializer=fed__grpc__pb2.weightList.SerializeToString,
                response_deserializer=fed__grpc__pb2.accuracy.FromString,
                )
        self.popClient = channel.unary_unary(
                '/main.FederatedService/popClient',
                request_serializer=fed__grpc__pb2.void.SerializeToString,
                response_deserializer=fed__grpc__pb2.sinal.FromString,
                )
        self.killClient = channel.unary_unary(
                '/main.FederatedService/killClient',
                request_serializer=fed__grpc__pb2.void.SerializeToString,
                response_deserializer=fed__grpc__pb2.void.FromString,
                )


class FederatedServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def clientRegister(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def startLearning(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getSampleSize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def modelValidation(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def popClient(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def killClient(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FederatedServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'clientRegister': grpc.unary_unary_rpc_method_handler(
                    servicer.clientRegister,
                    request_deserializer=fed__grpc__pb2.registerArgs.FromString,
                    response_serializer=fed__grpc__pb2.registerOut.SerializeToString,
            ),
            'startLearning': grpc.unary_unary_rpc_method_handler(
                    servicer.startLearning,
                    request_deserializer=fed__grpc__pb2.void.FromString,
                    response_serializer=fed__grpc__pb2.weightList.SerializeToString,
            ),
            'getSampleSize': grpc.unary_unary_rpc_method_handler(
                    servicer.getSampleSize,
                    request_deserializer=fed__grpc__pb2.void.FromString,
                    response_serializer=fed__grpc__pb2.sampleSize.SerializeToString,
            ),
            'modelValidation': grpc.unary_unary_rpc_method_handler(
                    servicer.modelValidation,
                    request_deserializer=fed__grpc__pb2.weightList.FromString,
                    response_serializer=fed__grpc__pb2.accuracy.SerializeToString,
            ),
            'popClient': grpc.unary_unary_rpc_method_handler(
                    servicer.popClient,
                    request_deserializer=fed__grpc__pb2.void.FromString,
                    response_serializer=fed__grpc__pb2.sinal.SerializeToString,
            ),
            'killClient': grpc.unary_unary_rpc_method_handler(
                    servicer.killClient,
                    request_deserializer=fed__grpc__pb2.void.FromString,
                    response_serializer=fed__grpc__pb2.void.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'main.FederatedService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FederatedService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def clientRegister(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/main.FederatedService/clientRegister',
            fed__grpc__pb2.registerArgs.SerializeToString,
            fed__grpc__pb2.registerOut.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def startLearning(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/main.FederatedService/startLearning',
            fed__grpc__pb2.void.SerializeToString,
            fed__grpc__pb2.weightList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getSampleSize(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/main.FederatedService/getSampleSize',
            fed__grpc__pb2.void.SerializeToString,
            fed__grpc__pb2.sampleSize.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def modelValidation(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/main.FederatedService/modelValidation',
            fed__grpc__pb2.weightList.SerializeToString,
            fed__grpc__pb2.accuracy.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def popClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/main.FederatedService/popClient',
            fed__grpc__pb2.void.SerializeToString,
            fed__grpc__pb2.sinal.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def killClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/main.FederatedService/killClient',
            fed__grpc__pb2.void.SerializeToString,
            fed__grpc__pb2.void.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
