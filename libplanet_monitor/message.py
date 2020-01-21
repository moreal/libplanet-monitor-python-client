import abc
from abc import ABC

from bencodex import BValue, loads, dumps
from enum import IntEnum, auto
from typing import List, Type, Dict


class MessageType(IntEnum):
    # key: (,)
    GetTip = 0
    Tip = auto()

    # key: (block-index,)
    GetBlockHash = auto()
    BlockHash = auto()

    # key: (block-hash,)
    GetBlock = auto()
    Block = auto()

    # TODO: implement messages below when BlockHeader became accessible.
    # GetBlockHeader = auto()
    # BlockHeader = auto()
    # GetTransactions = auto()
    # Transactions = auto()

    # TODO: implement state-references with pager.
    # key: (address, page,)
    # GetStateReferences = auto()
    # StateReferences = auto()

    # key: (block - hash, address,)
    GetState = auto()
    State = auto()


# FIXME: Is it okay to manage mapping like below?
_enum_to_type: Dict[MessageType, Type['Message']] = dict()
_type_to_enum: Dict[Type['Message'], MessageType] = dict()


def message_decorator(message_type: MessageType):
    def decorator(message_class: Type['Message']):
        _enum_to_type[message_type] = message_class
        _type_to_enum[message_class] = message_type
        return message_class
    return decorator


class Message(ABC):

    @staticmethod
    @abc.abstractmethod
    def from_frames(frames: List[bytes]):
        ...

    @property
    @abc.abstractmethod
    def frames(self) -> List[bytes]:
        ...

    def as_multipart(self) -> List[bytes]:
        message_type = _type_to_enum[type(self)]
        return [int.to_bytes(message_type, 4, 'big'), ] + self.frames

    @staticmethod
    def parse(frames: List[bytes]) -> Type['Message']:
        message_type: MessageType = int.from_bytes(frames[0], 'big')
        return _enum_to_type[message_type].from_frames(frames[1:])


@message_decorator(MessageType.GetTip)
class GetTip(Message):
    def __init__(self):
        ...

    @staticmethod
    def from_frames(frames: List[bytes]):
        return GetTip()

    @property
    def frames(self) -> List[bytes]:
        return list()


@message_decorator(MessageType.Tip)
class Tip(Message):
    def __init__(self, block_index: int, block_hash: bytes):
        self.block_index = block_index
        self.block_hash = block_hash

    @staticmethod
    def from_frames(frames: List[bytes]):
        block_index = int.from_bytes(frames[0], 'big')
        block_hash = frames[1]
        return Tip(block_index, block_hash)

    @property
    def frames(self) -> List[bytes]:
        raw_block_index = int.to_bytes(self.block_index, 8, 'big')
        raw_block_hash = self.block_hash
        return [raw_block_index, raw_block_hash]


@message_decorator(MessageType.GetState)
class GetState(Message):
    def __init__(self, block_hash: bytes, address: bytes):
        self.block_hash = block_hash
        self.address = address

    @staticmethod
    def from_frames(frames: List[bytes]):
        block_hash = frames[0]
        address = int.from_bytes(frames[0], 'big')
        return GetState(block_hash, address)

    @property
    def frames(self) -> List[bytes]:
        raw_block_hash = self.block_hash
        raw_address = self.address
        return [raw_block_hash, raw_address]


@message_decorator(MessageType.State)
class State(Message):
    def __init__(self, state: BValue):
        self.state = state

    @staticmethod
    def from_frames(frames: List[bytes]):
        state = loads(frames[0])
        return State(state)

    @property
    def frames(self) -> List[bytes]:
        raw_state = dumps(self.state)
        return [raw_state]


@message_decorator(MessageType.GetBlock)
class GetBlock(Message):
    def __init__(self, block_hash: bytes):
        self.block_hash = block_hash

    @staticmethod
    def from_frames(frames: List[bytes]):
        block_hash = frames[0]
        return GetBlock(block_hash)

    @property
    def frames(self) -> List[bytes]:
        return [self.block_hash]


@message_decorator(MessageType.Block)
class Block(Message):
    def __init__(self, block: BValue):
        self.block = block

    @staticmethod
    def from_frames(frames: List[bytes]):
        block = loads(frames[0])
        return Block(block)

    @property
    def frames(self) -> List[bytes]:
        raw_block = dumps(self.block)
        return [raw_block]
