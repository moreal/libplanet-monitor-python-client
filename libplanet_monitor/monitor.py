import zmq

from libplanet_monitor.message import Tip, GetTip, Message


class Monitor:
    def __init__(self, host: str, port: int):
        self.__connection_string = f"tcp://{host}:{port}"
        self.__context = zmq.Context()
        self.__request = self.__context.socket(zmq.REQ)
        self.__request.connect(self.__connection_string)

    def get_tip(self) -> Tip:
        request = GetTip()
        print(request.as_multipart())
        self.__request.send_multipart(request.as_multipart())
        raw = self.__request.recv_multipart()
        message = Message.parse(raw)
        return message
