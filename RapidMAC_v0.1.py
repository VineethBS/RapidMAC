#!/usr/bin/python3.6.7
# -*- coding: utf-8 -*-

import wx
from wx.lib.floatcanvas import FloatCanvas, NavCanvas, Resources
import numpy

listbox_list = ['Wait for Packet','Random backoff','Send Packet']

class TestFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.tool_bar = wx.ToolBar()
        self.tool_bar.AddSeparator()

        self.splitter_window = wx.SplitterWindow(self, id = wx.ID_ANY, style = wx.SP_3D)

        self.nav_canvas = NavCanvas.NavCanvas(self.splitter_window, size=(1000, 1000), BackgroundColor = "IVORY")
        self.canvas = self.nav_canvas.Canvas
        self.canvas.InitAll()
        self.canvas.MinScale = 2
        self.canvas.MaxScale = 30

        self.properties_panel = wx.Panel(self.splitter_window, id = wx.ID_ANY)

        self.splitter_window.SplitVertically(self.nav_canvas, self.properties_panel)
        self.tool_bar = wx.ToolBar()
        self.tool_bar.AddSeparator()
        self.CreateStatusBar()
        
        self.panel_list = wx.ListBox(self.properties_panel,-1, (30,30),(150,100),
                                listbox_list,wx.LB_SINGLE)

        self.panel_list.Bind(wx.EVT_LISTBOX, self.OnListBox)

        self.nav_canvas.Bind(FloatCanvas.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Show(True)

    def OnListBox(self, event):
        self.SetStatusText(event.GetEventObject().GetStringSelection())

        # add a rectangle
    def OnLeftDown(self,event):
        x = event.Coords[0]
        y = event.Coords[1]
        rect = FloatCanvas.Rectangle((x,y), (300, 50), FillColor='Yellow')
        self.canvas.AddObject(rect)
        self.canvas.Draw()

if __name__ == '__main__':
    app = wx.App()
    frame = TestFrame(None, title="Mouse Event Tester")
    app.MainLoop()

    
