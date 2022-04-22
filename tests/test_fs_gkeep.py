import pytest
from gkeepapi.node import List as GKeepListRaw

from taskwarrior_syncall.filesystem_file import FilesystemFile
from taskwarrior_syncall.google.gkeep_note import GKeepNote


def test_convert_fs_file_to_gkeep_note(
    fs_file: FilesystemFile, expected_gkeep_note: GKeepNote
):
    pass


def test_convert_gkeep_note_to_fs_file(
    expected_gkeep_note: GKeepNote, fs_file: FilesystemFile
):
    pass


def test_convert_gkeep_list_to_fs_file(
    expected_gkeep_list: GKeepList, fs_file: FilesystemFile
):
    pass
