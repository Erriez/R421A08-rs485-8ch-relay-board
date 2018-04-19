# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Apr  8 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class frmRelays
###########################################################################

class frmRelays ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 400,400 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 240, 240, 240 ) )
		
		fgSizer = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer.AddGrowableCol( 0 )
		fgSizer.AddGrowableRow( 1 )
		fgSizer.SetFlexibleDirection( wx.BOTH )
		fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		sbSizerConnection = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Connection" ), wx.VERTICAL )
		
		fgSizerSerialPort = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizerSerialPort.AddGrowableCol( 1 )
		fgSizerSerialPort.SetFlexibleDirection( wx.BOTH )
		fgSizerSerialPort.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_lblSerialPort = wx.StaticText( sbSizerConnection.GetStaticBox(), wx.ID_ANY, u"Serial port:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblSerialPort.Wrap( -1 )
		fgSizerSerialPort.Add( self.m_lblSerialPort, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5 )
		
		m_cmbSerialPortChoices = []
		self.m_cmbSerialPort = wx.Choice( sbSizerConnection.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_cmbSerialPortChoices, 0 )
		self.m_cmbSerialPort.SetSelection( 0 )
		self.m_cmbSerialPort.SetToolTip( u"Serial port (9600 8N1)" )
		
		fgSizerSerialPort.Add( self.m_cmbSerialPort, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_btnConnectDisconnect = wx.Button( sbSizerConnection.GetStaticBox(), wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerSerialPort.Add( self.m_btnConnectDisconnect, 0, wx.ALL, 5 )
		
		
		sbSizerConnection.Add( fgSizerSerialPort, 1, wx.EXPAND, 5 )
		
		
		fgSizer.Add( sbSizerConnection, 1, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
		
		self.m_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_notebook.SetBackgroundColour( wx.Colour( 250, 250, 250 ) )
		self.m_notebook.SetToolTip( u"F2 to rename tab." )
		
		
		fgSizer.Add( self.m_notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( fgSizer )
		self.Layout()
		self.m_menubar = wx.MenuBar( 0 )
		self.m_menuFile = wx.Menu()
		self.m_menuItemNew = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"&New"+ u"\t" + u"Ctrl+N", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItemNew )
		
		self.m_menuItemOpen = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"&Open..."+ u"\t" + u"Ctrl+O", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItemOpen )
		
		self.m_menuItemSave = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"Save"+ u"\t" + u"Ctrl+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItemSave )
		
		self.m_menuItemSaveAs = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"Save As..."+ u"\t" + u"Ctrl+Shift+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItemSaveAs )
		
		self.m_menuFile.AppendSeparator()
		
		self.m_menuItemQuit = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"Quit"+ u"\t" + u"Ctrl+Q", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItemQuit )
		
		self.m_menubar.Append( self.m_menuFile, u"&File" ) 
		
		self.m_menuConnection = wx.Menu()
		self.m_menuItemRefreshPorts = wx.MenuItem( self.m_menuConnection, wx.ID_ANY, u"Refresh Serial Ports"+ u"\t" + u"F6", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuConnection.Append( self.m_menuItemRefreshPorts )
		
		self.m_menuItemConnect = wx.MenuItem( self.m_menuConnection, wx.ID_ANY, u"&Connect"+ u"\t" + u"F3", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuConnection.Append( self.m_menuItemConnect )
		
		self.m_menuItemDisconnect = wx.MenuItem( self.m_menuConnection, wx.ID_ANY, u"&Disconnect"+ u"\t" + u"F4", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuConnection.Append( self.m_menuItemDisconnect )
		
		self.m_menuConnection.AppendSeparator()
		
		self.m_menuItemMonitor = wx.MenuItem( self.m_menuConnection, wx.ID_ANY, u"Monitor"+ u"\t" + u"Ctrl+M", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuConnection.Append( self.m_menuItemMonitor )
		
		self.m_menubar.Append( self.m_menuConnection, u"&Connection" ) 
		
		self.m_menuBoard = wx.Menu()
		self.m_menuItemRename = wx.MenuItem( self.m_menuBoard, wx.ID_ANY, u"&Rename"+ u"\t" + u"F2", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuBoard.Append( self.m_menuItemRename )
		
		self.m_menuBoard.AppendSeparator()
		
		self.m_menuItemAddBoard = wx.MenuItem( self.m_menuBoard, wx.ID_ANY, u"&Add"+ u"\t" + u"Ctrl+B", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuBoard.Append( self.m_menuItemAddBoard )
		
		self.m_menuItemRemoveBoard = wx.MenuItem( self.m_menuBoard, wx.ID_ANY, u"Remove"+ u"\t" + u"Ctrl+D", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuBoard.Append( self.m_menuItemRemoveBoard )
		
		self.m_menubar.Append( self.m_menuBoard, u"&Board" ) 
		
		self.m_menuRelays = wx.Menu()
		self.m_menuItemAllOn = wx.MenuItem( self.m_menuRelays, wx.ID_ANY, u"All On"+ u"\t" + u"Ctrl+1", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuRelays.Append( self.m_menuItemAllOn )
		
		self.m_menuItemAllOff = wx.MenuItem( self.m_menuRelays, wx.ID_ANY, u"All Off"+ u"\t" + u"Ctrl+0", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuRelays.Append( self.m_menuItemAllOff )
		
		self.m_menuRelays.AppendSeparator()
		
		self.m_menuItemRefresh = wx.MenuItem( self.m_menuRelays, wx.ID_ANY, u"Refresh"+ u"\t" + u"F5", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuRelays.Append( self.m_menuItemRefresh )
		
		self.m_menubar.Append( self.m_menuRelays, u"&Relays" ) 
		
		self.m_menuHelp = wx.Menu()
		self.m_menuItemHelp = wx.MenuItem( self.m_menuHelp, wx.ID_ANY, u"&Help"+ u"\t" + u"F1", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuHelp.Append( self.m_menuItemHelp )
		
		self.m_menuItemSource = wx.MenuItem( self.m_menuHelp, wx.ID_ANY, u"Source on GitHub", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuHelp.Append( self.m_menuItemSource )
		
		self.m_menuItemUpdates = wx.MenuItem( self.m_menuHelp, wx.ID_ANY, u"&Check updates...", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuHelp.Append( self.m_menuItemUpdates )
		
		self.m_menuHelp.AppendSeparator()
		
		self.m_menuItemAbout = wx.MenuItem( self.m_menuHelp, wx.ID_ANY, u"About"+ u"\t" + u"Shift+?", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuHelp.Append( self.m_menuItemAbout )
		
		self.m_menubar.Append( self.m_menuHelp, u"&Help" ) 
		
		self.SetMenuBar( self.m_menubar )
		
		self.m_statusBar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnWindowClose )
		self.Bind( wx.EVT_ICONIZE, self.OnWindowIconize )
		self.m_btnConnectDisconnect.Bind( wx.EVT_BUTTON, self.OnConnectDisconnectClick )
		self.m_notebook.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnNotebookPageChanged )
		self.Bind( wx.EVT_MENU, self.OnNewClick, id = self.m_menuItemNew.GetId() )
		self.Bind( wx.EVT_MENU, self.OnOpenClick, id = self.m_menuItemOpen.GetId() )
		self.Bind( wx.EVT_MENU, self.OnSaveClick, id = self.m_menuItemSave.GetId() )
		self.Bind( wx.EVT_MENU, self.OnSaveAsClick, id = self.m_menuItemSaveAs.GetId() )
		self.Bind( wx.EVT_MENU, self.OnQuitClick, id = self.m_menuItemQuit.GetId() )
		self.Bind( wx.EVT_MENU, self.OnRefreshPortsClick, id = self.m_menuItemRefreshPorts.GetId() )
		self.Bind( wx.EVT_MENU, self.OnConnectClick, id = self.m_menuItemConnect.GetId() )
		self.Bind( wx.EVT_MENU, self.OnDisconnectClick, id = self.m_menuItemDisconnect.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMonitorClick, id = self.m_menuItemMonitor.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBoardRenameClick, id = self.m_menuItemRename.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBoardAddClick, id = self.m_menuItemAddBoard.GetId() )
		self.Bind( wx.EVT_MENU, self.OnBoardRemoveClick, id = self.m_menuItemRemoveBoard.GetId() )
		self.Bind( wx.EVT_MENU, self.OnAllRelaysOnClick, id = self.m_menuItemAllOn.GetId() )
		self.Bind( wx.EVT_MENU, self.OnAllRelaysOffClick, id = self.m_menuItemAllOff.GetId() )
		self.Bind( wx.EVT_MENU, self.OnRefreshAllRelaysClick, id = self.m_menuItemRefresh.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuHelp, id = self.m_menuItemHelp.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuSourceOnGitHub, id = self.m_menuItemSource.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuUpdates, id = self.m_menuItemUpdates.GetId() )
		self.Bind( wx.EVT_MENU, self.OnAboutClick, id = self.m_menuItemAbout.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnWindowClose( self, event ):
		event.Skip()
	
	def OnWindowIconize( self, event ):
		event.Skip()
	
	def OnConnectDisconnectClick( self, event ):
		event.Skip()
	
	def OnNotebookPageChanged( self, event ):
		event.Skip()
	
	def OnNewClick( self, event ):
		event.Skip()
	
	def OnOpenClick( self, event ):
		event.Skip()
	
	def OnSaveClick( self, event ):
		event.Skip()
	
	def OnSaveAsClick( self, event ):
		event.Skip()
	
	def OnQuitClick( self, event ):
		event.Skip()
	
	def OnRefreshPortsClick( self, event ):
		event.Skip()
	
	def OnConnectClick( self, event ):
		event.Skip()
	
	def OnDisconnectClick( self, event ):
		event.Skip()
	
	def OnMonitorClick( self, event ):
		event.Skip()
	
	def OnBoardRenameClick( self, event ):
		event.Skip()
	
	def OnBoardAddClick( self, event ):
		event.Skip()
	
	def OnBoardRemoveClick( self, event ):
		event.Skip()
	
	def OnAllRelaysOnClick( self, event ):
		event.Skip()
	
	def OnAllRelaysOffClick( self, event ):
		event.Skip()
	
	def OnRefreshAllRelaysClick( self, event ):
		event.Skip()
	
	def OnMenuHelp( self, event ):
		event.Skip()
	
	def OnMenuSourceOnGitHub( self, event ):
		event.Skip()
	
	def OnMenuUpdates( self, event ):
		event.Skip()
	
	def OnAboutClick( self, event ):
		event.Skip()
	

