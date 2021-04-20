#import wx
from .noname import note
from .text_editor_toolbar import TextEditorToolbar

'''
class TextEditor(wx.Panel):#Panel表示不是一个单独的窗口,如果修改为Frame,就变为了2个独立的窗口
    def __init__(self, parent):
        super().__init__(parent)
        self._init_ui()
    def _init_ui(self):
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.bSizer1 = wx.BoxSizer(wx.VERTICAL)
        self._init_title()
        self._init_toolbar()
        self._init_edit()
        self.SetSizer(self.bSizer1)
    def _init_title(self):
        self.tc_title = wx.TextCtrl(self, wx.ID_ANY, u"请输入标题", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bSizer1.Add(self.tc_title, 0, wx.ALL | wx.EXPAND, 5)
    def _init_edit(self):
        self.tc_detail = wx.TextCtrl(self, wx.ID_ANY, u"请输入内容", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bSizer1.Add(self.tc_detail, 1, wx.ALL | wx.EXPAND, 5)
    def _init_toolbar(self):
        self.toolbar = TextEditorToolbar(self);
        self.bSizer1.Add(self.toolbar, flag=wx.EXPAND | wx.LEFT, border=15)
        line = wx.StaticLine(self, size=(-1, 1))
        line.SetBackgroundColour("#e5e5e5")
        self.bSizer1.Add(line, flag=wx.EXPAND | wx.TOP, border=25);
'''

import wx
import wx.richtext as rt

#----------------------------------------------------------------------

