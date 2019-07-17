#!/usr/bin/python3.6.7
# -*- coding: utf-8 -*-

PROGRAM_TITLE = "Rapid MAC"
import wx
from wx.lib.floatcanvas import FloatCanvas, NavCanvas, Resources

listbox_list = ['Wait for Packet','Random Backoff','Send Packet']

Node_length = 150
Node_breadth = 30
Port_length = 10
Port_breadth = 15
nodes = []
edges = []
ports = []

inport_wait = []
outport_wait = []
node_wait = []
inport1_back = []
inport2_back = []
outport_back = []
node_back = []

class TestFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.splitter_window = wx.SplitterWindow(self, id = wx.ID_ANY, style = wx.SP_3D)

        self.nav_canvas = NavCanvas.NavCanvas(self.splitter_window, size=(1000, 1000), BackgroundColor = "WHITE")
        self.canvas = self.nav_canvas.Canvas
        self.canvas.InitAll()
        self.canvas.MinScale = 2
        self.canvas.MaxScale = 30
        self.liststatus = 0     # status variable for listbox selections
        self.StatusButton = 0  # status variable for buttons: Nodes,Edges,Ports
        self.EdgeCoords = 0    # status variable for coordinate number of edges
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.properties_panel = wx.Panel(self.splitter_window, id = wx.ID_ANY)
        self.splitter_window.SplitVertically(self.nav_canvas, self.properties_panel)
        
        self.tool_bar = self.nav_canvas.ToolBar
        self.tool_bar.AddSeparator()
        
        self.panel_list = wx.ListBox(self.properties_panel,-1, (30,30),(150,100),
                                listbox_list,wx.LB_SINGLE)

        nodes = wx.Button(self.tool_bar, wx.ID_ANY, "Nodes")
        edges = wx.Button(self.tool_bar, wx.ID_ANY, "Edges")
        ports = wx.Button(self.tool_bar, wx.ID_ANY, "Ports")
        select = wx.Button(self.tool_bar, wx.ID_ANY, "Select")
        
        self.tool_bar.AddControl(nodes)
        self.tool_bar.AddControl(edges)
        self.tool_bar.AddControl(ports)
        self.tool_bar.AddControl(select)
        self.tool_bar.AddSeparator()
        
        self.canvas.Bind(FloatCanvas.EVT_LEFT_DOWN,self.OnLeftDown)
        self.panel_list.Bind(wx.EVT_LISTBOX, self.OnListBox)
        nodes.Bind(wx.EVT_BUTTON, self.OnNodes)
        edges.Bind(wx.EVT_BUTTON, self.OnEdges)
        ports.Bind(wx.EVT_BUTTON, self.OnPorts)

        self.CreateStatusBar()                                                                                                                                                                                                                                                      

        self.Show(True)
        self.Maximize(True)

    def OnNodes(self,event):
        self.StatusButton = 1

    def OnEdges(self,event):
        self.StatusButton = 2

    def OnPorts(self,event):
        self.StatusButton = 3

    def OnListBox(self, event):
        self.SetStatusText(event.GetEventObject().GetStringSelection())
        if (event.GetEventObject().GetStringSelection()) == listbox_list[0]:    # if "Wait for Packet" is selected
            self.liststatus = 1
            self.StatusButton = 0
            self.EdgeCoords = 0
        if (event.GetEventObject().GetStringSelection()) == listbox_list[1]:    # if "Random Backoff" is selected
            self.liststatus = 2
            self.StatusButton = 0
            self.EdgeCoords = 0

    def OnLeftDown(self,event):
        print("self.StatusButton :  ",self.StatusButton)
        print("self.EdgeCoords:  ", self.EdgeCoords)
        if self.StatusButton == 1:      # if Nodes button is pressed, draw rectangular nodes
            if self.EdgeCoords == 0:  
                x = event.Coords[0]
                y = event.Coords[1]
                L = Node_length
                B = Node_breadth
                nodes.append(FloatCanvas.Rectangle((x-L/2,y-B/2), (L, B), FillColor="#95bce7"))
                self.canvas.AddObject(nodes[-1])
                self.canvas.Draw()
            else:
                self.EdgeCoords = 0
                x = event.Coords[0]
                y = event.Coords[1]
                L = Node_length
                B = Node_breadth
                nodes.append(FloatCanvas.Rectangle((x-L/2,y-B/2), (L, B), FillColor="#95bce7"))
                self.canvas.AddObject(nodes[-1])
                self.canvas.Draw()
       
        if self.StatusButton == 2:  # if Edges button is pressed, draw linear edges
            print("self.EdgeCoords: ",self.EdgeCoords)
            if self.EdgeCoords == 0:
                self.x1 = event.Coords[0]
                self.y1 = event.Coords[1]
                print("x1: ",self.x1,"y1: ",self.y1)
                self.EdgeCoords = self.EdgeCoords+1
                print("after addition: self.EdgeCoords-->",self.EdgeCoords)
            else:
                self.x2 = event.Coords[0]
                self.y2 = event.Coords[1]
                print("x2: ",self.x2,"y2: ",self.y2)
                edges.append(FloatCanvas.Line([(self.x1,self.y1),(self.x2,self.y2)], LineColor = 'Black', LineStyle='Solid',LineWidth=2))
                self.canvas.AddObject(edges[-1])
                self.canvas.Draw()
                self.x1 = 0
                self.y1 = 0
                self.x2 = 0
                self.y2 = 0
                self.EdgeCoords = 0
                print("after drawing edge::")
                print("x1: ",self.x1,"y1: ",self.y1)
                print("x2: ",self.x2,"y2: ",self.y2)
                
        if self.StatusButton == 3:      # if Ports button is pressed, draw ports for nodes
            if self.EdgeCoords == 0:
                L = Port_length
                B = Port_breadth
                x = event.Coords[0]
                y = event.Coords[1]
                ports.append(FloatCanvas.Rectangle((x-B/2,y-L/2),(L,B),FillColor = "yellow"))
                self.canvas.AddObject(ports[-1])
                self.canvas.Draw()
            else:
                self.EdgeCoords = 0
                L = Port_length
                B = Port_breadth
                x = event.Coords[0]
                y = event.Coords[1]
                ports.append(FloatCanvas.Rectangle((x-B/2,y-L/2),(L,B),FillColor = "yellow"))
                self.canvas.AddObject(ports[-1])
                self.canvas.Draw()

        if self.StatusButton == 0:
            if self.liststatus == 1:
                x = event.Coords[0]
                y = event.Coords[1]
                L = Node_length
                B = Node_breadth
                l = Port_length
                b = Port_breadth
                inport_wfp = FloatCanvas.Rectangle((x-2,y+B/2), (l, b), FillColor="#b5e795")  # colour: very soft green
                inport_wait.append(inport_wfp)
                self.canvas.AddObject(inport_wait[-1])
                outport_wfp = FloatCanvas.Rectangle((x-2,y-(B/2)-b), (l, b), FillColor="#e795b5")  # colour: very soft pink
                outport_wait.append(outport_wfp)
                self.canvas.AddObject(outport_wait[-1])
                node_wfp = FloatCanvas.Rectangle((x-L/2,y-B/2), (L, B), FillColor="#95bce7")   # colour: very soft blue
                node_wait.append(node_wfp)
                self.canvas.AddObject(node_wait[-1])
                self.canvas.Draw()
            if self.liststatus == 2:
                x = event.Coords[0]
                y = event.Coords[1]
                L = Node_length
                B = Node_breadth
                l = Port_length
                b = Port_breadth
                inport1_rb = FloatCanvas.Rectangle((x-(L/4)-l,y+B/2), (l, b), FillColor="#b5e795")
                inport1_back.append(inport1_rb)
                self.canvas.AddObject(inport1_back[-1])
                inport2_rb = FloatCanvas.Rectangle((x+L/4,y+B/2), (l, b), FillColor="#b5e795")
                inport2_back.append(inport2_rb)
                self.canvas.AddObject(inport2_back[-1])
                outport_rb = FloatCanvas.Rectangle((x-l/2,y-B/2-b), (l, b), FillColor="#e795b5")
                outport_back.append(outport_rb)
                self.canvas.AddObject(outport_back[-1])
                node_rb = FloatCanvas.Rectangle((x-L/2,y-B/2), (L, B), FillColor="#95bce7")
                node_back.append(node_rb)
                self.canvas.AddObject(node_back[-1])
                self.canvas.Draw()

                           
if __name__ == '__main__':
    app = wx.App()
    frame = TestFrame(None, title=PROGRAM_TITLE)
    frame.Show()
    app.MainLoop()

    
