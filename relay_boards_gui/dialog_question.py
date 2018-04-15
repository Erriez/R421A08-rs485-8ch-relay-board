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
## Class dlgQuestion
###########################################################################

class dlgQuestion ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Title", pos = wx.DefaultPosition, size = wx.Size( 325,150 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHints( wx.Size( 325,150 ), wx.DefaultSize )
		
		fgSizerDialog = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizerDialog.AddGrowableCol( 0 )
		fgSizerDialog.AddGrowableRow( 0 )
		fgSizerDialog.SetFlexibleDirection( wx.BOTH )
		fgSizerDialog.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel.SetBackgroundColour( wx.Colour( 250, 250, 250 ) )
		
		fgSizerText = wx.FlexGridSizer( 0, 3, 0, 10 )
		fgSizerText.AddGrowableRow( 0 )
		fgSizerText.SetFlexibleDirection( wx.BOTH )
		fgSizerText.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		
		fgSizerText.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_bitmap1 = wx.StaticBitmap( self.m_panel, wx.ID_ANY, wx.Bitmap( u"images/question.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizerText.Add( self.m_bitmap1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.m_lblQuestion = wx.StaticText( self.m_panel, wx.ID_ANY, u"Question", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_lblQuestion.Wrap( 250 )
		fgSizerText.Add( self.m_lblQuestion, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		self.m_panel.SetSizer( fgSizerText )
		self.m_panel.Layout()
		fgSizerText.Fit( self.m_panel )
		fgSizerDialog.Add( self.m_panel, 1, wx.EXPAND|wx.BOTTOM, 5 )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		fgSizerButtons = wx.FlexGridSizer( 0, 4, 0, 0 )
		fgSizerButtons.AddGrowableCol( 0 )
		fgSizerButtons.SetFlexibleDirection( wx.BOTH )
		fgSizerButtons.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		
		fgSizerButtons.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_btnYes = wx.Button( self.m_panel2, wx.ID_ANY, u"&Yes", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		fgSizerButtons.Add( self.m_btnYes, 0, wx.ALL, 5 )
		
		self.m_btnNo = wx.Button( self.m_panel2, wx.ID_ANY, u"&No", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		fgSizerButtons.Add( self.m_btnNo, 0, wx.ALL, 5 )
		
		self.m_btnCancel = wx.Button( self.m_panel2, wx.ID_CANCEL, u"&Cancel", wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
		fgSizerButtons.Add( self.m_btnCancel, 0, wx.ALL, 5 )
		
		
		self.m_panel2.SetSizer( fgSizerButtons )
		self.m_panel2.Layout()
		fgSizerButtons.Fit( self.m_panel2 )
		fgSizerDialog.Add( self.m_panel2, 1, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )
		
		
		self.SetSizer( fgSizerDialog )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_btnYes.Bind( wx.EVT_BUTTON, self.OnYesClick )
		self.m_btnNo.Bind( wx.EVT_BUTTON, self.OnNoClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnYesClick( self, event ):
		event.Skip()
	
	def OnNoClick( self, event ):
		event.Skip()
	

