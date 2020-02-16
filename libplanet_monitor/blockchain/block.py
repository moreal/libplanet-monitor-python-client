from dataclasses import dataclass, field
from typing import AnyStr, Dict, List, Optional

from bencodex import BValue, dumps, loads

from .address import Address
from .hashcash import Hash, Nonce
from .transaction import Transaction


_INDEX_KEY = b'i'
_TIMESTAMP_KEY = b't'
_DIFFICULTY_KEY = b'd'
_NONCE_KEY = b'n'
_MINER_KEY = b'm'
_PREVIOUS_HASH_KEY = b'p'
_HASH_KEY = b'h'
_BLOCK_HEADER_KEY = 'H'
_TRANSACTIONS_KEY = b'T'


@dataclass(frozen=True)
class Block:

    index: int
    difficulty: int
    hash: Hash
    nonce: Nonce
    miner: Address
    timestamp: str
    transactions: List[Transaction]
    previous_hash: Optional[Hash]

    def serialize(self) -> bytes:
        return dumps(self.bencode())

    def bencode(self) -> BValue:
        return {
            _BLOCK_HEADER_KEY: {
                _INDEX_KEY: self.index,
                _TIMESTAMP_KEY: self.timestamp,
                _DIFFICULTY_KEY: self.difficulty,
                _NONCE_KEY: self.nonce,
                _MINER_KEY: self.miner,
                _PREVIOUS_HASH_KEY: self.previous_hash,
                _HASH_KEY: self.hash,
            },
            _TRANSACTIONS_KEY: self.transactions
        }

    @staticmethod
    def deserialize(raw: bytes) -> Block:
        decoded = loads(raw)
        block_header = decoded[_BLOCK_HEADER_KEY]
        transactions = list(map(Transaction.from_dict, decoded[_TRANSACTIONS_KEY]))
        return Block(
            index=block_header[_INDEX_KEY],
            timestamp=block_header[_TIMESTAMP_KEY],
            difficulty=block_header[_DIFFICULTY_KEY],
            nonce=block_header[_NONCE_KEY],
            miner=block_header[_MINER_KEY],
            previous_hash=block_header[_PREVIOUS_HASH_KEY],
            hash=block_header[_HASH_KEY],
            transactions=transactions
        )
