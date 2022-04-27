from typing import Sequence

import pytest

from taskwarrior_syncall.filesystem_file import FilesystemFile
from taskwarrior_syncall.filesystem_side import FilesystemSide


@pytest.mark.parametrize(
    "fs_side",
    ["fs_side_no_items", "fs_side_with_existing_items"],
    indirect=True,
)
def test_create_new_item(fs_side: FilesystemSide):
    root = fs_side.filesystem_root

    # create a new FilesystemFile
    title = "the title"
    contents = "Kalimera!"
    new_item = FilesystemFile(path=title)
    new_item.contents = contents
    new_id = new_item.id
    assert new_id is not None

    all_items_before_addition = fs_side.get_all_items()
    prev_len = len(all_items_before_addition)

    # add the item to the side, assert that the given path is written to disk on
    # fs_side.add_item
    item_path = root / f"{title}.txt"
    assert not item_path.exists()
    fs_side.add_item(new_item)
    assert item_path.is_file()

    # get the newly created item - make sure that its the same item as returned by
    # get_all_items()
    all_items_after_addition = fs_side.get_all_items()
    assert len(all_items_after_addition) == prev_len + 1
    fs_file = [item for item in all_items_after_addition if item.id == new_id][0]
    fs_file2 = fs_side.get_item(item_id=new_id)
    assert fs_file == fs_file2


def test_update_item(fs_side_with_existing_items: FilesystemSide):
    fs_side = fs_side_with_existing_items
    item = fs_side.get_all_items()[0]
    id_ = item.id
    assert id_ is not None

    new_contents = f"{item.contents} and some new content"
    new_title = "Some other title"
    item.contents = new_contents
    item.title = new_title
    for sth in item:
        print(sth)
    fs_side.update_item(item_id=id_, **item)
    updated_item = fs_side.get_item(item_id=id_)
    assert updated_item is not None

    assert updated_item.contents == new_contents
    assert updated_item.title == new_title


def test_delete_item():
    pass


def test_finish():
    pass


def test_items_are_identical():
    pass


def test_id_key_and_summary():
    pass


def test_get_all_items(fs_side_with_existing_items: FilesystemSide):
    fs_side = fs_side_with_existing_items
    fs_files: Sequence[FilesystemFile] = fs_side.get_all_items()
    assert len(fs_files) == 10
    for fs_file in fs_files:
        # contents should be something like "Some content for file3"
        # title should be file3
        assert fs_file.title in fs_file.contents
        assert fs_file.id is not None


def test_item_not_in_cache():
    pass
