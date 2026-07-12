import shutil
import stat
from pathlib import Path


def remove_dir(path):
    def on_error(_func, fpath, _exc_info):
        Path(fpath).chmod(stat.S_IWRITE)
        Path(fpath).unlink()

    shutil.rmtree(path, onexc=on_error)


def reset_dir(path):
    path = Path(path)
    if path.exists():
        remove_dir(path)
    path.mkdir(parents=True, exist_ok=True)
