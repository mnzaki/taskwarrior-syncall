import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Iterator, Mapping, Sequence

from bubop.time import is_same_datetime
from item_synchronizer.types import ID
from loguru import logger


class KeyType(Enum):
    String = auto()
    Date = auto()


@dataclass
class ItemKey:
    name: str
    type: KeyType


class _ConcreteItemMeta(type(Mapping), ABC):
    pass


class ConcreteItem(_ConcreteItemMeta):
    """Type of the items passed around in the synchronization classes."""

    def __init__(self, keys: Sequence[ItemKey]):
        self._keys = set(keys)
        self._keys.add(ItemKey(name="id", type=KeyType.String))

    @property
    def id(self) -> ID:
        return self._id()

    @abstractmethod
    def _id(self) -> str:
        pass

    def __getitem__(self, key) -> Any:
        return getattr(self, key)

    def __iter__(self) -> Iterator[ItemKey]:
        for k in self._keys:
            yield k

    def __len__(self):
        return len(self._keys)

    def compare(self, other: "ConcreteItem", keys_to_check: Sequence[ItemKey]) -> bool:
        """Compare two items, return True if they are considered equal, False otherwise"""

        for key in keys_to_check:
            if key.type is KeyType.Date:
                if not is_same_datetime(
                    self[key], other[key], tol=datetime.timedelta(minutes=10)
                ):
                    logger.opt(lazy=True).trace(
                        f"\n\nItems differ\n\nItem1\n\n{self}\n\nItem2\n\n{other}\n\nKey"
                        f" [{key}] is different - [{repr(self[key])}] | [{repr(other[key])}]"
                    )
                    return False
            else:
                if self[key] != other[key]:
                    logger.opt(lazy=True).trace(f"Items differ [{key}]\n\n{self}\n\n{other}")
                    return False

        return True
