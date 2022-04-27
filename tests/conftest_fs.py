from pathlib import Path

import pytest

from taskwarrior_syncall.filesystem_file import FilesystemFile
from taskwarrior_syncall.filesystem_side import FilesystemSide


@pytest.fixture
def fs_file(request: pytest.FixtureRequest) -> dict:
    """Fixture to parametrize on."""
    param = request.param  # type: ignore
    return request.getfixturevalue(param)


@pytest.fixture
def fs_side(request: pytest.FixtureRequest) -> dict:
    """Fixture to parametrize on."""
    param = request.param  # type: ignore
    return request.getfixturevalue(param)


@pytest.fixture
def fs_file_default_fname() -> str:
    return "file.txt"


@pytest.fixture
def fs_file_default_name() -> str:
    return "file"


@pytest.fixture
def non_existent_python_path(tmpdir, fs_file_default_fname) -> Path:
    return Path(tmpdir) / fs_file_default_fname


@pytest.fixture
def fs_file_empty(tmpdir, fs_file_default_fname) -> FilesystemFile:
    fs = FilesystemFile(fs_file_default_fname)
    fs.root = Path(tmpdir)

    return fs


@pytest.fixture
def python_path_with_content(tmpdir, fs_file_default_fname) -> Path:
    path = Path(tmpdir) / fs_file_default_fname
    path.write_text(
        """Here is some
multi-line text
with unicode 🚀😄 characters.
"""
    )
    return path


@pytest.fixture
def fs_file_with_content(python_path_with_content: Path) -> FilesystemFile:
    fs = FilesystemFile(python_path_with_content.name)
    fs.root = python_path_with_content.parent

    return fs


@pytest.fixture
def fs_side_no_items(tmpdir) -> FilesystemSide:
    return FilesystemSide(filesystem_root=Path(tmpdir))


@pytest.fixture
def fs_side_with_existing_items(tmpdir) -> FilesystemSide:
    dir_ = Path(tmpdir)
    for i in range(10):
        with FilesystemFile(path=f"file{i}") as fs:
            fs.contents = f"Some content for file{i}"
            fs.root = dir_

    return FilesystemSide(filesystem_root=dir_)
