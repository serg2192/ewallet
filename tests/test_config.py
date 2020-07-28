import pytest

from billing.errors import InvalidInputParamsError
from billing.main import init_app


@pytest.mark.xfail(reason='Not existent path', raises=FileNotFoundError, run=True, strict=True)
def test_config(monkeypatch):
    with monkeypatch.context() as m:
        m.setenv('CONFIG_PATH', 'nonexistent_path')
        init_app()


def test_config_with_invalid_config(monkeypatch, tmp_path):
    with monkeypatch.context() as m:
        file_ = tmp_path / "mock_config.txt"
        file_.write_text('')
        m.setenv('CONFIG_PATH', str(file_))
        with pytest.raises(InvalidInputParamsError):
            init_app()
        file_.unlink()
        tmp_path.rmdir()
