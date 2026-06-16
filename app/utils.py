import os
import shutil
import stat


def remove_dir(path):
    def on_error(_func, fpath, _exc_info):
        os.chmod(fpath, stat.S_IWRITE)
        os.unlink(fpath)

    shutil.rmtree(path, onexc=on_error)


def reset_dir(path):
    if os.path.exists(path):
        remove_dir(path)
    os.makedirs(path, exist_ok=True)
