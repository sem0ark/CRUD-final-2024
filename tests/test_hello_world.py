from unittest import TestCase


class TestHelloWorld(TestCase):
    def test_upper(self) -> None:
        self.assertEqual("hello world!".upper(), "HELLO WORLD!")
