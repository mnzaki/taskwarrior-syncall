"""Filesystem <-> Google Keep conversion functions"""

from taskwarrior_syncall.filesystem_file import FilesystemFile
from taskwarrior_syncall.google.gkeep_note import GKeepNote


def convert_filesystem_file_to_gkeep_note(filesystem_file: FilesystemFile) -> GKeepNote:
    return GKeepNote(plaintext=filesystem_file.contents, title=filesystem_file.title)


def convert_gkeep_note_to_filesystem_file(gkeep_note: GKeepNote) -> FilesystemFile:
    fs = FilesystemFile(path=gkeep_note.title)
    fs.contents = gkeep_note.plaintext
    return fs
