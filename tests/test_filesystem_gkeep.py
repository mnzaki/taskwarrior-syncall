from pathlib import Path

import pytest
from gkeepapi.node import List

from taskwarrior_syncall.filesystem_file import FilesystemFile
from taskwarrior_syncall.filesystem_gkeep_utils import (
    convert_filesystem_file_to_gkeep_note,
    convert_gkeep_note_to_filesystem_file,
)
from taskwarrior_syncall.google.gkeep_note import GKeepNote


def test_convert_fs_file_to_gkeep_note_from_empty(
    fs_file_empty: FilesystemFile, fs_file_default_name: str
):
    out = convert_filesystem_file_to_gkeep_note(fs_file_empty)
    assert fs_file_empty.id is not None
    assert out.title == fs_file_default_name
    assert out.plaintext == ""


def test_convert_fs_file_to_gkeep_note_with_existing_content(
    fs_file_with_content: FilesystemFile, fs_file_default_name: str
):
    out = convert_filesystem_file_to_gkeep_note(fs_file_with_content)
    assert fs_file_with_content.id is not None
    assert out.title == fs_file_default_name
    assert out.plaintext == fs_file_with_content.contents


def test_convert_gkeep_note_to_fs_file_from_empty(
    gkeep_note_empty_instance: GKeepNote, tmpdir
):
    fs_root = Path(tmpdir)
    out = convert_gkeep_note_to_filesystem_file(
        gkeep_note_empty_instance, filesystem_root=fs_root
    )
    assert out.title == gkeep_note_empty_instance.title
    assert out.contents == ""
    assert out.id is not None
