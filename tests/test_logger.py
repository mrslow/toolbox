import logging
import pytest

from toolbox import Logger
from toolbox.logger import LoggerNotFound


@pytest.fixture
def logger(tmpdir):
    return Logger(tmpdir)


def test_register(logger):
    logger.register('test_register')
    assert type(logger.loggers['test_register']) == logging.Logger
    assert len(logger.loggers['test_register'].handlers) == 1


def test_register_cout(logger):
    logger.register('test_cout', cout=True)
    assert type(logger.loggers['test_cout']) == logging.Logger
    assert len(logger.loggers['test_cout'].handlers) == 2


def test_get(logger):
    logger.register('test_get')
    assert type(logger.get('test_get')) == logging.Logger
    with pytest.raises(LoggerNotFound):
        logger.get('test_unknown')


def test_attr(logger):
    logger.register('test_attr')
    assert logger.test_attr == logger.get('test_attr')
