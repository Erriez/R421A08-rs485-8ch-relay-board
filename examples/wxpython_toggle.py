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
# This is a wxPython GUI example to control a single R421A08 relay board with a USB - RS485
# dongle.
#
# Source: https://github.com/Erriez/R421A08-rs485-8ch-relay-board
#

import os
import sys
import wx
import wx.adv

# Add system path to find relay_ Python packages
sys.path.append('.')
sys.path.append('..')

import relay_modbus
import relay_boards


# Required: Configure serial port, for example:
#   On Windows: 'COMx'
#   On Linux:   '/dev/ttyUSB0'
SERIAL_PORT = 'COM3'

# Default relay board address (DIP switch 1 ON, others OFF)
ADDRESS = 1

# Path to window icon
ICO_PATH = '../images/relay.ico'


class RelayFrame(wx.Frame):
    def __init__(self, parent, serial_port, address):
        # Create frame
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u'GUI example', pos=wx.DefaultPosition,
                          size=wx.Size(275, 280), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        # Define variables
        self.m_relay_modbus = None
        self.m_relay_board = None
        self.m_statusBar = None

        # Create modbus and relay object
        self.CreateObjects(serial_port, address)

        # Create window
        self.CreateWindow(parent)

    def CreateObjects(self, serial_port, address):
        # Check argument types
        assert type(serial_port) == str
        assert type(address) == int

        # Create MODBUS object and open serial port
        self.m_relay_modbus = relay_modbus.Modbus(serial_port)
        try:
            self.m_relay_modbus.open()
        except relay_modbus.SerialOpenException as err:
            wx.MessageBox(str(err), u'Failure', style=wx.OK | wx.ICON_STOP)
            sys.exit(1)

        # Create relay board object
        self.m_relay_board = relay_boards.R421A08(self.m_relay_modbus)
        if address < 0 or address >= self.m_relay_board.num_addresses:
            wx.MessageBox(u'Invalid address {}'.format(address), u'Failure',
                          style=wx.OK | wx.ICON_STOP)
            sys.exit(1)
        self.m_relay_board.address = address

        # Set window title
        self.SetTitle(u'{} address {}'.format(self.m_relay_modbus.serial_port,
                                              self.m_relay_board.address))

    def CreateWindow(self, parent):
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetMinSize(wx.Size(250, 250))
        self.SetBackgroundColour(wx.Colour(240, 240, 240))
        if os.path.exists(ICO_PATH):
            self.SetIcon(wx.Icon(ICO_PATH))

        self.CreateMenuBar()
        self.CreateRelayButtons()
        self.CreateStatusbar()

        self.Layout()
        self.Centre(wx.BOTH)

    def CreateMenuBar(self):
        # Create menu
        m_menubar = wx.MenuBar(0)

        # File menu
        m_menuFile = wx.Menu()
        m_menuItemQuit = wx.MenuItem(m_menuFile, wx.ID_ANY, u'&Quit' + u'\t' + u'Ctrl+Q',
                                     wx.EmptyString, wx.ITEM_NORMAL)
        m_menuFile.Append(m_menuItemQuit)
        m_menubar.Append(m_menuFile, u'&File')

        # About menu
        m_menuAbout = wx.Menu()
        m_menuItemAbout = wx.MenuItem(m_menuAbout, wx.ID_ANY, u'&About' + u'\t' + u'Shift+?',
                                      wx.EmptyString, wx.ITEM_NORMAL)
        m_menuAbout.Append(m_menuItemAbout)
        m_menubar.Append(m_menuAbout, u'&Help')

        # Set menu
        self.SetMenuBar(m_menubar)

        self.Bind(wx.EVT_MENU, self.OnMenuQuit, id=m_menuItemQuit.GetId())
        self.Bind(wx.EVT_MENU, self.OnMenuAbout, id=m_menuItemAbout.GetId())

    def CreateRelayButtons(self):
        gSizer = wx.GridSizer(0, 2, 0, 0)

        # Create button 'all on'
        m_btnAllOn = wx.Button(self, 9, u'All on', wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer.Add(m_btnAllOn, 0,
                   wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        m_btnAllOn.Bind(wx.EVT_BUTTON, self.OnBtnAllOnClick)

        # Create button 'all off'
        m_btnAllOff = wx.Button(self, 10, u'All off', wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer.Add(m_btnAllOff, 0,
                   wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        m_btnAllOff.Bind(wx.EVT_BUTTON, self.OnBtnAllOffClick)

        # Create toggle buttons
        for relay in range(self.m_relay_board.num_relays):
            # Convert relay numbers to grid: First column 0..3, second column: 4..7
            if relay & 1:
                relay = 4 + int((relay - 1) / 2)
            else:
                relay = int(relay / 2)

            button_text = u'Toggle ' + str(relay + 1)
            m_btnToggleRelay = wx.Button(self, relay, button_text,
                                         wx.DefaultPosition, wx.DefaultSize, 0)
            gSizer.Add(m_btnToggleRelay, 0,
                       wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
            m_btnToggleRelay.Bind(wx.EVT_BUTTON, self.OnBtnToggleClick)

        self.SetSizer(gSizer)

    def CreateStatusbar(self):
        self.m_statusBar = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)
        self.m_statusBar.SetStatusText(u'Click on a button')

    def OnMenuQuit(self, event):
        self.Close()

    def OnMenuAbout(self, event):
        info = wx.adv.AboutDialogInfo()
        info.SetName('Relay example GUI')
        if os.path.exists(ICO_PATH):
            info.SetIcon(wx.Icon(ICO_PATH))
        info.SetVersion('v1.0')
        info.SetCopyright('(C) 2018 by Erriez')
        info.SetDescription('Relay example with wxPython {}'.format(wx.version()))
        info.SetWebSite('https://github.com/Erriez/R421A08-rs485-8ch-relay-board',
                        'Source & Documentation')
        info.AddDeveloper('Erriez')
        info.SetLicense('MIT License: Completely and totally open source!')
        wx.adv.AboutBox(info)

    def OnBtnAllOnClick(self, event):
        try:
            retval = self.m_relay_board.on_all()
        except relay_modbus.TransferException as err:
            self.m_statusBar.SetStatusText(u'Relays on - {}'.format(str(err)))
        else:
            if retval:
                self.m_statusBar.SetStatusText('All relays on.')
            else:
                self.m_statusBar.SetStatusText(u'Error: Could not turn on relays!')

    def OnBtnAllOffClick(self, event):
        try:
            retval = self.m_relay_board.off_all()
        except relay_modbus.TransferException as err:
            self.m_statusBar.SetStatusText(u'Relays off - {}'.format(str(err)))
        else:
            if retval:
                self.m_statusBar.SetStatusText('All relays off.')
            else:
                self.m_statusBar.SetStatusText(u'Error: Could not turn off relays!')

    def OnBtnToggleClick(self, event):
        relay = event.GetId() + 1

        try:
            retval = self.m_relay_board.toggle(relay)
        except relay_modbus.TransferException as err:
            self.m_statusBar.SetStatusText(u'Relay {} - {}'.format(relay, str(err)))
        else:
            if retval:
                self.m_statusBar.SetStatusText('Relay {} toggled.'.format(relay))
            else:
                self.m_statusBar.SetStatusText(u'Error: Could not toggle relay {}!'.format(relay))


def main():
    if len(sys.argv) == 3:
        serial_port = str(sys.argv[1])
        address = int(sys.argv[2])
    else:
        serial_port = SERIAL_PORT
        address = ADDRESS

    app = wx.App()
    form = RelayFrame(None, serial_port, address)
    form.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
