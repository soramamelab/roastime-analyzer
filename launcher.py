import sys
import os
from streamlit.web import cli as stcli

if getattr(sys, 'frozen', False):
    app_script = os.path.join(sys._MEIPASS, 'app.py')
else:
    app_script = os.path.join(os.path.dirname(__file__), 'app.py')

if __name__ == '__main__':
    sys.argv = [
        "streamlit",
        "run",
        app_script,
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())
