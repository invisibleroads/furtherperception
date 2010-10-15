#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sun Dec 28 22:31:20 2008


# Import system modules
import wx
import wx.grid
import sys
import csv
# Import custom modules
import script_process
from fp.lib import view, store, classifier_cnn


# begin wxGlade: extracode
# end wxGlade


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.label_1 = wx.StaticText(self, -1, "Input map count")
        self.spin_ctrl_inputMapCount = wx.SpinCtrl(self, -1, "3", min=1, max=1000)
        self.label_2 = wx.StaticText(self, -1, "Output map count")
        self.spin_ctrl_outputMapCount = wx.SpinCtrl(self, -1, "6", min=1, max=1000)
        self.grid = wx.grid.Grid(self, -1, size=(1, 1))
        self.button_3 = wx.Button(self, -1, "Load")
        self.button_1 = wx.Button(self, -1, "Clear")
        self.button_2 = wx.Button(self, -1, "Save")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_SPINCTRL, self.onSpinInputMapCount, self.spin_ctrl_inputMapCount)
        self.Bind(wx.EVT_SPINCTRL, self.onSpinOutputMapCount, self.spin_ctrl_outputMapCount)
        self.Bind(wx.EVT_BUTTON, self.onClickLoad, self.button_3)
        self.Bind(wx.EVT_BUTTON, self.onClickClear, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.onClickSave, self.button_2)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("Connect layers")
        self.SetSize((800, 400))
        self.grid.CreateGrid(5, 6)
        self.grid.SetRowLabelSize(20)
        self.grid.SetColLabelSize(20)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_1 = wx.FlexGridSizer(2, 2, 0, 20)
        grid_sizer_1.Add(self.label_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.spin_ctrl_inputMapCount, 0, wx.ADJUST_MINSIZE, 0)
        grid_sizer_1.Add(self.label_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.spin_ctrl_outputMapCount, 0, wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(grid_sizer_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_2.Add(self.grid, 1, wx.EXPAND, 0)
        sizer_3.Add(self.button_3, 1, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.button_1, 1, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        sizer_3.Add(self.button_2, 1, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade
        self.grid.SetDefaultCellAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)
        self.grid.SetDefaultColSize(7, True)
        self.grid.SetDefaultRowSize(7, True)
        self.countRowsAndColumns()

    def countRowsAndColumns(self):
        self.rowCount = self.grid.GetNumberRows()
        self.columnCount = self.grid.GetNumberCols()

    def refresh(self):
        # Initialize
        newRowCount = self.spin_ctrl_inputMapCount.GetValue()
        newColumnCount = self.spin_ctrl_outputMapCount.GetValue()
        # Count
        rowChangeCount = newRowCount - self.rowCount
        columnChangeCount = newColumnCount - self.columnCount
        # If the number of rows changed,
        if rowChangeCount > 0: 
            self.grid.AppendRows(numRows=rowChangeCount)
        elif rowChangeCount < 0: 
            self.grid.DeleteRows(pos=newRowCount, numRows=-rowChangeCount)
        # If the number of columns changed,
        if columnChangeCount > 0: 
            self.grid.AppendCols(numCols=columnChangeCount)
        elif columnChangeCount < 0: 
            self.grid.DeleteCols(pos=newColumnCount, numCols=-columnChangeCount)
        # Count
        self.countRowsAndColumns()

    def clear(self):
        view.clearGrid(self.grid)

    def onSpinInputMapCount(self, event): # wxGlade: MainFrame.<event_handler>
        self.refresh()

    def onSpinOutputMapCount(self, event): # wxGlade: MainFrame.<event_handler>
        self.refresh()

    def onClickClear(self, event): # wxGlade: MainFrame.<event_handler>
        self.clear()

    def onClickSave(self, event): # wxGlade: MainFrame.<event_handler>
        # Get file information
        dialog = wx.FileDialog(self, 'Save', style=wx.SAVE, wildcard='Connection maps (*.map)|*.map')
        if dialog.ShowModal() != wx.ID_OK: return
        connectionMapPath = store.replaceFileExtension(dialog.GetPath(), 'map')
        connectionCSVWriter = csv.writer(open(store.replaceFileExtension(connectionMapPath, 'csv'), 'w'))
        dialog.Destroy()
        # Get connections
        connections = []
        for rowIndex in xrange(self.grid.GetNumberRows()):
            row = []
            for columnIndex in xrange(self.grid.GetNumberCols()):
                value = self.grid.GetCellValue(rowIndex, columnIndex)
                row.append(value)
                if value:
                    connections.append((rowIndex, columnIndex))
            connectionCSVWriter.writerow(row)
        # Save
        open(connectionMapPath, 'wt').write(classifier_cnn.makeLushMatrix(connections))

    def onClickLoad(self, event): # wxGlade: MainFrame.<event_handler>
        # Get file information
        dialog = wx.FileDialog(self, 'Open', style=wx.OPEN, wildcard='Connection maps (*.map)|*.map')
        if dialog.ShowModal() != wx.ID_OK: return
        connectionMapPath = dialog.GetPath()
        dialog.Destroy()
        # Get connections
        inputMapCount, outputMapCount, connections = classifier_cnn.getConnectionMap(connectionMapPath)
        # Load
        self.spin_ctrl_inputMapCount.SetValue(inputMapCount)
        self.spin_ctrl_outputMapCount.SetValue(outputMapCount)
        self.refresh()
        self.clear()
        for x, y in connections: self.grid.SetCellValue(x, y, '1')


    def onClickGo_extractDatabases(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `onClickGo_extractDatabases' not implemented"
        event.Skip()

# end of class MainFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    mainFrame = MainFrame(None, -1, "")
    app.SetTopWindow(mainFrame)
    mainFrame.Show()
    app.MainLoop()
