
import wx
import wx.aui
from .nav_panel import NavPanel
from .list_panel import ListPanel
from .text_editor import TextEditor

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='UltraNote',size=(800,600))
        self.aui_manager = wx.aui.AuiManager(self,wx.aui.AUI_MGR_TRANSPARENT_HINT)
        self.nav_panel = NavPanel(self)
        self.list_panel = ListPanel(self)
        self.detail_panel = TextEditor(self)

        self.formatMenu = wx.Menu()

        self.fm_bold = wx.MenuItem(self.formatMenu, -1, "&Bold\tCtrl+B")
        self.fm_test = wx.MenuItem(self.formatMenu,-1,"&test\tCtrl+U");
        self.fm_in = wx.MenuItem(self.formatMenu, -1, "&in\tCtrl+I");
        self.formatMenu.AppendItem(self.fm_bold)
        self.formatMenu.AppendItem(self.fm_test)
        self.formatMenu.AppendItem(self.fm_in)
        self.Bind(wx.EVT_MENU,self.OnBold, id=self.fm_bold.GetId())
        self.Bind(wx.EVT_MENU,self.OnUnder, id=self.fm_test.GetId())
        self.Bind(wx.EVT_MENU,self.OnItalic, id=self.fm_in.GetId())




        #self.Bind(wx.EVT_MENU,self.OnBold);

        menubar = wx.MenuBar()
        menubar.Append(self.formatMenu, 'format')




        self.SetMenuBar(menubar)

        self.aui_manager.AddPane(self.nav_panel, wx.aui.AuiPaneInfo().Left().Row(0).BestSize(300,-1))
        self.aui_manager.AddPane(self.list_panel, wx.aui.AuiPaneInfo().Left().Row(1).BestSize(250, -1).MinSize(150,-1))
        self.aui_manager.AddPane(self.detail_panel, wx.aui.AuiPaneInfo().CenterPane().Position(0).BestSize(400,-1))

        self.aui_manager.Update()

        self.Maximize(True)
        self._register_listeners()
    def OnBold(self, evt):
        self.detail_panel.OnBold(evt)
    def OnUnder(self, evt):
        self.detail_panel.OnUnderline(evt)
    def OnItalic(self, evt):
        self.detail_panel.OnItalic(evt)


    def _get_default_pane_info(self):
        return wx.aui.AuiPaneInfo().CaptionVisible(False).PaneBorder(False).CloseButton(False).PinButton(False).Gripper(
            False)

    def on_frame_closing(self, e):
        self.aui_manager.UnInit()
        del self.aui_manager
        self.Destroy()

    def _register_listeners(self):
        self.Bind(wx.EVT_CLOSE, self.on_frame_closing)



