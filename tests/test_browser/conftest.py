import os.path
import sys

import pytest

sys.path.append(os.getcwd())

from src.browser import VirtualBrowser


@pytest.fixture()
def virtual_browser():
    virtual_browser_instance = VirtualBrowser(user_id="11111", path_file='D:/')
    return virtual_browser_instance
