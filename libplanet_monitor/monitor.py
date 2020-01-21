from typing import Type

import zmq

from libplanet_monitor.message import Tip, GetTip, Message, GetState, State


class Monitor:
    def __init__(self, host: str, port: int):
        self.__connection_string = f"tcp://{host}:{port}"
        self.__context = zmq.Context()
        self.__request = self.__context.socket(zmq.REQ)
        self.__request.connect(self.__connection_string)

    def get_tip(self) -> Tip:
        self._send_message(GetTip())
        return self._receive_message()

    def get_state(self, address: bytes) -> State:
        tip = self.get_tip()
        self._send_message(GetState(tip.block_hash, address))
        return self._receive_message()

    def _send_message(self, message: Type[Message]):
        message.as_multipart()
        self.__request.send_multipart(message.as_multipart())

    def _receive_message(self) -> Type[Message]:
        raw = self.__request.recv_multipart()
        return Message.parse(raw)
