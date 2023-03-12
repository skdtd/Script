# -*- coding: UTF-8 -*-
__author__ = 'huangbinghe@gmail.com'

import wx


class TestFrm(wx.Frame):
    """TestFrm"""

    def __init__(self, *arg, **kw):
        super().__init__(*arg, **kw)
        panel = wx.Panel(self, -1)
        box = wx.BoxSizer(wx.VERTICAL)
        for i in range(5):
            btn = wx.Button(panel, -1, label="test-{}".format(i))
            btn.Bind(wx.EVT_BUTTON, lambda e, mark=i: self.on_click(e, mark))
            box.Add(btn, 0, wx.LEFT)

        panel.SetSizer(box)

    def on_click(self, event, mark):
        wx.MessageDialog(self, 'click mark:{}'.format(
            mark), 'click btn', wx.ICON_INFORMATION).ShowModal()


if __name__ == '__main__':
    app = wx.App()
    frm = TestFrm(None, title="hello world")
    frm.Show()
    app.MainLoop()