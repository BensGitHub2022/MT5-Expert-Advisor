
import pytest
from src.context_factory import ContextFactory
from src.context_mt5 import ContextMT5
from src.context_sim import ContextSimulator


def test_meta_trader_factory_create_production():
    factory = ContextFactory(True)
    meta = factory.create_context()
    assert type(meta) == ContextMT5

def test_meta_trader_factory_create_mock():
    factory = ContextFactory(False)
    meta = factory.create_context()
    assert type(meta) == ContextSimulator
