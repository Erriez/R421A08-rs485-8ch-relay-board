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
# MODBUS GUI.
#
# This is a wxPython application to send and receive MODBUS commands with a USB - RS485 dongle.
#
# Source: https://github.com/Erriez/R421A08-rs485-8ch-relay-board
#

import os
import sys
import wx
import wx.adv
from wx.lib.wordwrap import wordwrap
from threading import Thread, Event

import relay_modbus
from . form_modbus import frmModbus


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class ModbusGUI(frmModbus):
    def __init__(self, parent, serial_port=None):
        frmModbus.__init__(self, parent)

        # Set default serial port
        self._serial_port = serial_port

        # Set application icon
        ico_path = resource_path('images/modbus.ico')
        if os.path.exists(ico_path):
            self.SetIcon(wx.Icon(ico_path))

        # Initialize control states
        self.controls_disconnect()

        # Create MODBUS object
        self._modbus = relay_modbus.Modbus()

        # Transmit / receive frame counter
        self.frame_count = 0

        # Create MODBUS receive thread
        self._modbus_receive_thread = ModbusReceiveThread(self._modbus, self.append_log)
        self._modbus_receive_thread.daemon = True
        self._modbus_receive_thread.start()

        # Load serial ports
        self.OnBtnRefreshClick(None)

        if self._serial_port:
            # Open default serial port
            self.OnBtnConnectDisconnect()
            self.m_cmbCommand.SetFocus()
        else:
            # Set default status bar text
            self.m_statusBar.SetStatusText('Select a serial port and click Open')

    def OnWindowClose(self, event):
        if self._modbus.is_open():
            self._modbus.close()
        self.Destroy()

    def controls_connect(self):
        self.m_cmbSerialPort.Disable()
        self.m_menuItemRefreshSerialPorts.Enable(False)
        self.m_menuItemConnect.Enable(False)
        self.m_menuItemDisconnect.Enable(True)
        self.m_btnOnConnectDisconnect.SetLabelText('Disconnect')
        self.m_cmbCommand.Enable()
        self.m_btnSend.Enable()
        self.m_menuItemClearHistory.Enable(True)
        self.m_menuItemAppendCRC.Enable(True)

    def controls_disconnect(self):
        self.m_cmbSerialPort.Enable()
        self.m_menuItemRefreshSerialPorts.Enable(True)
        self.m_menuItemConnect.Enable(True)
        self.m_menuItemDisconnect.Enable(False)
        self.m_btnOnConnectDisconnect.SetLabelText('Connect')
        self.m_cmbCommand.Disable()
        self.m_btnSend.Disable()
        self.m_menuItemClearHistory.Enable(False)
        self.m_menuItemAppendCRC.Enable(False)

    def OnMenuQuit(self, event):
        """
            Close the frame, terminating the application.
        :param event:
        :return:
        """
        self.Close(True)

    def OnMenuAbout(self, event):
        """
            Display an About Dialog
        :param event:
        :return:
        """
        info = wx.adv.AboutDialogInfo()
        info.SetName('RS485 MODBUS GUI')
        info.SetVersion('v{}'.format(relay_modbus.VERSION))
        info.SetCopyright('(C) 2018 by Erriez')
        ico_path = resource_path('images/modbus.ico')
        if os.path.exists(ico_path):
            info.SetIcon(wx.Icon(ico_path))
        info.SetDescription(wordwrap(
            "This is an example application to monitor and send MODBUS commands using wxPython!",
            350, wx.ClientDC(self)))
        info.SetWebSite("https://github.com/Erriez/R421A08-rs485-8ch-relay-board",
                        "Source & Documentation")
        info.AddDeveloper('Erriez')
        info.SetLicense(wordwrap("MIT License: Completely and totally open source!", 500,
                                 wx.ClientDC(self)))
        # Then we call wx.AboutBox giving it that info object
        wx.adv.AboutBox(info)

    def OnBtnRefreshClick(self, event=None):
        """
            Button refresh serial ports
        :param event:
        :return:
        """
        serial_ports = relay_modbus.get_serial_ports()
        self.m_cmbSerialPort.Clear()
        for serial_port in serial_ports:
            self.m_cmbSerialPort.Append(serial_port)

        # Set default serial port
        if self._serial_port:
            self.m_cmbSerialPort.SetValue(self._serial_port)

    def OnBtnConnectDisconnect(self, event=None):
        """
            Button open serial port
        :param event:
        :return:
        """
        if self._modbus.is_open():
            self._modbus_receive_thread.disable()
            self._modbus.close()
            self.controls_disconnect()
            self.m_statusBar.SetStatusText('Serial port closed')
        else:
            serial_port = self.m_cmbSerialPort.GetStringSelection()

            if not serial_port:
                self.m_statusBar.SetStatusText('Please select a serial port')
                return

            self._modbus.serial_port = serial_port
            try:
                self._modbus.open()
            except relay_modbus.SerialOpenException as err:
                self.m_statusBar.SetStatusText(str(err))
                wx.MessageBox(str(err), 'Open serial port',
                              wx.OK | wx.ICON_STOP)
                return

            self.controls_connect()
            self._modbus_receive_thread.enable()
            self.m_statusBar.SetStatusText('Serial port open')

    def OnMenuCopyLogClipboard(self, event):
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.m_txtLog.GetValue()))
            wx.TheClipboard.Close()
            self.m_statusBar.SetStatusText('Log copied to clipboard.')
        else:
            self.m_statusBar.SetStatusText('Error: Failed to open clipboard')

    def OnMenuClearLog(self, event):
        self.m_txtLog.Clear()
        self.m_statusBar.SetStatusText('Log cleared.')

    def OnMenuClearHistory(self, event):
        self.m_cmbCommand.Clear()
        self.m_statusBar.SetStatusText('History cleared.')

    def OnMenuAppendCRC(self, event):
        if self.m_menuItemAppendCRC.IsChecked():
            self.m_statusBar.SetStatusText('Append CRC to frame enabled.')
        else:
            self.m_statusBar.SetStatusText('Append CRC to frame disabled.')

    def OnCommandText(self, event):
        self.m_statusBar.SetStatusText('Click send or press [ENTER] to transmit')

    def OnCommandEnter(self, event):
        """
            Enter key in command combo box
        :param event:
        :return:
        """
        self.OnBtnSend(None)

    def OnBtnSend(self, event):
        """
            Button send
        :param event:
        :return:
        """
        command = self.m_cmbCommand.GetValue()
        if not command:
            return

        if self.m_cmbCommand.FindString(command) == wx.NOT_FOUND:
            self.m_cmbCommand.Insert(command, 0)

        self.m_statusBar.SetStatusText('TX: {}...'.format(command))

        try:
            # Replace characters, for example:
            #   ':010600010100D99A' -> '010600010100D99A'
            #   '0x01, 0x06, 0x00, 0x01, 0x01, 0x00, 0xD9, 0x9A' -> '01 06 00 01 01 00 D9 9A'
            for c in ['0x', ':', ',', ' ']:
                command = command.replace(c, '')

            # Insert space every 2 characters, for example:
            #   '010600010100D99A' -> '01 06 00 01 01 00 D9 9A'
            command = ' '.join(a + b for a, b in zip(command[::2], command[1::2]))

            # Split data in ints, for example:
            #   [0x01, 0x06, 0x00, 0x01, 0x01, 0x00, 0xD9, 0x9A]
            tx_data = [int(i, 16) for i in command.split(' ')]
        except ValueError:
            self.m_statusBar.SetStatusText('Incorrect send argument.'.format(command))
            return

        # Send and receive MODBUS frame
        self._modbus.transfer_begin()
        try:
            self._modbus.transfer(tx_data, self.m_menuItemAppendCRC.IsChecked(), rx_length=0)
        except relay_modbus.TransferException as err:
            self.append_log(tx_frame=self._modbus.last_tx_frame, rx_frame=str(err))
            self._modbus.transfer_end()
            self.m_statusBar.SetStatusText(str(err))
            return

        self.append_log(tx_frame=self._modbus.last_tx_frame, rx_frame=self._modbus.last_rx_frame)

        self._modbus.transfer_end()
        self.m_statusBar.SetStatusText('Transmit completed.')

    def OnLogKeyDown(self, event):
        ctrl_key = event.ControlDown()
        alt_key = event.AltDown()
        shift_key = event.ShiftDown()
        key_code = event.GetKeyCode()

        # print(ctrl_key, alt_key, shift_key, keycode)

        # Add keyboard shortcuts:
        #   CTRL + DEL: Clear textbox
        #   CTRL + A:   Select all
        if ctrl_key and not alt_key and not shift_key and key_code == wx.WXK_DELETE:
            self.m_txtLog.Clear()
        elif 27 < key_code < 256:
            if ctrl_key and not alt_key and not shift_key and chr(key_code) == 'A':
                self.m_txtLog.SelectAll()

        # Handle other keyboard shortcuts
        event.Skip()

    def append_log(self, tx_frame=None, rx_frame=None):
        self.frame_count += 1
        if self.m_txtLog.GetValue():
            self.m_txtLog.AppendText('\n\n')
        if tx_frame:
            self.m_txtLog.AppendText('{:04d} {}'.format(self.frame_count, tx_frame))
        if tx_frame and rx_frame:
            self.m_txtLog.AppendText('\n')
        if rx_frame:
            self.m_txtLog.AppendText('{:04d} {}'.format(self.frame_count, rx_frame))


class ModbusReceiveThread(Thread):
    def __init__(self, modbus, append_log):
        """
            MODBUS receive thread
        :param modbus:
        :type modbus: relay_modbus.Modbus
        :param append_log:
        """
        Thread.__init__(self)
        self._stop_event = Event()
        self._modbus = modbus
        self._append_log = append_log
        self._enabled = False

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def cancel(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.wait(0.2):
            if self._enabled:
                self._modbus.transfer_begin()
                try:
                    rx_data = self._modbus.receive(0)
                except relay_modbus.TransferException:
                    rx_data = None

                if rx_data:
                    self._append_log(rx_frame=self._modbus.last_rx_frame)
                self._modbus.transfer_end()
