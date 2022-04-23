from pathlib import Path

import pytest

from taskwarrior_syncall.filesystem_file import FilesystemFile


@pytest.fixture()
def fs_file(request: pytest.FixtureRequest) -> dict:
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
    return FilesystemFile(path=Path(tmpdir) / fs_file_default_fname)


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
    return FilesystemFile(path=python_path_with_content)
