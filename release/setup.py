#!/usr/bin/python3

from cx_Freeze import setup, Executable
import sys

sys.path.append('../')


# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["json", "os", "sys", "serial", "threading", "webbrowser",
                                  "print_stderr",
                                  "relay_boards",
                                  "relay_boards_gui",
                                  "relay_modbus",
                                  "relay_modbus_gui",
                                  "wx",
                                  "wx.adv"
                    ],
                     "excludes": [
                         "tkinter", "sqlite3"
                    ],
                     "include_files": [
                        ("../images/modbus.ico", "images/modbus.ico"),
                        ("../images/relay.ico", "images/relay.ico"),
                        ("../images/state_on.png", "images/state_on.png"),
                        ("../images/state_off.png", "images/state_off.png"),
                        ("../images/state_unknown.png", "images/state_unknown.png"),
                        ("../images/R421A08.ico", "images/R421A08.ico"),
                        ("../images/question.png", "images/question.png")
                     ],
                     "optimize": 2
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name = "modbus",
      version = "1.0.1",
      description = "8 Channel RS485 MODBUS RTU relay board type R421A08",
      options = {"build_exe": build_exe_options},
      executables = [
          Executable("../modbus.py", base=None, icon='../images/shell.ico'),
          Executable("../relay.py", base=None, icon='../images/shell.ico'),
          Executable("../modbus_gui.py", base=base, icon='../images/modbus.ico'),
          Executable("../relay_gui.py", base=base, icon='../images/relay.ico')
      ]
)
