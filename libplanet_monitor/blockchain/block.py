from dataclasses import dataclass, field
from typing import List, AnyStr, Optional

from .address import Address
from .hashcash import Hash, Nonce
from .transaction import Transaction


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
