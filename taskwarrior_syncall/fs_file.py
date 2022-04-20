import datetime
from functools import cached_property
from pathlib import Path
from typing import Any, Mapping, Sequence

from bubop.fs import FileType
from bubop.time import is_same_datetime
from gkeepapi.node import ListItem
from item_synchronizer.types import ID
from loguru import logger


class FsFile(Mapping):
    """Encode the interaction with a filesystem entity.

    This uses the inode of a file as its unique identifier. Only filesystems that use inodes
    are supported.

    Exposes a similar API to the NotionTodoBlock class.
    """

    _key_names = {
        "last_modified_date",
        "contents",
        "id",
    }

    _date_key_names = {"last_modified_date"}

    def __init__(self, path: Path, contents: str = "", filetype=FileType.FILE):
        """Create a file using the given path and the given contents."""

        if not filetype is FileType.FILE:
            raise NotImplementedError("Only supporting synchronization for raw files.")

        self._path = path
        self._contents = contents
        self._filetype = filetype

    @cached_property
    def id(self) -> ID:
        return ID(self._path.stat().st_ino)

    @property
    def contents(self):
        return self._contents

    @contents.setter
    def contents(self, new_contents):
        self._contents = new_contents

    @property
    def last_modified_date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._path.stat().st_mtime)

    def __getitem__(self, key) -> Any:
        return getattr(self, key)

    def __iter__(self):
        for k in self._key_names:
            yield k

    def __len__(self):
        return len(self._key_names)

    def delete(self) -> None:
        self._path.unlink()

    def compare(self, other: "FsFile", ignore_keys: Sequence[str] = []) -> bool:
        """Compare two items, return True if they are considered equal."""
        raise NotImplementedError()
