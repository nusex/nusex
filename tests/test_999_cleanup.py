import os
import shutil


def test_cleanup():
    # Cleans up after the tests are complete.
    os.chdir("..")
    shutil.rmtree("./awesome_pkg")
    assert not os.path.isdir("./awesome_pkg")
