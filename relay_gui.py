#!/usr/bin/python3
#
# MIT License
#
# Copyright (c) 2018 Erriez
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

##
# 8 Channel RS485 RTU relay board type R421A08 GUI.
#
# This is a wxPython GUI to control multiple R421A08 relay boards  by using a USB - RS485 dongle.
#
# Tested with wxPython 4.0.1 and Python 3.5 / 3.6.
#
# Source: https://github.com/Erriez/R421A08-rs485-8ch-relay-board
#

import os
import sys
import wx

import relay_boards_gui


def main():
    if len(sys.argv) > 1:
        settings_file = sys.argv[1]
    else:
        settings_file = None

    # Change directory to script directory to find relative path resources
    script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    os.chdir(script_path)

    app = wx.App()
    form = relay_boards_gui.RelayGUI(None, settings_file)
    form.SetSize(wx.Size(650, 650))
    form.SetMinSize(wx.Size(610, 620))
    form.Center()
    form.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
