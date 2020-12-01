import os
import tempfile
from pathlib import Path

import pytest

from powersimdata.tests.mock_ssh import MockConnection
from powersimdata.utility.server_setup import get_server_user
from powersimdata.utility.transfer_data import SSHDataAccess

CONTENT = b"content"


@pytest.fixture
def data_access():
    data_access = SSHDataAccess()
    yield data_access
    data_access.close()


@pytest.fixture
def temp_fs(tmp_path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    dest_dir = tmp_path / "dest"
    dest_dir.mkdir()
    return src_dir, dest_dir


@pytest.fixture
def mock_data_access(monkeypatch, temp_fs):
    data_access = SSHDataAccess()
    monkeypatch.setattr(data_access, "_ssh", MockConnection())
    data_access.root = temp_fs[0]
    data_access.dest_root = temp_fs[1]
    yield data_access
    data_access.close()


@pytest.fixture
def make_temp(temp_fs):
    files = []

    def _make_temp(rel_path=None):
        if rel_path is None:
            rel_path = Path("")
        location = temp_fs[0] / rel_path
        test_file = tempfile.NamedTemporaryFile(dir=location)
        files.append(test_file)
        test_file.write(CONTENT)
        test_file.seek(0)
        return os.path.basename(test_file.name)

    yield _make_temp
    for f in files:
        f.close()


def _check_content(filepath):
    assert os.path.exists(filepath)
    with open(filepath, "rb") as f:
        assert CONTENT == f.read()


@pytest.mark.integration
@pytest.mark.ssh
def test_setup_server_connection(data_access):
    _, stdout, _ = data_access.execute_command("whoami")
    assert stdout.read().decode("utf-8").strip() == get_server_user()


def test_mocked_correctly(mock_data_access):
    assert isinstance(mock_data_access.ssh, MockConnection)


@pytest.mark.wip
def test_copy_from(mock_data_access, temp_fs, make_temp):
    fname = make_temp()
    mock_data_access.copy_from(fname)
    _check_content(os.path.join(temp_fs[1], fname))


@pytest.mark.wip
def test_copy_from_multi_path(mock_data_access, temp_fs, make_temp):
    rel_path = Path("foo", "bar")
    src_path = temp_fs[0] / rel_path
    src_path.mkdir(parents=True)
    fname = make_temp(rel_path)
    mock_data_access.copy_from(fname, rel_path)
    _check_content(os.path.join(temp_fs[1], rel_path, fname))


@pytest.mark.wip
def test_copy_to(mock_data_access, tmp_path):
    pass
