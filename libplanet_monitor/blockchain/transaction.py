from dataclasses import dataclass
from typing import AnyStr, NewType, Sequence

from .address import Address
from .crypto import PublicKey

Signature = NewType('Signature', bytes)

@dataclass(frozen=True)
class Transaction:

    nonce: int
    signer: Address
    public_key: PublicKey
    signature: Signature
    timestamp: str
    updatedAddresses: Sequence[Address]
