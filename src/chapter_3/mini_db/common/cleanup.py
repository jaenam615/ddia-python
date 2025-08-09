import os
import shutil


def wipe_path(path: str) -> None:
    """Delete a file or directory tree if it exists (best-effort)."""
    if not path:
        return
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
    else:
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
        except Exception:
            # ignore
            pass