class TextEditor(wx.Panel):#Panel表示不是一个单独的窗口,如果修改为Frame,就变为了2个独立的窗口
    def __init__(self, parent):
        super().__init__(parent)
        #self.toolbar = parent.CreateToolBar()
        self._init_ui()
        #wx.Panel.__init__(self, parent, -1)

    def _init_ui(self):
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.bSizer1 = wx.BoxSizer(wx.VERTICAL)
        self._init_title()
        self._init_toolbar()
        self._init_edit()
        self.SetSizer(self.bSizer1)

    def _init_title(self):
        self.tc_title = wx.TextCtrl(self, wx.ID_ANY, u"请输入标题", wx.DefaultPosition, wx.DefaultSize, 0)
        self.bSizer1.Add(self.tc_title, 0, wx.ALL | wx.EXPAND, 5)

    def _init_toolbar(self):

        self.toolbar = TextEditorToolbar(self);
        #doBind( fileMenu.Append(-1, "E&xit\tCtrl+Q", "Quit this program"),self.OnFileExit )
        self.bSizer1.Add(self.toolbar, flag=wx.EXPAND | wx.LEFT, border=15)
        line = wx.StaticLine(self, size=(-1, 1))
        line.SetBackgroundColour("#e5e5e5")
        self.bSizer1.Add(line, flag=wx.EXPAND | wx.TOP, border=25);

    def _init_edit(self):

        self.rtc = rt.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER);
        wx.CallAfter(self.rtc.SetFocus)

        self.rtc.Freeze()
        self.rtc.BeginSuppressUndo()

        self.rtc.BeginParagraphSpacing(0, 20)

        self.rtc.BeginBold()

        self.rtc.BeginFontSize(14)
        self.rtc.WriteText("Welcome to wxRichTextCtrl, a wxWidgets control for editing and presenting " \
                           "styled text and images")
        self.rtc.EndFontSize()
        self.rtc.Newline()

        self.rtc.BeginItalic()
        self.rtc.WriteText("by Julian Smart")
        self.rtc.EndItalic()
        self.rtc.EndBold()
        self.rtc.Thaw()
        self.bSizer1.Add(self.rtc, 1, wx.ALL | wx.EXPAND, 5)


    def OnURL(self, evt):

        wx.MessageBox(evt.GetString(), "URL Clicked")


    def OnFileOpen(self, evt):

        # This gives us a string suitable for the file dialog based on
        # the file handlers that are loaded
        wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=False)
        dlg = wx.FileDialog(self, "Choose a filename",
                            wildcard=wildcard,
                            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path:
                fileType = types[dlg.GetFilterIndex()]
                self.rtc.LoadFile(path, fileType)
        dlg.Destroy()


    def OnFileSave(self, evt):

        if not self.rtc.GetFilename():
            self.OnFileSaveAs(evt)
            return

        self.rtc.SaveFile()


    def OnFileSaveAs(self, evt):

        wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=True)

        dlg = wx.FileDialog(self, "Choose a filename",
                            wildcard=wildcard,
                            style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path:
                fileType = types[dlg.GetFilterIndex()]
                ext = rt.RichTextBuffer.FindHandlerByType(fileType).GetExtension()
                if not path.endswith(ext):
                    path += '.' + ext
                self.rtc.SaveFile(path, fileType)

        dlg.Destroy()


    def OnFileViewHTML(self, evt):

        # Get an instance of the html file handler, use it to save the
        # document to a StringIO stream, and then display the
        # resulting html text in a dialog with a HtmlWindow.
        handler = rt.RichTextHTMLHandler()
        handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
        handler.SetFontSizeMapping([7,9,11,12,14,22,100])

        import cStringIO
        stream = cStringIO.StringIO()
        if not handler.SaveStream(self.rtc.GetBuffer(), stream):
            return

        import wx.html
        dlg = wx.Dialog(self, title="HTML", style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        html = wx.html.HtmlWindow(dlg, size=(500,400), style=wx.BORDER_SUNKEN)
        html.SetPage(stream.getvalue())
        btn = wx.Button(dlg, wx.ID_CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.ALL|wx.EXPAND, 5)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 10)
        dlg.SetSizer(sizer)
        sizer.Fit(dlg)

        dlg.ShowModal()

        handler.DeleteTemporaryImages()


    def OnFileExit(self, evt):

        self.Close(True)


    def OnBold(self, evt):
        print('ediot bold')
        self.rtc.ApplyBoldToSelection()


    def OnItalic(self, evt):

        self.rtc.ApplyItalicToSelection()


    def OnUnderline(self, evt):

        self.rtc.ApplyUnderlineToSelection()


    def OnAlignLeft(self, evt):

        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_LEFT)


    def OnAlignRight(self, evt):

        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_RIGHT)


    def OnAlignCenter(self, evt):

        self.rtc.ApplyAlignmentToSelection(rt.TEXT_ALIGNMENT_CENTRE)


    def OnIndentMore(self, evt):

        attr = wx.TextAttrEx()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetLeftIndent(attr.GetLeftIndent() + 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)


    def OnIndentLess(self, evt):

        attr = wx.TextAttrEx()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

        if attr.GetLeftIndent() >= 100:
            attr.SetLeftIndent(attr.GetLeftIndent() - 100)
            attr.SetFlags(rt.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)


    def OnParagraphSpacingMore(self, evt):

        attr = rt.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() + 20);
            attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
            self.rtc.SetStyle(r, attr)


    def OnParagraphSpacingLess(self, evt):

        attr = rt.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            if attr.GetParagraphSpacingAfter() >= 20:
                attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() - 20);
                attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
                self.rtc.SetStyle(r, attr)


    def OnLineSpacingSingle(self, evt):

        attr = rt.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(10)
            self.rtc.SetStyle(r, attr)


    def OnLineSpacingHalf(self, evt):

        attr = rt.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(15)
            self.rtc.SetStyle(r, attr)


    def OnLineSpacingDouble(self, evt):

        attr = wx.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(20)
            self.rtc.SetStyle(r, attr)


    def OnFont(self, evt):

        if not self.rtc.HasSelection():
            return

        r = self.rtc.GetSelectionRange()
        fontData = wx.FontData()
        fontData.EnableEffects(False)
        attr = rt.TextAttrEx()
        attr.SetFlags(rt.TEXT_ATTR_FONT)
        if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
            fontData.SetInitialFont(attr.GetFont())

        dlg = wx.FontDialog(self, fontData)
        if dlg.ShowModal() == wx.ID_OK:
            fontData = dlg.GetFontData()
            font = fontData.GetChosenFont()
            if font:
                attr.SetFlags(rt.TEXT_ATTR_FONT)
                attr.SetFont(font)
                self.rtc.SetStyle(r, attr)
        dlg.Destroy()


    def OnColour(self, evt):

        colourData = wx.ColourData()
        attr = rt.TextAttrEx()
        attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
        if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
            colourData.SetColour(attr.GetTextColour())

        dlg = wx.ColourDialog(self, colourData)
        if dlg.ShowModal() == wx.ID_OK:
            colourData = dlg.GetColourData()
            colour = colourData.GetColour()
            if colour:
                if not self.rtc.HasSelection():
                    self.rtc.BeginTextColour(colour)
                else:
                    r = self.rtc.GetSelectionRange()
                    attr.SetFlags(rt.TEXT_ATTR_TEXT_COLOUR)
                    attr.SetTextColour(colour)
                    self.rtc.SetStyle(r, attr)
        dlg.Destroy()



    def OnUpdateBold(self, evt):

        evt.Check(self.rtc.IsSelectionBold())


    def OnUpdateItalic(self, evt):

        evt.Check(self.rtc.IsSelectionItalics())


    def OnUpdateUnderline(self, evt):

        evt.Check(self.rtc.IsSelectionUnderlined())


    def OnUpdateAlignLeft(self, evt):

        evt.Check(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_LEFT))


    def OnUpdateAlignCenter(self, evt):

        evt.Check(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_CENTRE))


    def OnUpdateAlignRight(self, evt):

        evt.Check(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_RIGHT))


    def ForwardEvent(self, evt):

        # The RichTextCtrl can handle menu and update events for undo,
        # redo, cut, copy, paste, delete, and select all, so just
        # forward the event to it.
        self.rtc.ProcessEvent(evt)


    def MakeMenuBar(self):

        def doBind(item, handler, updateUI=None):

            self.Bind(wx.EVT_MENU, handler, item)
            if updateUI is not None:
                self.Bind(wx.EVT_UPDATE_UI, updateUI, item)

        fileMenu = wx.Menu()
        doBind( fileMenu.Append(-1, "&Open\tCtrl+O", "Open a file"),
                self.OnFileOpen )
        doBind( fileMenu.Append(-1, "&Save\tCtrl+S", "Save a file"),
                self.OnFileSave )
        doBind( fileMenu.Append(-1, "&Save As...\tF12", "Save to a new file"),
                self.OnFileSaveAs )
        fileMenu.AppendSeparator()
        doBind( fileMenu.Append(-1, "&View as HTML", "View HTML"),
                self.OnFileViewHTML)
        fileMenu.AppendSeparator()
        doBind( fileMenu.Append(-1, "E&xit\tCtrl+Q", "Quit this program"),
                self.OnFileExit )

        editMenu = wx.Menu()
        doBind( editMenu.Append(wx.ID_UNDO, "&Undo\tCtrl+Z"),
                self.ForwardEvent, self.ForwardEvent)
        doBind( editMenu.Append(wx.ID_REDO, "&Redo\tCtrl+Y"),
                self.ForwardEvent, self.ForwardEvent )
        editMenu.AppendSeparator()
        doBind( editMenu.Append(wx.ID_CUT, "Cu&t\tCtrl+X"),
                self.ForwardEvent, self.ForwardEvent )
        doBind( editMenu.Append(wx.ID_COPY, "&Copy\tCtrl+C"),
                self.ForwardEvent, self.ForwardEvent)
        doBind( editMenu.Append(wx.ID_PASTE, "&Paste\tCtrl+V"),
                self.ForwardEvent, self.ForwardEvent)
        doBind( editMenu.Append(wx.ID_CLEAR, "&Delete\tDel"),
                self.ForwardEvent, self.ForwardEvent)
        editMenu.AppendSeparator()
        doBind( editMenu.Append(wx.ID_SELECTALL, "Select A&ll\tCtrl+A"),
                self.ForwardEvent, self.ForwardEvent )

        formatMenu = wx.Menu()
        doBind( formatMenu.AppendCheckItem(-1, "&Bold\tCtrl+B"),
                self.OnBold, self.OnUpdateBold)
        doBind( formatMenu.AppendCheckItem(-1, "&Italic\tCtrl+I"),
                self.OnItalic, self.OnUpdateItalic)
        doBind( formatMenu.AppendCheckItem(-1, "&Underline\tCtrl+U"),
                self.OnUnderline, self.OnUpdateUnderline)
        formatMenu.AppendSeparator()
        doBind( formatMenu.AppendCheckItem(-1, "L&eft Align"),
                self.OnAlignLeft, self.OnUpdateAlignLeft)
        doBind( formatMenu.AppendCheckItem(-1, "&Centre"),
                self.OnAlignCenter, self.OnUpdateAlignCenter)
        doBind( formatMenu.AppendCheckItem(-1, "&Right Align"),
                self.OnAlignRight, self.OnUpdateAlignRight)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, "Indent &More"), self.OnIndentMore)
        doBind( formatMenu.Append(-1, "Indent &Less"), self.OnIndentLess)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, "Increase Paragraph &Spacing"), self.OnParagraphSpacingMore)
        doBind( formatMenu.Append(-1, "Decrease &Paragraph Spacing"), self.OnParagraphSpacingLess)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, "Normal Line Spacing"), self.OnLineSpacingSingle)
        doBind( formatMenu.Append(-1, "1.5 Line Spacing"), self.OnLineSpacingHalf)
        doBind( formatMenu.Append(-1, "Double Line Spacing"), self.OnLineSpacingDouble)
        formatMenu.AppendSeparator()
        doBind( formatMenu.Append(-1, "&Font..."), self.OnFont)

        #mb = wx.MenuBar()
        #mb.Append(fileMenu, "&File")
        #mb.Append(editMenu, "&Edit")
        #mb.Append(formatMenu, "F&ormat")
       # self.SetMenuBar(mb)


    def MakeToolBar(self):

        def doBind(item, handler, updateUI=None):

            self.Bind(wx.EVT_TOOL, handler, item)
            if updateUI is not None:
                self.Bind(wx.EVT_UPDATE_UI, updateUI, item)

        #tbar = self.CreateToolBar()


        #tbar.Realize()


#----------------------------------------------------------------------

class TestPanel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Show the RichTextCtrl sample", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

        self.AddRTCHandlers()


    def AddRTCHandlers(self):

        # make sure we haven't already added them.
        if rt.RichTextBuffer.FindHandlerByType(rt.RICHTEXT_TYPE_HTML) is not None:
            return

        # This would normally go in your app's OnInit method.  I'm
        # not sure why these file handlers are not loaded by
        # default by the C++ richtext code, I guess it's so you
        # can change the name or extension if you wanted...
        rt.RichTextBuffer.AddHandler(rt.RichTextHTMLHandler())
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())

        # ...like this
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler(name="Other XML",
                                                           ext="ox",
                                                           type=99))

        # This is needed for the view as HTML option since we tell it
        # to store the images in the memory file system.
        wx.FileSystem.AddHandler(wx.MemoryFSHandler())


    def OnButton(self, evt):

        win = RichTextFrame(self, -1, "wx.richtext.RichTextCtrl",
                            size=(700, 500),
                            style = wx.DEFAULT_FRAME_STYLE)
        win.Show(True)

        # give easy access to the demo's PyShell if it's running
        self.rtfrm = win
        self.rtc = win.rtc






