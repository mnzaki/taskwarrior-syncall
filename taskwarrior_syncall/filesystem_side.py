from typing import Optional, Sequence

from item_synchronizer.types import ID

from taskwarrior_syncall.concrete_item import ConcreteItem
from taskwarrior_syncall.sync_side import ItemType, SyncSide


class FilesystemSide(SyncSide):
    """Integration for managing files in a local filesystem.

    - Embed the UUID as an extended attribute of each file.
    """

    def __init__(self, **kargs):
        pass

    @classmethod
    def id_key(cls) -> str:
        return "id"

    @classmethod
    def summary_key(cls) -> str:
        return "title"


    def __init__(self, name: str, fullname: str, *args, **kargs) -> None:
        self._fullname = fullname
        self._name = name

   def start(self):
        """Initialization steps.

        Call this manually. Derived classes can take care of setting up data
        structures / connection, authentication requests etc.
        """
        pass

    def finish(self):
        """Finalization steps.

        Call this manually. Derived classes can take care of closing open connections, flashing
        their cached data, etc.
        """
        pass

    def get_all_items(self, **kargs) -> Sequence[ItemType]:
        raise NotImplementedError("Implement this")

    def get_item(self, item_id: ID, use_cached: bool = False) -> Optional[ItemType]:
        raise NotImplementedError("Implement this")

    def delete_single_item(self, item_id: ID):
        raise NotImplementedError("Should be implemented in derived")

    def update_item(self, item_id: ID, **changes):
        raise NotImplementedError("Should be implemented in derived")

    def add_item(self, item: ItemType) -> ItemType:
        raise NotImplementedError("Implement this")

    @classmethod
    def items_are_identical(
        cls, item1: ItemType, item2: ItemType, ignore_keys: Optional[Sequence[ItemKey]] = None
    ) -> bool:
        raise NotImplementedError("Implement this")

    @classmethod
    def items_are_identical(
        cls, item1: ConcreteItem, item2: ConcreteItem, ignore_keys: Sequence[str] = []
    ) -> bool:
        ignore_keys_ = ["last_edited_time"]
        ignore_keys_.extend(ignore_keys)
        return item1.compare(item2, ignore_keys=ignore_keys_)
        return True
