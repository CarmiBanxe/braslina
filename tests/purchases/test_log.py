import importlib


def test_purchase_log_module_imports():
    module = importlib.import_module("src.purchases.log")
    assert module is not None
