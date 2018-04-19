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

import json
import os
import sys
import webbrowser
import wx
import wx.adv
from wx.lib.wordwrap import wordwrap

import relay_modbus
import relay_boards

import relay_modbus_gui

from print_stderr import print_stderr

from . dialog_question import dlgQuestion
from . form_relay import frmRelays

SOURCE_URL = 'https://github.com/Erriez/R421A08-rs485-8ch-relay-board'


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# --------------------------------------------------------------------------------------------------
# Relay main form
# --------------------------------------------------------------------------------------------------
class RelayGUI(frmRelays):
    def __init__(self, parent, settings_file=None):
        frmRelays.__init__(self, parent)

        # Protect events when closing window
        self.closing_window = False

        # Set window size and minimum window size
        self.SetSize(wx.Size(580, 650))
        self.SetMinSize(wx.Size(580, 650))

        # Set application icon
        ico_path = resource_path('images/relay.ico')
        if ico_path:
            self.m_relay_icon = wx.Icon(ico_path)
            self.SetIcon(self.m_relay_icon)
        self.SetTitle('R421A08 Relay Control')

        # Create taskbar icon
        self.m_taskbar_icon = CustomTaskBarIcon(self, self.m_relay_icon)

        # Create MODBUS object
        self.m_relay_modbus = relay_modbus.Modbus()

        # Refresh serial ports
        self.OnRefreshPortsClick(None)
        self.m_menuItemDisconnect.Enable(False)

        # Load settings from file when available
        self.m_settings_file = settings_file
        self.m_panel_changed = False
        if self.m_settings_file and os.path.exists(self.m_settings_file):
            self.load_settings(self.m_settings_file)
        else:
            # Create default relay panel
            self.new_relay_panel()

            # Disable controls on relay panel
            self.disable_relay_panels()

            # Disable relay menu
            self.disable_relay_menu()

        self.m_notebook.Bind(wx.EVT_CONTEXT_MENU, self.OnContext)

    def OnWindowClose(self, event):
        self.closing_window = True

        # Ask to save changes
        if self.ask_save_changes() == wx.ID_CANCEL:
            return

        # Disconnect serial port
        if self.m_relay_modbus.is_open():
            self.m_relay_modbus.close()

        # Destroy taskbar icon
        self.m_taskbar_icon.RemoveIcon()
        self.m_taskbar_icon.Destroy()

        self.Destroy()

    def OnWindowIconize(self, event):
        if self.IsIconized():
            if sys.platform == 'win32':
                # Iconize in Ubuntu is broken with wxPython 4.0.1, so hide window in Windows only.
                self.Hide()

    def OnContext(self, event):
        popup_menu = wx.Menu()

        m_menuItemRenameBoard = wx.MenuItem(popup_menu, wx.ID_ANY,
                                            u"Rename board (F2)", wx.EmptyString,
                                            wx.ITEM_NORMAL)
        popup_menu.Append(m_menuItemRenameBoard)

        popup_menu.AppendSeparator()

        m_menuItemAddBoard = wx.MenuItem(popup_menu, wx.ID_ANY,
                                         u"Add board (Ctrl+B)", wx.EmptyString,
                                         wx.ITEM_NORMAL)
        popup_menu.Append(m_menuItemAddBoard)

        m_menuItemRemoveBoard = wx.MenuItem(popup_menu, wx.ID_ANY,
                                            u"Remove board (Ctrl+D)", wx.EmptyString,
                                            wx.ITEM_NORMAL)
        popup_menu.Append(m_menuItemRemoveBoard)

        self.Bind(wx.EVT_MENU, self.OnBoardRenameClick, id=m_menuItemRenameBoard.GetId())
        self.Bind(wx.EVT_MENU, self.OnBoardAddClick, id=m_menuItemAddBoard.GetId())
        self.Bind(wx.EVT_MENU, self.OnBoardRemoveClick, id=m_menuItemRemoveBoard.GetId())

        self.PopupMenu(popup_menu)

        popup_menu.Destroy()

    def new_relay_panel(self):
        # Create new relay panel
        m_panel = RelayPanel(self.m_notebook, self.m_notebook.GetPageCount() + 1)
        m_panel.SetBackgroundColour(wx.Colour(248, 248, 248))

        # Insert panel
        self.m_notebook.AddPage(m_panel,
                                u"Relay board #{}".format(self.m_notebook.GetPageCount() + 1),
                                False)

        # Set focus on new relay panel
        self.m_notebook.SetSelection(self.m_notebook.GetPageCount() - 1)

        # Update panel status
        self.update_controls()

        # Update status bar
        self.m_statusBar.SetStatusText('New relay board created.')

    def remove_all_relay_panels(self):
        while self.m_notebook.GetRowCount() > 1:
            self.m_notebook.RemovePage(0)
        self.m_statusBar.SetStatusText('All relay board removed.')

    def disable_relay_panels(self):
        for page_id in range(self.m_notebook.GetPageCount()):
            page = self.m_notebook.GetPage(page_id)
            if page:
                page.set_relay_status_icons_unknown()
                page.disable_buttons()

    def enable_relay_panels(self):
        for page_id in range(self.m_notebook.GetPageCount()):
            page = self.m_notebook.GetPage(page_id)
            if page:
                page.enable_buttons()

    def update_controls(self):
        if self.m_relay_modbus.is_open():
            self.m_btnConnectDisconnect.SetLabel('Disconnect')
            self.m_cmbSerialPort.Disable()
            self.enable_relay_panels()
            self.m_menuItemRefreshPorts.Enable(False)
            self.m_menuItemConnect.Enable(False)
            self.m_menuItemDisconnect.Enable(True)
            self.enable_relay_menu()
            self.OnRefreshAllRelaysClick()
        else:
            self.m_btnConnectDisconnect.SetLabel('Connect')
            self.m_cmbSerialPort.Enable()
            self.disable_relay_panels()
            self.m_menuItemRefreshPorts.Enable(True)
            self.m_menuItemConnect.Enable(True)
            self.m_menuItemDisconnect.Enable(False)
            self.disable_relay_menu()

    def disable_relay_menu(self):
        # Disable top-level menu (Works on Windows only):
        self.m_menubar.EnableTop(3, False)
        menu = self.m_menubar.GetMenus()[3][0]
        for menu_item in menu.MenuItems:
            menu_item.Enable(False)

    def enable_relay_menu(self):
        self.m_menubar.EnableTop(3, True)
        menu = self.m_menubar.GetMenus()[3][0]
        for menu_item in menu.MenuItems:
            menu_item.Enable(True)

    def OnNotebookPageChanged(self, event):
        if not self.closing_window:
            self.update_controls()

    # ----------------------------------------------------------------------------------------------
    # Serial control Events
    def OnConnectDisconnectClick(self, event):
        if self.m_relay_modbus.is_open():
            self.disconnect()
        else:
            self.connect()

    def disconnect(self):
        self.m_relay_modbus.close()
        self.m_statusBar.SetStatusText('Serial port closed.')
        self.update_controls()

    def connect(self):
        serial_port = self.m_cmbSerialPort.GetStringSelection()
        self.m_relay_modbus.serial_port = serial_port
        try:
            self.m_relay_modbus.open()
        except relay_modbus.SerialOpenException as err:
            self.m_statusBar.SetStatusText(str(err))
        else:
            self.m_statusBar.SetStatusText('Serial port {} opened.'.format(serial_port))
        self.update_controls()

    # ----------------------------------------------------------------------------------------------
    # Menu Events
    def OnNewClick(self, event=None):
        if self.ask_save_changes() == wx.ID_CANCEL:
            return

        self.disconnect()
        while self.m_notebook.GetPageCount():
            self.m_notebook.RemovePage(0)
        self.OnBoardAddClick(None)
        self.m_panel_changed = False
        self.m_settings_file = None
        self.m_statusBar.SetStatusText('New project created.')

    def OnOpenClick(self, event=None):
        if self.ask_save_changes() == wx.ID_CANCEL:
            return

        dlg = wx.FileDialog(self, 'Load settings...', os.getcwd(), '', '*.relay', style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.disconnect()
            while self.m_notebook.GetPageCount():
                self.m_notebook.RemovePage(0)
            self.m_settings_file = dlg.GetPath()
            self.load_settings(self.m_settings_file)
        dlg.Destroy()

    def OnSaveClick(self, event=None):
        if self.m_settings_file:
            self.save_settings(self.m_settings_file)
        else:
            self.OnSaveAsClick(event)

    def OnSaveAsClick(self, event=None):
        dlg = wx.FileDialog(self, 'Save settings as...', os.getcwd(), '', '*.relay',
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.m_settings_file = dlg.GetPath()
            if not self.m_settings_file.endswith('.relay'):
                self.m_settings_file += '.relay'
            self.save_settings(self.m_settings_file)
        dlg.Destroy()

    def ask_save_changes(self):
        if self.m_panel_changed:
            dlg = QuestionDialog('Current project has been modified...\n'
                                 'Do you want to save changes?',
                                 'Save project',
                                 self)
            answer = dlg.ShowModal()
            if answer == wx.ID_YES:
                self.OnSaveClick()
            return answer
        else:
            return wx.ID_NO

    def load_settings(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as fp:
                settings = json.load(fp)
                if 'relay_boards' in settings:
                    relay_boards_ = settings['relay_boards']

                    for relay_board in relay_boards_:
                        board = relay_boards_[relay_board]

                        self.new_relay_panel()

                        page_id = self.m_notebook.GetPageCount() - 1

                        if 'board_name' in board:
                            board_name = board['board_name']
                            self.m_notebook.SetPageText(page_id, board_name)

                        page = self.m_notebook.GetPage(page_id)

                        if 'board_address' in board:
                            address = board['board_address']
                            page.m_spinAddress.SetValue(address)

                        if 'board_relays' in board:
                            relays = board['board_relays']
                            for relay in relays:
                                if 'name' in relays[relay]:
                                    relay_name = relays[relay]['name']
                                    page.m_txtName[int(relay)].SetValue(relay_name)

                                if 'pulse' in relays[relay]:
                                    relay_pulse = relays[relay]['pulse']
                                    page.m_spnDelay[int(relay)].SetValue(relay_pulse)

                if 'current_board' in settings:
                    current_page = settings['current_board']
                    self.m_notebook.SetSelection(int(current_page))

                if 'serial_port' in settings:
                    serial_port = settings['serial_port']
                    if serial_port in self.m_cmbSerialPort.GetStrings():
                        self.m_cmbSerialPort.SetStringSelection(serial_port)

                        if 'serial_port_open' in settings:
                            if bool(settings['serial_port_open']) == True:
                                try:
                                    self.connect()
                                except relay_modbus.SerialOpenException:
                                    pass
                        else:
                            self.disconnect()

            self.m_panel_changed = False
            self.m_statusBar.SetStatusText('Settings loaded from file.')
        else:
            self.m_statusBar.SetStatusText('Error: File does not exist.')

    def save_settings(self, file_path):
        settings = {
            'source_url': SOURCE_URL,
            'serial_port': self.m_relay_modbus.serial_port,
            'serial_port_open': self.m_relay_modbus.is_open(),
            'relay_boards': {},
            'current_board': self.m_notebook.GetSelection()
        }

        for page_id in range(self.m_notebook.GetPageCount()):
            page = self.m_notebook.GetPage(page_id)

            relays = {}
            for relay in range(len(page.m_txtName)):
                relays[relay] = {
                    'name': page.m_txtName[relay].GetValue(),
                    'pulse': page.m_spnDelay[relay].GetValue()
                }

            settings['relay_boards'][page_id] = {
                'board_name': self.m_notebook.GetPageText(page_id),
                'board_address': page.m_spinAddress.GetValue(),
                'board_relays': relays
            }

        with open(file_path, 'w') as fp:
            json.dump(settings, fp, sort_keys=True, indent=4)

        if os.path.exists(file_path):
            self.m_panel_changed = False
            self.m_statusBar.SetStatusText('Settings saved to file.')
        else:
            self.m_statusBar.SetStatusText('Error: Could not save settings.')

    def OnQuitClick(self, event=None):
        # Close window
        self.Close()

    def OnRefreshPortsClick(self, event=None):
        self.m_cmbSerialPort.Clear()
        for serial_port in relay_modbus.get_serial_ports():
            self.m_cmbSerialPort.Append(serial_port)
        if self.m_cmbSerialPort.Count:
            self.m_cmbSerialPort.Select(0)
        self.m_statusBar.SetStatusText('Serial ports refreshed.')

    def OnConnectClick(self, event=None):
        self.OnConnectDisconnectClick(None)

    def OnDisconnectClick(self, event=None):
        self.OnConnectDisconnectClick(None)

    def OnMonitorClick(self, event=None):
        dlg = relay_modbus_gui.ModbusGUI(self)
        dlg.Show()
        self.m_statusBar.SetStatusText('MODBUS monitor opened.')

    def OnBoardRenameClick(self, event=None):
        current_tab = self.m_notebook.GetSelection()

        dlg = wx.TextEntryDialog(self, 'Relay board name:', 'Set relay board name')
        dlg.SetValue(self.m_notebook.GetPageText(current_tab))
        if dlg.ShowModal() == wx.ID_OK:
            self.m_notebook.SetPageText(current_tab, dlg.GetValue())
            self.m_panel_changed = True
            self.m_statusBar.SetStatusText('Relay board renamed.')
        else:
            self.m_statusBar.SetStatusText('Relay board not renamed.')
        dlg.Destroy()

    def OnBoardAddClick(self, event=None):
        self.new_relay_panel()
        self.m_panel_changed = True

    def OnBoardRemoveClick(self, event=None):
        if self.m_notebook.GetPageCount() > 1:
            current_tab = self.m_notebook.GetSelection()
            if current_tab != wx.NOT_FOUND:
                self.m_notebook.RemovePage(current_tab)
                self.m_panel_changed = True
            self.m_statusBar.SetStatusText('Relay board removed.')
        else:
            self.m_statusBar.SetStatusText('Cannot remove board.')

    def OnAllRelaysOnClick(self, event=None):
        if self.m_relay_modbus.is_open():
            page = self.m_notebook.GetCurrentPage()
            page.send_all_relays_command('on_all')
        else:
            self.m_statusBar.SetStatusText('Error: Serial port disconnected.')

    def OnAllRelaysOffClick(self, event=None):
        if self.m_relay_modbus.is_open():
            page = self.m_notebook.GetCurrentPage()
            page.send_all_relays_command('off_all')
        else:
            self.m_statusBar.SetStatusText('Error: Serial port disconnected.')

    def OnRelayToggleClick(self, event=None):
        if self.m_relay_modbus.is_open():
            page = self.m_notebook.GetCurrentPage()
            page.send_relay_command('toggle', event.GetId())
        else:
            self.m_statusBar.SetStatusText('Error: Serial port disconnected.')

    def OnRefreshAllRelaysClick(self, event=None):
        if self.m_relay_modbus.is_open():
            page = self.m_notebook.GetCurrentPage()
            page.refresh_all_relays()
        else:
            self.m_statusBar.SetStatusText('Error: Serial port disconnected.')

    def OnMenuHelp(self, event=None):
        # Open Github Wiki page in new browser tab
        webbrowser.open(SOURCE_URL + '/wiki', new=2)

    def OnMenuSourceOnGitHub(self, event=None):
        # Open Github main page in new browser tab
        webbrowser.open(SOURCE_URL, new=2)

    def OnMenuUpdates(self, event=None):
        # Open Github Releases in new browser tab
        webbrowser.open(SOURCE_URL + '/releases', new=2)

    def OnAboutClick(self, event=None):
        info = wx.adv.AboutDialogInfo()
        info.SetName('RS485 MODBUS GUI')
        info.SetVersion('v{}'.format(relay_boards.VERSION))
        info.SetCopyright('(C) 2018 by Erriez')
        ico_path = resource_path('images/R421A08.ico')
        if os.path.exists(ico_path):
            info.SetIcon(wx.Icon(ico_path))
        info.SetDescription(wordwrap(
            "This is an example application to control a R421A08 relay board using wxPython!",
            350, wx.ClientDC(self)))
        info.SetWebSite(SOURCE_URL,
                        "Source & Documentation")
        info.AddDeveloper('Erriez')
        info.SetLicense(wordwrap("MIT License: Completely and totally open source!", 500,
                                 wx.ClientDC(self)))
        wx.adv.AboutBox(info)


# --------------------------------------------------------------------------------------------------
# Relay panel
# --------------------------------------------------------------------------------------------------
class RelayPanel(wx.Panel):
    def __init__(self, parent, board_address):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                          size=wx.Size(600, 300), style=wx.TAB_TRAVERSAL)

        # ------------------------------------------------------------------------------------------
        self.m_status_bar = parent.GetTopLevelParent().m_statusBar
        self.m_relay_modbus = parent.GetTopLevelParent().m_relay_modbus
        self.m_relay_board = relay_boards.R421A08(self.m_relay_modbus)

        # ------------------------------------------------------------------------------------------
        # Load resources
        self.m_relay_status_on = None
        self.m_relay_status_off = None
        self.m_relay_status_unknown = None

        img_list = [
            resource_path('images/state_on.png'),
            resource_path('images/state_off.png'),
            resource_path('images/state_unknown.png'),
         ]

        all_found = True
        for img in img_list:
            if not os.path.exists(img):
                all_found = False
                break

        if all_found:
            self.m_relay_status_on = wx.Icon(resource_path('images/state_on.png'))
            self.m_relay_status_off = wx.Icon(resource_path('images/state_off.png'))
            self.m_relay_status_unknown = wx.Icon(resource_path('images/state_unknown.png'))

        # ------------------------------------------------------------------------------------------
        # Form sizer
        fgSizerForm = wx.FlexGridSizer(0, 1, 0, 0)
        fgSizerForm.AddGrowableRow(1)
        fgSizerForm.AddGrowableCol(0)
        fgSizerForm.SetFlexibleDirection(wx.BOTH)
        fgSizerForm.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # ------------------------------------------------------------------------------------------
        # Relay board static box sizer
        sbSizerAddress = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Relay board"),
                                           wx.HORIZONTAL)

        self.m_txtAddress = wx.StaticText(sbSizerAddress.GetStaticBox(), wx.ID_ANY, u"Address:",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_txtAddress.Wrap(-1)
        sbSizerAddress.Add(self.m_txtAddress, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.m_spinAddress = wx.SpinCtrl(sbSizerAddress.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                         wx.DefaultPosition, wx.Size(100, -1), wx.SP_ARROW_KEYS,
                                         0, 63, board_address)
        sbSizerAddress.Add(self.m_spinAddress, 0, wx.ALL, 5)

        fgSizerForm.Add(sbSizerAddress, 1, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 5)

        # ------------------------------------------------------------------------------------------
        # Relays static box sizer
        sbSizerRelays = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"Relays"), wx.VERTICAL)

        fgSizer = wx.FlexGridSizer(0, 7, 0, 0)
        fgSizer.AddGrowableCol(1)
        fgSizer.SetFlexibleDirection(wx.BOTH)
        fgSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_bmpStatus = []
        self.m_txtName = []
        self.m_btnRelayOn = []
        self.m_btnRelayOff = []
        self.m_lblDelay = []
        self.m_spnDelay = []
        self.m_btnPulse = []
        self.m_timer = []
        for relay in range(0, self.m_relay_board.num_relays):
            fgSizer.AddGrowableRow(relay)
            self.add_relay(relay, sbSizerRelays, fgSizer)

        # ------------------------------------------------------------------------------------------
        # Set sizers
        sbSizerRelays.Add(fgSizer, 1, wx.EXPAND, 5)
        fgSizerForm.Add(sbSizerRelays, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(fgSizerForm)
        self.Layout()

    def add_relay(self, relay, sbSizerRelays, fgSizer):
        # ------------------------------------------------------------------------------------------
        m_bmpStatus = wx.StaticBitmap(sbSizerRelays.GetStaticBox(),
                                      relay + 1, wx.NullBitmap,
                                      wx.DefaultPosition, wx.DefaultSize, 0)
        if self.m_relay_status_unknown:
            m_bmpStatus.SetIcon(self.m_relay_status_unknown)
        m_bmpStatus.SetToolTip('Click: Toggle relay.\n'
                               'Ctrl+Click: All on.\n'
                               'Ctrl+Shift+Click: All off')
        fgSizer.Add(m_bmpStatus, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # ------------------------------------------------------------------------------------------
        bSizerName = wx.BoxSizer(wx.VERTICAL)
        bSizerName.Add((0, 0), 1, wx.EXPAND, 5)

        m_txtName = wx.TextCtrl(sbSizerRelays.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                wx.DefaultPosition, wx.DefaultSize, 0)
        m_txtName.SetMaxLength(64)
        m_txtName.SetValue('Relay {}'.format(relay + 1))
        bSizerName.Add(m_txtName, 0, wx.ALL | wx.EXPAND, 5)

        bSizerName.Add((0, 0), 1, wx.EXPAND, 5)
        fgSizer.Add(bSizerName, 1, wx.EXPAND, 5)

        # ------------------------------------------------------------------------------------------
        m_btnRelayOn = wx.Button(sbSizerRelays.GetStaticBox(), relay + 1, u"On",
                                 wx.DefaultPosition, wx.Size(70, -1), 0)
        fgSizer.Add(m_btnRelayOn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # ------------------------------------------------------------------------------------------
        m_btnRelayOff = wx.Button(sbSizerRelays.GetStaticBox(), relay + 1, u"Off",
                                  wx.DefaultPosition, wx.Size(70, -1), 0)
        fgSizer.Add(m_btnRelayOff, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # ------------------------------------------------------------------------------------------
        m_lblDelay = wx.StaticText(sbSizerRelays.GetStaticBox(), wx.ID_ANY, u"Delay:",
                                   wx.DefaultPosition, wx.DefaultSize, 0)
        m_lblDelay.Wrap(-1)
        fgSizer.Add(m_lblDelay, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # ------------------------------------------------------------------------------------------
        m_spnDelay = wx.SpinCtrl(sbSizerRelays.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                 wx.DefaultPosition, wx.Size(100, -1), wx.SP_ARROW_KEYS,
                                 1, 255, 1)
        fgSizer.Add(m_spnDelay, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # ------------------------------------------------------------------------------------------
        m_btnPulse = wx.Button(sbSizerRelays.GetStaticBox(), relay + 1, u"Pulse",
                               wx.DefaultPosition, wx.Size(70, -1), 0)
        fgSizer.Add(m_btnPulse, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # ------------------------------------------------------------------------------------------
        # Connect Events
        m_bmpStatus.Bind(wx.EVT_LEFT_DOWN, self.OnBmpClick)
        m_btnRelayOn.Bind(wx.EVT_BUTTON, self.OnBtnRelayOnClick)
        m_btnRelayOff.Bind(wx.EVT_BUTTON, self.OnBtnRelayOffClick)
        m_btnPulse.Bind(wx.EVT_BUTTON, self.OnBtnRelayPulse)

        self.m_bmpStatus.append(m_bmpStatus)
        self.m_txtName.append(m_txtName)
        self.m_btnRelayOn.append(m_btnRelayOn)
        self.m_btnRelayOff.append(m_btnRelayOff)
        self.m_lblDelay.append(m_lblDelay)
        self.m_spnDelay.append(m_spnDelay)
        self.m_btnPulse.append(m_btnPulse)
        self.m_timer.append(wx.Timer(self, id=relay + 1))

    def disable_buttons(self):
        for relay in range(self.m_relay_board.num_relays):
            self.m_bmpStatus[relay].Disable()
            self.m_btnRelayOn[relay].Disable()
            self.m_btnRelayOff[relay].Disable()
            self.m_btnPulse[relay].Disable()

    def enable_buttons(self):
        for relay in range(self.m_relay_board.num_relays):
            self.m_bmpStatus[relay].Enable()
            self.m_btnRelayOn[relay].Enable()
            self.m_btnRelayOff[relay].Enable()
            self.m_btnPulse[relay].Enable()

    def OnBmpClick(self, event=None):
        ctrl_key = event.ControlDown()
        alt_key = event.AltDown()
        shift_key = event.ShiftDown()

        if not ctrl_key and not alt_key and not shift_key:
            self.OnBtnRelayToggleClick(event)
        elif ctrl_key and not alt_key and not shift_key:
            self.send_all_relays_command('on_all')
        elif ctrl_key and not alt_key and shift_key:
            self.send_all_relays_command('off_all')

    def OnBtnRelayOnClick(self, event=None):
        relay = event.GetId()
        self.send_relay_command('on', relay)

    def OnBtnRelayOffClick(self, event=None):
        relay = event.GetId()
        self.send_relay_command('off', relay)

    def OnBtnRelayToggleClick(self, event=None):
        # Another wxPython bug on Ubuntu only:
        # Disabling a panel does not generate events on Windows which is correct behavior,
        # but does not work on Ubuntu.
        # For this reason, it is required to check the state is enabled.
        m_bmpStatus = event.GetEventObject()
        if m_bmpStatus.IsEnabled():
            self.send_relay_command('toggle', relay=event.GetId())

    def OnBtnRelayPulse(self, event=None):
        relay = event.GetId()
        delay = self.m_spnDelay[relay - 1].GetValue()
        self.OnBtnRelayOnClick(event)
        self.m_timer[relay - 1].StartOnce(delay * 1000)
        self.Bind(wx.EVT_TIMER, self.notify, self.m_timer[relay - 1])

    def notify(self, event):
        self.OnBtnRelayOffClick(event)

    def send_relay_command(self, command, relay, delay=None):
        address = self.m_spinAddress.GetValue()

        if delay:
            msg = 'Board #{} relay {} pulse {} sec ... '.format(address, relay, delay)
        else:
            msg = 'Board #{} relay {} {} ... '.format(address, relay, command)

        # Set lock serial port
        self.m_relay_modbus.transfer_begin()
        # Set message status bar
        self.m_status_bar.SetStatusText(msg)
        # Set relay board address
        self.m_relay_board.address = address

        # Send relay command
        try:
            if command == 'on':
                self.m_relay_board.on(relay)
            elif command == 'off':
                self.m_relay_board.off(relay)
            elif command == 'toggle':
                self.m_relay_board.toggle(relay)
            elif command == 'delay' and delay:
                self.m_relay_board.delay(relay, delay)
            else:
                raise Exception('Unknown command: {}'.format(command))
            # Read relay status
            relay_status = self.m_relay_board.get_status(relay)
        except relay_modbus.TransferException as err:
            msg += str(err)
            relay_status = -1
        else:
            msg += 'OK'

        # Update message status bar with result
        self.m_status_bar.SetStatusText(msg)
        # Set relay status icon
        self.set_relay_status_icon(relay, relay_status)
        # Release lock serial port
        self.m_relay_modbus.transfer_end()

    def send_all_relays_command(self, command, delay=None):
        # Get relay board address
        address = self.m_spinAddress.GetValue()

        if delay:
            msg = 'Board #{} all relays pulse {} sec ... '.format(address, delay)
        else:
            msg = 'Board #{} all relays {} ... '.format(address, command)

        # Set lock serial port
        self.m_relay_modbus.transfer_begin()
        # Set message status bar
        self.m_status_bar.SetStatusText(msg)
        # Set relay board address
        self.m_relay_board.address = address

        # Send relay command
        try:
            if command == 'on_all':
                self.m_relay_board.on_all()
            elif command == 'off_all':
                self.m_relay_board.off_all()
            else:
                raise Exception('Unknown command: {}'.format(command))
        except relay_modbus.TransferException as err:
            msg += str(err)
        else:
            msg += 'OK'

        # Release lock serial port
        self.m_relay_modbus.transfer_end()

        # Refresh all relays
        self.refresh_all_relays()

    def refresh_all_relays(self):
        # Get relay board address
        address = self.m_spinAddress.GetValue()

        # Lock serial port around retrieving status all relays
        self.m_relay_modbus.transfer_begin()
        self.m_relay_board.address = address
        try:
            status_relays = self.m_relay_board.get_status_all()
        except relay_modbus.TransferException:
            status_relays = None

        self.m_relay_modbus.transfer_end()

        if status_relays:
            for relay, status in status_relays.items():
                self.set_relay_status_icon(relay, status)
                self.m_status_bar.SetStatusText('Status all relays refreshed.')
        else:
            self.set_relay_status_icons_unknown()
            self.m_status_bar.SetStatusText('Board not responding.')

        self.Refresh()

    def set_relay_status_icons_unknown(self):
        for relay in range(self.m_relay_board.num_relays):
            self.set_relay_status_icon(relay, -1)

    def set_relay_status_icon(self, relay, status):
        if status == 0:
            if self.m_relay_status_off:
                self.m_bmpStatus[relay - 1].SetIcon(self.m_relay_status_off)
        elif status == 1:
            if self.m_relay_status_on:
                self.m_bmpStatus[relay - 1].SetIcon(self.m_relay_status_on)
        else:
            if self.m_relay_status_unknown:
                self.m_bmpStatus[relay - 1].SetIcon(self.m_relay_status_unknown)


# --------------------------------------------------------------------------------------------------
# Custom question dialog box which is not available on all platforms
# --------------------------------------------------------------------------------------------------
class QuestionDialog(dlgQuestion):
    def __init__(self, msg, title, parent):
        """
            Question dialog constructor
        :param msg: Message
        :param title: Dialog title
        :param parent: Parent window
        """
        dlgQuestion.__init__(self, parent)

        self.SetTitle(title)
        self.m_lblQuestion.SetLabel(msg)

    def OnYesClick(self, event):
        self.EndModal(wx.ID_YES)

    def OnNoClick(self, event):
        self.EndModal(wx.ID_NO)


# --------------------------------------------------------------------------------------------------
# Taskbar icon
# --------------------------------------------------------------------------------------------------
class CustomTaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame, icon):
        """
            Create Taskbar icon
        :param frame: Frame
        :type frame: RelayGUI
        :param icon: Taskbar icon
        """
        wx.adv.TaskBarIcon.__init__(self)
        self.frame = frame

        self.SetIcon(icon, self.frame.GetTitle())
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)

    def OnTaskBarActivate(self, event):
        pass

    def OnTaskBarClose(self, event):
        self.frame.Close()

    def OnTaskBarLeftClick(self, event):
        if self.frame.IsIconized():
            self.frame.Show()
            self.frame.Restore()
        else:
            self.frame.Iconize()
            if sys.platform == 'win32':
                # Iconize in Ubuntu is broken with wxPython 4.0.1, so hide window in Windows only.
                self.frame.Hide()

    def OnClose(self, event):
        self.frame.Close()

    def OnRelayClick(self, event):
        self.frame.OnRelayToggleClick(event)

    def CreatePopupMenu(self):
        # Create popupmenu
        popup_menu = wx.Menu()

        # Add Restore/Minimize menu
        if self.frame.IsIconized():
            menu_text = u"Restore"
        else:
            menu_text = u"Minimize"
        m_menuItemRestore = wx.MenuItem(popup_menu, wx.ID_ANY, menu_text, wx.EmptyString,
                                        wx.ITEM_NORMAL)
        popup_menu.Append(m_menuItemRestore)
        self.Bind(wx.EVT_MENU, self.OnTaskBarLeftClick, id=m_menuItemRestore.GetId())

        # Add separator
        popup_menu.AppendSeparator()

        # Add toggle relays menu
        for relay in range(8):
            m_menuItemRelayToggle = wx.MenuItem(popup_menu, relay + 1,
                                                u"Toggle relay {}".format(relay + 1),
                                                wx.EmptyString,
                                                wx.ITEM_NORMAL)
            popup_menu.Append(m_menuItemRelayToggle)
            self.Bind(wx.EVT_MENU, self.OnRelayClick, id=m_menuItemRelayToggle.GetId())

        # Add separator
        popup_menu.AppendSeparator()

        # Add Quit menu
        m_menuItemQuit = wx.MenuItem(popup_menu, wx.ID_ANY, u"Quit", wx.EmptyString,
                                     wx.ITEM_NORMAL)
        popup_menu.Append(m_menuItemQuit)
        self.Bind(wx.EVT_MENU, self.OnClose, id=m_menuItemQuit.GetId())

        # Return popupmenu
        return popup_menu
