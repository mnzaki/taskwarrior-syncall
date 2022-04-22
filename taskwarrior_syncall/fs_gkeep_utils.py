"""Filesystem <-> Google Keep conversion functions"""
from bubop.time import format_datetime_tz

from taskwarrior_syncall.filesystem_file import FilesystemFile
from taskwarrior_syncall.google.gkeep_note import GKeepNote


def convert_filesystem_file_to_gkeep_note(filesystem_file: FsFile) -> GKeepNote:
    pass


def convert_gkeep_note_to_filesystem_file(gkeep_note: GKeepNote) -> FsFile:
    pass
