import datetime
import uuid
from pathlib import Path

import xattr
from bubop.fs import FileType
from item_synchronizer.types import ID

from taskwarrior_syncall.concrete_item import ConcreteItem, ItemKey, KeyType


def _generate_uuid() -> str:
    return str(uuid.uuid4())


class FilesystemFile(ConcreteItem):
    """Encode the interaction with a filesystem entity.

    This uses the inode of a file as its unique identifier. Only filesystems that use inodes
    are supported.

    Exposes a similar API to the NotionTodoBlock class.
    """

    _attr = "user.syncall.uuid"

    def __init__(self, path: Path, contents: str = "", filetype=FileType.FILE):
        """Create a file using the given path and the given contents."""
        super().__init__(
            keys=(
                ItemKey("last_modified_date", KeyType.Date),
                ItemKey("contents", KeyType.String),
            )
        )

        if not filetype is FileType.FILE:
            raise NotImplementedError("Only supporting synchronization for raw files.")

        self._path = path
        self._contents = contents
        self._filetype = filetype

        self._fd = self._path.open()

    def close(self):
        """Teardown method.

        - Close open file descriptors.
        """
        self._fd.write(self._contents)
        self._fd.close()

    def _assign_id(self):
        """Embed a UUID in the metadata of the open file."""
        xattr.setxattr(self._fd, self._attr, _generate_uuid())

    def _id(self) -> ID:
        return xattr.getxattr(self._fd, self._attr).decode()

    @property
    def contents(self):
        return self._contents

    @contents.setter
    def contents(self, new_contents):
        self._contents = new_contents

    @property
    def last_modified_date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._path.stat().st_mtime)

    def delete(self) -> None:
        self.close()
        self._path.unlink()
