import pytest

from chapter_3.mini_db.interfaces.processing_interface import ProcessingInterface


class DummyProc(ProcessingInterface):
    def execute(self, op: str, *args, **kwargs):
        return op


def test_processing_interface_contract():
    p = DummyProc()
    assert p.execute("x") == "x"

