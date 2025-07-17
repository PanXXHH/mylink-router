# MYLINK-URI是实现链接跳转的支持库

from pathlib import Path
import sys
import _private_config

from App import App

sys.argv.append("mylink://d.work/")
if __name__ == "__main__":

    with App(
        SCRIPT_DIRECTORY=Path(__file__).parent,
        config_module=_private_config,
        sys_argv=list(sys.argv),
    ) as _app:
        _app.uri()
