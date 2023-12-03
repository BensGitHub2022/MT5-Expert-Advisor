
import pytest
from src.meta_trader_factory import MetaTraderFactory
from src.meta_trader_adapter import MetaTraderAdapter
from src.meta_trader_mock import MetaTraderMock


def test_meta_trader_factory_create_production():
    factory = MetaTraderFactory(True)
    meta = factory.create_meta_trader()
    assert type(meta) == MetaTraderAdapter

def test_meta_trader_factory_create_mock():
    factory = MetaTraderFactory(False)
    meta = factory.create_meta_trader()
    assert type(meta) == MetaTraderMock
