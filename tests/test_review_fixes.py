from pathlib import Path

import pytest

from finetune.config import Config

webui_app = pytest.importorskip("webui.app")
load_data_files = webui_app.load_data_files
resolve_data_file_path = webui_app.resolve_data_file_path


def test_config_to_dict_round_trip_preserves_derived_defaults():
    config = Config(overrides={"batch_size": 32})
    round_tripped = Config(overrides=config.to_dict())

    assert round_tripped.batch_size == 32
    assert round_tripped.n_train_iter == 2000 * 32
    assert round_tripped.n_val_iter == 400 * 32
    assert round_tripped.backtest_benchmark == "SH000300"


def test_config_explicit_iteration_overrides_are_preserved():
    config = Config(overrides={"batch_size": 16, "n_train_iter": 123, "n_val_iter": 45})

    assert config.n_train_iter == 123
    assert config.n_val_iter == 45


def test_load_data_files_returns_repo_relative_paths():
    data_files = load_data_files()

    assert data_files, "Expected at least one example data file to be discoverable."
    assert all(not Path(entry["path"]).is_absolute() for entry in data_files)


def test_resolve_data_file_path_rejects_traversal_outside_allowed_dirs():
    resolved_path, error = resolve_data_file_path("../../etc/passwd")

    assert resolved_path is None
    assert error is not None


def test_resolve_data_file_path_accepts_known_example_dataset():
    resolved_path, error = resolve_data_file_path("examples/data/XSHG_5min_600977.csv")

    assert error is None
    assert resolved_path is not None
    assert resolved_path.name == "XSHG_5min_600977.csv"
