import os
import shutil
from pathlib import Path

import pytest

OUTPUT = "output"


@pytest.fixture(scope="session", autouse=True)
def scope_session():
    # OUTPUT ディレクトリ削除
    basedir = Path(os.path.dirname(os.path.abspath(__file__)))
    output_path_name = os.path.join(basedir, OUTPUT)
    if os.path.exists(output_path_name):
        shutil.rmtree(output_path_name)
