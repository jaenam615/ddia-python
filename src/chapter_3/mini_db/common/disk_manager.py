import os

from chapter_3.mini_db.interfaces.disk_manager_interface import DiskManagerInterface

PAGE_SIZE = 4096

class GeneralDiskManager(DiskManagerInterface):
    def __init__(self, path: str):
        os.makedirs(path, exist_ok=True)
        self.path = os.path.join(path, "data.bin")
        if not os.path.exists(self.path):
            with open(self.path, "wb") as f:
                f.truncate(0)
        self._page_count = os.path.getsize(self.path) // PAGE_SIZE

    def read_page(self, page_id: int) -> bytes:
        with open(self.path, "rb") as f:
            f.seek(page_id * PAGE_SIZE)
            return f.read(PAGE_SIZE)

    def write_page(self, page_id: int, data: bytes):
        assert len(data) <= PAGE_SIZE
        data = data.ljust(PAGE_SIZE, b"\x00")
        with open(self.path, "r+b") as f:
            f.seek(page_id * PAGE_SIZE)
            f.write(data)
        if page_id >= self._page_count:
            self._page_count = page_id + 1

    def alloc_page(self) -> int:
        pid = self._page_count
        # extend file by one page
        with open(self.path, "ab") as f:
            f.write(b"\x00" * PAGE_SIZE)
        self._page_count += 1
        return pid