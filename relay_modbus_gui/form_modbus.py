# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jan 23 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class frmModbus
###########################################################################

class frmModbus ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"MODBUS Send & Receive", pos = wx.DefaultPosition, size = wx.Size( 450,400 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.Size( 400,320 ), wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )
		
		self.m_menubar = wx.MenuBar( 0 )
		self.m_menuFile = wx.Menu()
		self.m_menuItemQuit = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"&Quit"+ u"\t" + u"Ctrl+Q", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItemQuit )
		
		self.m_menubar.Append( self.m_menuFile, u"&File" ) 
		
		self.m_menuEdit = wx.Menu()
		self.m_menuItemCopyLogClipboard = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, u"&Copy log to clipboard"+ u"\t" + u"Ctrl+L", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItemCopyLogClipboard )
		
		self.m_menuEdit.AppendSeparator()
		
		self.m_menuItemClearLog = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, u"Clear &Log"+ u"\t" + u"Ctrl+DEL", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItemClearLog )
		
		self.m_menuItemClearHistory = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, u"Clear Transmit &History"+ u"\t" + u"Ctrl+H", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItemClearHistory )
		
		self.m_menubar.Append( self.m_menuEdit, u"&Edit" ) 
		
		self.m_menuConnection = wx.Menu()
		self.m_menuItemRefreshSerialPorts = wx.MenuItem( self.m_menuConnection, wx.ID_ANY, u"&Refresh Serial Ports"+ u"\t" + u"F6", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuConnection.Append( self.m_menuItemRefreshSerialPorts )
		
		self.m_menuItemConnect = wx.MenuItem( self.m_menuConnection, wx.ID_ANY, u"Connect"+ u"\t" + u"F3", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuConnection.Append( self.m_menuItemConnect )
		
		self.m_menuItemDisconnect = wx.MenuItem( self.m_menuConnection, wx.ID_ANY, u"&Disconnect"+ u"\t" + u"F4", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuConnection.Append( self.m_menuItemDisconnect )
		
		self.m_menubar.Append( self.m_menuConnection, u"&Connection" ) 
		
		self.m_menuOptions = wx.Menu()
		self.m_menuItemAppendCRC = wx.MenuItem( self.m_menuOptions, wx.ID_ANY, u"&Append CRC to frame"+ u"\t" + u"F9", wx.EmptyString, wx.ITEM_CHECK )
		self.m_menuOptions.Append( self.m_menuItemAppendCRC )
		self.m_menuItemAppendCRC.Check( True )
		
		self.m_menubar.Append( self.m_menuOptions, u"&Options" ) 
		
		self.m_menuHelp = wx.Menu()
		self.m_menuItemAbout = wx.MenuItem( self.m_menuHelp, wx.ID_ANY, u"&About"+ u"\t" + u"Shift+?", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuHelp.Append( self.m_menuItemAbout )
		
		self.m_menubar.Append( self.m_menuHelp, u"&Help" ) 
		
		self.SetMenuBar( self.m_menubar )
		
		fgSizer = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer.AddGrowableCol( 0 )
		fgSizer.AddGrowableRow( 1 )
		fgSizer.SetFlexibleDirection( wx.BOTH )
		fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		sbSizerConnection = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Connection" ), wx.VERTICAL )
		
		fgSizerSerialPort = wx.FlexGridSizer( 0, 4, 0, 0 )
		fgSizerSerialPort.AddGrowableCol( 1 )
		fgSizerSerialPort.SetFlexibleDirection( wx.BOTH )
		fgSizerSerialPort.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_lblSerialPort = wx.StaticText( sbSizerConnection.GetStaticBox(), wx.ID_ANY, u"Serial port:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblSerialPort.Wrap( -1 )
		fgSizerSerialPort.Add( self.m_lblSerialPort, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_cmbSerialPortChoices = []
		self.m_cmbSerialPort = wx.ComboBox( sbSizerConnection.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_cmbSerialPortChoices, wx.CB_DROPDOWN|wx.CB_READONLY )
		self.m_cmbSerialPort.SetToolTip( u"Serial port (9600 8N1)" )
		
		fgSizerSerialPort.Add( self.m_cmbSerialPort, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_btnOnConnectDisconnect = wx.Button( sbSizerConnection.GetStaticBox(), wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_btnOnConnectDisconnect.SetToolTip( u"Open/close serial port" )
		
		fgSizerSerialPort.Add( self.m_btnOnConnectDisconnect, 0, wx.ALL, 5 )
		
		
		sbSizerConnection.Add( fgSizerSerialPort, 1, wx.EXPAND, 5 )
		
		
		fgSizer.Add( sbSizerConnection, 1, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		sbSizerLog = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Log" ), wx.VERTICAL )
		
		self.m_txtLog = wx.TextCtrl( sbSizerLog.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
		sbSizerLog.Add( self.m_txtLog, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer.Add( sbSizerLog, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		sbSizerTransmit = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Transmit" ), wx.VERTICAL )
		
		fgSizerTransmit = wx.FlexGridSizer( 2, 2, 0, 0 )
		fgSizerTransmit.AddGrowableCol( 0 )
		fgSizerTransmit.SetFlexibleDirection( wx.BOTH )
		fgSizerTransmit.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		m_cmbCommandChoices = [ u":010600010300", u"01 06 00 01 03 00", u"0x01, 0x06, 0x00, 0x01, 0x03, 0x00" ]
		self.m_cmbCommand = wx.ComboBox( sbSizerTransmit.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_cmbCommandChoices, wx.TE_PROCESS_ENTER )
		fgSizerTransmit.Add( self.m_cmbCommand, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_btnSend = wx.Button( sbSizerTransmit.GetStaticBox(), wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_btnSend.SetToolTip( u"Send MODBUS frame [ENTER]" )
		
		fgSizerTransmit.Add( self.m_btnSend, 0, wx.ALL, 5 )
		
		
		sbSizerTransmit.Add( fgSizerTransmit, 1, wx.EXPAND, 5 )
		
		
		fgSizer.Add( sbSizerTransmit, 1, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )
		
		
		self.SetSizer( fgSizer )
		self.Layout()
		self.m_statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnWindowClose )
		self.Bind( wx.EVT_MENU, self.OnMenuQuit, id = self.m_menuItemQuit.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuCopyLogClipboard, id = self.m_menuItemCopyLogClipboard.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuClearLog, id = self.m_menuItemClearLog.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuClearHistory, id = self.m_menuItemClearHistory.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBtnRefreshClick, id = self.m_menuItemRefreshSerialPorts.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBtnConnectDisconnect, id = self.m_menuItemConnect.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBtnConnectDisconnect, id = self.m_menuItemDisconnect.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuAppendCRC, id = self.m_menuItemAppendCRC.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuAbout, id = self.m_menuItemAbout.GetId() )
		self.m_btnOnConnectDisconnect.Bind( wx.EVT_BUTTON, self.OnBtnConnectDisconnect )
		self.m_txtLog.Bind( wx.EVT_KEY_DOWN, self.OnLogKeyDown )
		self.m_cmbCommand.Bind( wx.EVT_TEXT, self.OnCommandText )
		self.m_cmbCommand.Bind( wx.EVT_TEXT_ENTER, self.OnCommandEnter )
		self.m_btnSend.Bind( wx.EVT_BUTTON, self.OnBtnSend )
		self.m_btnSend.Bind( wx.EVT_LEFT_DOWN, self.OnSend )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnWindowClose( self, event ):
		event.Skip()
	
	def OnMenuQuit( self, event ):
		event.Skip()
	
	def OnMenuCopyLogClipboard( self, event ):
		event.Skip()
	
	def OnMenuClearLog( self, event ):
		event.Skip()
	
	def OnMenuClearHistory( self, event ):
		event.Skip()
	
	def OnBtnRefreshClick( self, event ):
		event.Skip()
	
	def OnBtnConnectDisconnect( self, event ):
		event.Skip()
	
	
	def OnMenuAppendCRC( self, event ):
		event.Skip()
	
	def OnMenuAbout( self, event ):
		event.Skip()
	
	
	def OnLogKeyDown( self, event ):
		event.Skip()
	
	def OnCommandText( self, event ):
		event.Skip()
	
	def OnCommandEnter( self, event ):
		event.Skip()
	
	def OnBtnSend( self, event ):
		event.Skip()
	
	def OnSend( self, event ):
		event.Skip()
	

