from pathlib import Path
from typing import MutableMapping, Optional, Sequence

from item_synchronizer.types import ID
from loguru import logger

from taskwarrior_syncall.concrete_item import ConcreteItem, ItemKey
from taskwarrior_syncall.google.gkeep_note import GKeepNote
from taskwarrior_syncall.sync_side import ItemType, SyncSide


class GKeepNoteSide(SyncSide):
    """Create, update, delete notes on the Google Keep side."""

    @classmethod
    def id_key(cls) -> str:
        return "id"

    @classmethod
    def summary_key(cls) -> str:
        return "title"

    @classmethod
    def last_modification_key(cls) -> str:
        return "last_modified_date"

    def __init__(self) -> None:
        pass

    def start(self):
        pass

    def finish(self):
        pass

    def get_all_items(self, **kargs) -> Sequence[GKeepNote]:
        pass

    def update_item(self, item_id: ID, **changes):
        pass

    def add_item(self, item: GKeepNote) -> GKeepNote:
        pass

    @classmethod
    def items_are_identical(
        cls, item1: ConcreteItem, item2: ConcreteItem, ignore_keys: Sequence[str] = []
    ) -> bool:
        ignore_keys_ = [cls.last_modification_key()]
        ignore_keys_.extend(ignore_keys)
        return item1.compare(item2, ignore_keys=ignore_keys_)
