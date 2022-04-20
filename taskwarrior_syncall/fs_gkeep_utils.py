"""Filesystem <-> Google Keep conversion functions"""
from bubop.time import format_datetime_tz

from taskwarrior_syncall.fs_file import FsFile
from taskwarrior_syncall.google.gkeep_note import GKeepNote


def convert_fs_file_to_gkeep_note(fs_file: FsFile) -> GKeepNote:
    pass


def convert_gkeep_note_to_fs_file(gkeep_note: GKeepNote) -> FsFile:
    pass
