# -*- coding: utf-8 -*-

###########################################################################
# Python code generated with wxFormBuilder
# http://www.wxformbuilder.org/
###########################################################################

import webbrowser

import wx
import wx.adv
import wx.xrc
from libs.settings import GREEN

###########################################################################
# Class SetFrame
###########################################################################


class SetFrame (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"MCDR Installer", pos=wx.DefaultPosition,
                          size=wx.Size(475, 270), style=wx.DEFAULT_FRAME_STYLE)

        self.SetSizeHints(wx.Size(425, -1), wx.Size(-1, -1))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"安装路径：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)

        bSizer5.Add(self.m_staticText3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.path_text = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString,
                                     wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY)
        self.path_text.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        bSizer5.Add(self.path_text, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.path_btn = wx.Button(self, wx.ID_ANY, u"选择", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.path_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(bSizer5, 1, wx.EXPAND, 5)

        bSizer9 = wx.BoxSizer(wx.HORIZONTAL)

        self.fabric_check = wx.CheckBox(self, wx.ID_ANY, u"安装 Fabric Server", wx.DefaultPosition, wx.DefaultSize, 0)
        self.fabric_check.SetValue(True)

        bSizer9.Add(self.fabric_check, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        fabric_boxChoices = []
        self.fabric_box = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, fabric_boxChoices, 0)
        self.fabric_box.SetSelection(0)
        bSizer9.Add(self.fabric_box, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.fabric_text = wx.StaticText(self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        self.fabric_text.Wrap(-1)

        self.fabric_text.SetForegroundColour(GREEN)

        bSizer9.Add(self.fabric_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(bSizer9, 1, wx.EXPAND, 5)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.java_check = wx.CheckBox(self, wx.ID_ANY, u"安装 Java", wx.DefaultPosition, wx.DefaultSize, 0)
        self.java_check.SetValue(True)
        bSizer2.Add(self.java_check, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        java_boxChoices = [u"8", u"11", u"16"]
        self.java_box = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, java_boxChoices, 0)
        self.java_box.SetSelection(0)
        bSizer2.Add(self.java_box, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.java_text = wx.StaticText(self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        self.java_text.Wrap(-1)

        self.java_text.SetForegroundColour(GREEN)

        bSizer2.Add(self.java_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        self.python_check = wx.CheckBox(self, wx.ID_ANY, u"安装 Python", wx.DefaultPosition, wx.DefaultSize, 0)
        self.python_check.SetValue(True)
        bSizer8.Add(self.python_check, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        python_boxChoices = []
        self.python_box = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, python_boxChoices, 0)
        self.python_box.SetSelection(0)
        bSizer8.Add(self.python_box, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.python_text = wx.StaticText(self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        self.python_text.Wrap(-1)

        self.python_text.SetForegroundColour(GREEN)

        bSizer8.Add(self.python_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(bSizer8, 1, wx.EXPAND, 5)

        bSizer81 = wx.BoxSizer(wx.HORIZONTAL)

        self.mcdr_check = wx.CheckBox(self, wx.ID_ANY, u"安装 MCDReforged", wx.DefaultPosition, wx.DefaultSize, 0)
        self.mcdr_check.SetValue(True)
        self.mcdr_check.Enable(False)

        bSizer81.Add(self.mcdr_check, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.mcdr_text = wx.StaticText(self, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        self.mcdr_text.Wrap(-1)

        self.mcdr_text.SetForegroundColour(GREEN)

        bSizer81.Add(self.mcdr_text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(bSizer81, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer4.Add((0, 0), 1, wx.EXPAND, 5)

        self.execute_btn = wx.Button(self, wx.ID_ANY, u"执行", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.execute_btn, 0, wx.ALL, 5)

        self.cancel_btn = wx.Button(self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.cancel_btn, 0, wx.ALL, 5)

        bSizer1.Add(bSizer4, 1, wx.EXPAND, 5)

        self.status_bar = self.CreateStatusBar(1)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass


###########################################################################
# Class InstallFrame
###########################################################################

class InstallFrame (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"MCDR Installer", pos=wx.DefaultPosition,
                          size=wx.Size(465, 224), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        bSizer6.Add((0, 0), 1, wx.EXPAND, 5)

        self.progress_text = wx.StaticText(self, wx.ID_ANY, u"正在准备...", wx.DefaultPosition, wx.DefaultSize, 0)
        self.progress_text.Wrap(-1)

        self.progress_text.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL,
                                   wx.FONTWEIGHT_NORMAL, False, "微软雅黑"))

        bSizer6.Add(self.progress_text, 0, wx.ALL, 5)

        self.progress = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size(self.Size[0], 20), wx.GA_HORIZONTAL)
        self.progress.SetValue(0)
        bSizer6.Add(self.progress, 0, wx.ALL, 5)

        self.subprogress = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition,
                                    wx.Size(self.Size[0], 10), wx.GA_HORIZONTAL)
        self.subprogress.SetValue(0)
        bSizer6.Add(self.subprogress, 0, wx.ALL, 5)

        self.subprogress_text = wx.StaticText(self, wx.ID_ANY, u"检测系统环境", wx.DefaultPosition, wx.DefaultSize, 0)
        self.subprogress_text.Wrap(-1)

        bSizer6.Add(self.subprogress_text, 0, wx.ALL, 5)

        bSizer6.Add((0, 0), 1, wx.EXPAND, 5)

        self.cancel_btn = wx.Button(self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer6.Add(self.cancel_btn, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer6)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass


class LinkDialog (wx.Dialog):

    def __init__(self, parent, title='',  message=''):
        wx.Dialog.__init__(self, parent, title=title, pos=wx.DefaultPosition,
                           size=wx.Size(600, 350), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.HSCROLL | wx.TE_AUTO_URL | wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        self.m_textCtrl2.SetValue(message)
        self.m_textCtrl2.Bind(wx.EVT_TEXT_URL, self.open_url)
        self.m_textCtrl2.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL,
                                 wx.FONTWEIGHT_NORMAL, False, "Consolas"))
        bSizer8.Add(self.m_textCtrl2, 1, wx.ALL | wx.EXPAND, 5)

        bSizer9 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer9.Add((0, 0), 1, wx.EXPAND, 5)

        self.agree = wx.Button(self, wx.ID_YES, u"同意", wx.DefaultPosition, wx.DefaultSize, 0)
        self.agree.Bind(wx.EVT_BUTTON, self.on_button)
        bSizer9.Add(self.agree, 0, wx.ALL, 5)

        self.disagree = wx.Button(self, wx.ID_NO, u"不同意", wx.DefaultPosition, wx.DefaultSize, 0)
        self.disagree.Bind(wx.EVT_BUTTON, self.on_button)
        bSizer9.Add(self.disagree, 0, wx.ALL, 5)

        bSizer8.Add(bSizer9, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer8)
        self.Layout()

        self.Centre(wx.BOTH)

    def on_button(self, event):
        if self.IsModal():
            self.EndModal(event.EventObject.Id)
        else:
            self.Close()

    def open_url(self, event: wx.TextUrlEvent):
        mouse: wx.MouseEvent = event.GetMouseEvent()
        if mouse.LeftDown():
            webbrowser.open_new_tab(self.m_textCtrl2.Value[event.URLStart:event.URLEnd])

    def __del__(self):
        pass
