from typing import Type, cast

import zmq

from typing import Tuple
from .message import *
from . import message, blockchain


class Monitor:
    def __init__(self, host: str, port: int):
        self.__connection_string = f"tcp://{host}:{port}"
        self.__context = zmq.Context()
        self.__request = self.__context.socket(zmq.REQ)
        self.__request.connect(self.__connection_string)

    def get_tip(self) -> Tuple[int, blockchain.Hash]:
        self._send_message(message.GetTip())
        reply: Tip = cast(Tip, self._receive_message())
        return reply.block_index, reply.block_hash

    def get_state(self, address: blockchain.Address, block_hash: blockchain.Hash = None) -> BValue:
        if block_hash is None:
            block_hash = self.get_tip()[1]
        self._send_message(message.GetState(block_hash, address))
        reply: State = cast(State, self._receive_message())
        return reply.state

    def get_block(self, block_hash: blockchain.Hash) -> blockchain.Block:
        self._send_message(message.GetBlock(block_hash))
        reply: Block = cast(Block, self._receive_message())
        return reply.block

    def get_block_hash(self, block_index: int) -> blockchain.Hash:
        self._send_message(message.GetBlockHash(block_index))
        reply: BlockHash = cast(BlockHash, self._receive_message())
        return reply.block_hash

    def _send_message(self, message: Message):
        message.as_multipart()
        self.__request.send_multipart(message.as_multipart())

    def _receive_message(self) -> Type[Message]:
        raw = self.__request.recv_multipart()
        return Message.parse(raw)
