from pathlib import Path
from tempfile import TemporaryFile

import xattr

from taskwarrior_syncall.filesystem_file import FilesystemFile


def test_fs_file_flush_attrs(python_path_with_content: Path):
    """
    Make sure that extended attributes of the FilesystemFile is only written when
    we actually .flush() it.
    """
    p = python_path_with_content
    fs_file = FilesystemFile(path=p)

    x = xattr.xattr(p)
    assert not x.list()
    assert fs_file.id is not None

    # flush -----------------------------------------------------------------------------------
    fs_file.flush()

    assert len(x.list()) == 1
    assert x.get(FilesystemFile._attr) is not None


def test_fs_file_flush_change_title_content(python_path_with_content: Path):
    """
    Make sure that title and content of the FilesystemFile is written when we actually .flush()
    it.
    """
    p = python_path_with_content
    path_contents = p.read_text()
    path_title = p.stem

    fs_file = FilesystemFile(path=p)
    assert fs_file.contents == path_contents
    assert fs_file.title == path_title
    assert fs_file.id != None

    # change contents and title
    new_contents = "New contents\nwith a bunch of lines\n🥳🥳🥳"
    new_title = "ένας νέος τίτλος"  # title uses unicode
    fs_file.contents = new_contents
    fs_file.title = new_title

    # flush -----------------------------------------------------------------------------------
    fs_file.flush()

    # test new title
    new_path = p.with_name(new_title).with_suffix(".txt")
    assert not p.exists()
    assert new_path.is_file()

    # test new contents
    assert new_path.read_text() == new_contents


def test_fs_file_dict_fns(non_existent_python_path):
    fs_file = FilesystemFile(path=non_existent_python_path)
    assert set(("last_modified_date", "contents", "title", "id")).issubset(
        key.name for key in fs_file.keys()
    )


def test_fs_file_delete(python_path_with_content: Path):
    """Verify that deletion happens on flush and not before it."""
    p = python_path_with_content
    fs = FilesystemFile(p)

    assert p.is_file()
    fs.delete()
    assert p.is_file()
    fs.flush()
    assert not p.exists()


def test_fs_file_open_twice(python_path_with_content: Path):
    new_content1 = "some other content"
    new_content2 = "some yet another content"
    p = python_path_with_content
    fs1 = FilesystemFile(p)
    fs1.contents = new_content1
    fs1.flush()
    assert p.read_text() == new_content1

    fs2 = FilesystemFile(p)
    fs2.contents = new_content2
    fs2.flush()
    assert p.read_text() == new_content2
