from dataclasses import dataclass
from typing import List, NewType

from bencodex import BValue, dumps, loads

from .address import Address
from .crypto import PublicKey


_NONCE_KEY = b'n'
_SIGNER_KEY = b's'
_UPDATED_ADDRESSES_KEY = b'u'
_PUBLIC_KEY_KEY = b'p'
_TIMESTAMP_KEY = b't'
_ACTIONS_KEY = b'a'
_SIGNATURE_KEY = b'S'

Signature = NewType('Signature', bytes)


@dataclass(frozen=True)
class Transaction:

    nonce: int
    signer: Address
    public_key: PublicKey
    signature: Signature
    timestamp: str
    updated_addresses: List[Address]
    actions: List[dict]

    def serialize(self) -> bytes:
        return dumps(self.bencode())

    def bencode(self) -> BValue:
        return {
            _NONCE_KEY: self.nonce,
            _SIGNER_KEY: self.signer,
            _PUBLIC_KEY_KEY: self.public_key,
            _SIGNATURE_KEY: self.signature,
            _TIMESTAMP_KEY: self.timestamp,
            _UPDATED_ADDRESSES_KEY: self.updated_addresses,
            _ACTIONS_KEY: self.actions,
        }

    @staticmethod
    def deserialize(raw: bytes) -> Transaction:
        decoded = loads(raw)
        return Transaction.from_dict(decoded)

    @staticmethod
    def from_dict(raw: dict) -> Transaction:
        return Transaction(
            nonce=raw[_NONCE_KEY],
            signer=raw[_SIGNER_KEY],
            public_key=raw[_PUBLIC_KEY_KEY],
            signature=raw[_SIGNATURE_KEY],
            timestamp=raw[_TIMESTAMP_KEY],
            updated_addresses=raw[_UPDATED_ADDRESSES_KEY],
            actions=raw[_ACTIONS_KEY],
        )
