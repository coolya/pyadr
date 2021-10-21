from pathlib import Path

import pytest
from git import Repo
from loguru import logger

import pyadr
from pyadr.const import DEFAULT_ADR_PATH, DEFAULT_CONFIG_FILE_NAME
from pyadr.core import AdrCore
from pyadr.git.core import GitAdrCore

LOGGING_VERBOSE = 18
LOGGING_VERY_VERBOSE = 16

logger.level("VERBOSE", LOGGING_VERBOSE, color="<bold>", icon="🔈️")
logger.level("VERY_VERBOSE", LOGGING_VERY_VERBOSE, color="<bold>", icon="🔊")


@pytest.fixture()
def adr_tmp_path(tmp_path):
    path = tmp_path / DEFAULT_ADR_PATH
    path.mkdir(parents=True)
    yield path


@pytest.fixture()
def tmp_repo(tmp_path):
    repo = Repo.init(tmp_path, initial_branch="main")

    file = Path(tmp_path / "foo")
    file.touch()

    repo.index.add([str(file)])
    repo.index.commit("initial commit")

    yield repo


@pytest.fixture(autouse=True)
def initialise_config(monkeypatch, tmp_path):
    monkeypatch.setattr(
        pyadr.config.AdrConfig, "config_file_path", tmp_path / DEFAULT_CONFIG_FILE_NAME
    )
    assert (
        pyadr.config.AdrConfig.config_file_path == tmp_path / DEFAULT_CONFIG_FILE_NAME
    )
    monkeypatch.setattr(
        pyadr.git.config.GitAdrConfig,
        "config_file_path",
        tmp_path / DEFAULT_CONFIG_FILE_NAME,
    )
    assert (
        pyadr.git.config.GitAdrConfig.config_file_path
        == tmp_path / DEFAULT_CONFIG_FILE_NAME
    )


@pytest.fixture()
def adr_core():
    yield AdrCore()


@pytest.fixture()
def git_adr_core():
    yield GitAdrCore()
