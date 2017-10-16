#!/usr/bin/env python
# -*- coding: utf8 -*-
class LanguagePack(object):
    def __init__(self):
        super(LanguagePack, self).__init__()
        self.validLanguages = ["English", "Chinese"]
        self.defaultLanguage = "English"
        self.actionsLanguage = {}

    def setEnglish(self):
        self.menuFile = u"&File"
        self.menuLanguage = u"&Language"

        self.toolbarFile=u"File"

        self.actionsLanguage["English"] = u"&English"
        self.actionsLanguage["Chinese"] = u"&Chinese"
        self.actionNew = u"&New"
        self.actionOpen = u"&Open"
        self.actionSave = u"&Save"
        self.actionSaveas = u"Save &As"
        self.actionAbout = u"&About"

        self.tipActionNew = u"Create an empty database."
        self.tipActionOpen = u"Open an existing database."
        self.tipActionSave = u"Save data into current database."
        self.tipActionSaveas = u"Save data in a new database."

        self.newFile = u"Created an empty database."
        self.openFile = u"Open a database"
        self.saveFile = u'Database has been saved to "%s".'
        self.saveasFile = u"Save the database"
        self.loadFile = u'Database has been loaded from "%s".'


        self.labelMagicNumber = u"&Magic Number:"
        self.labelService = u"&Service:"
        self.labelAccount = u"Acc&ount:"
        self.labelPassword = u"&Password:"

        self.buttonAdd = u"&Add"
        self.addService = u'Successfully adding "%s" into database.'
        self.buttonRemove = u"&Remove"
        self.removeService = u'Successfully removing "%s" from database.'
        self.buttonFind = u"F&ind"
        self.findService = u'Successfully finding account and password of "%s" from database.'
        self.buttonClear = u"&Clear"
        self.clear = u"All fields have been cleared."

        self.dockWidgetServices = u"List of Services"

        self.titleMainWindow = u"Account Password Manager"
        self.titleEmptyFile = u"Unnamed"
        self.titleAbout = u"About Account Password Manager"

        self.messageTitle = u"A voice from a piggy..."
        self.okToContinue = u"Would you like to save unsaved changes?"
        self.addExistFile = u"I find an old one. Can I eat it (｡◕∀◕｡)?"
        self.checkRemove = u"Cruelly kill it (ﾟ∀。)?"
        self.findNoService = u'I can\'t find "%s" (╥﹏╥)'
        self.saveNothing = u'Please add at least one service (*´∀`)~♥'

        self.ready = u"Ready"

    def setChinese(self):
        self.menuFile = u"檔案"
        self.menuLanguage = u"語言"

        self.toolbarFile = u"檔案"

        self.actionsLanguage["English"] = u"英文"
        self.actionsLanguage["Chinese"] = u"中文"
        self.actionNew = u"新檔案"
        self.actionOpen = u"開啟"
        self.actionSave = u"存檔"
        self.actionSaveas = u"另存新檔"
        self.actionAbout = u"關於"

        self.tipActionNew = u"開啟新的空白資料庫。"
        self.tipActionOpen = u"打開已存在的資料庫。"
        self.tipActionSave = u"儲存資料於當前資料庫。"
        self.tipActionSaveas = u"儲存資料於新的資料庫。"

        self.newFile = u"已創建一個空資料庫。"
        self.openFile = u"選擇要開啟的資料庫"
        self.saveFile = u'資料庫已儲存於"%s"。'
        self.saveasFile = u"儲存資料庫"
        self.loadFile = u'已讀取資料庫："%s"。'

        self.labelMagicNumber = u"魔法數字："
        self.labelService = u"服務："
        self.labelAccount = u"帳號："
        self.labelPassword = u"密碼："

        self.buttonAdd = u"加入"
        self.addService = u'成功將"%s"加入資料庫。'
        self.buttonRemove = u"移除"
        self.removeService = u'成功將"%s"從資料庫移除。'
        self.buttonFind = u"尋找"
        self.findService = u'成功從資料庫中找到"%s"的帳號密碼。'
        self.buttonClear = u"清除"
        self.clear = u'已清除所有欄位資料。'

        self.dockWidgetServices = u"服務列表"

        self.titleMainWindow = u"帳號密碼管理器"
        self.titleEmptyFile = u"未命名"
        self.titleAbout = u"關於帳號密碼管理器"

        self.messageTitle = u"天外飛來的豬叫聲..."
        self.okToContinue = u"俺好想幫你儲存未儲存的改變，課以嗎？"
        self.addExistFile = u"已經有相同的的服務囉，可以讓俺吃掉舊的嗎 (｡◕∀◕｡)?"
        self.checkRemove = u"殘忍的宰了它嗎(ﾟ∀。)？"
        self.findNoService = u'俺找不到"%s"的啦 (╥﹏╥)'
        self.saveNothing = u"至少添加一個服務嘛 (*´∀`)~♥"

        self.ready = u"準備完成"
