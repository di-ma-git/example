class TestContext:

    def __init__(self):
        self._test_params = {}

    def set_param(self, key: str, value: str):
        self._test_params[key] = value

    def get_param(self, key: str) -> str:
        return self._test_params.get(key)

    def clear(self):
        self._test_params.clear()
