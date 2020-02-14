from typing import Type, cast

import zmq

from .message import (Block, BlockHash, GetBlock, GetBlockHash, GetState,
                      GetTip, Message, State, Tip)


class Monitor:
    def __init__(self, host: str, port: int):
        self.__connection_string = f"tcp://{host}:{port}"
        self.__context = zmq.Context()
        self.__request = self.__context.socket(zmq.REQ)
        self.__request.connect(self.__connection_string)

    def get_tip(self) -> Tip:
        self._send_message(GetTip())
        return cast(Tip, self._receive_message())

    def get_state(self, address: bytes, block_hash: bytes = None) -> State:
        if block_hash is None:
            block_hash = self.get_tip().block_hash
        self._send_message(GetState(block_hash, address))
        return cast(State, self._receive_message())

    def get_block(self, block_hash: bytes) -> Block:
        self._send_message(GetBlock(block_hash))
        return cast(Block, self._receive_message())

    def get_block_hash(self, block_index: int) -> BlockHash:
        self._send_message(GetBlockHash(block_index))
        return cast(BlockHash, self._receive_message())

    def _send_message(self, message: Message):
        message.as_multipart()
        self.__request.send_multipart(message.as_multipart())

    def _receive_message(self) -> Type[Message]:
        raw = self.__request.recv_multipart()
        return Message.parse(raw)
