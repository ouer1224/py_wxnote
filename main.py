import wx
from views import MainFrame

class NoteApp(wx.App):
    def OnInit(self):
        MainFrame().Show()
        return True

if __name__ == "__main__":
    app = NoteApp()
    app.MainLoop()