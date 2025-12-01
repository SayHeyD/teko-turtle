import importlib

def test_main_function_calls_run(monkeypatch):
    called = {"count": 0}

    class FakeApp:
        def run(self):
            called["count"] += 1

    # Import the module (safe: the guard won't trigger on import)
    mod = importlib.import_module("cutting_board_drawers_optimizer.__main__")

    # Replace the imported class with our fake
    monkeypatch.setattr(mod, "CuttingBoardDrawersOptimizerApp", FakeApp)

    # Act
    mod.main()

    # Assert
    assert called["count"] == 1