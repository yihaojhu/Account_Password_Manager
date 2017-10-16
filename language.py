#!/usr/bin/env python
# -*- coding: utf8 -*-
class LanguagePack(object):
    def __init__(self):
        super(LanguagePack, self).__init__()
        self.validLanguages = ["English", "Chinese"]
        self.defaultLanguage = "English"
        self.actionsLanguage = {}

    def setEnglish(self):
        self.menuFile = "&File"
        self.menuLanguage = "&Language"

        self.toolbarFile="File"

        self.actionsLanguage = {}
        self.actionsLanguage["English"] = "&English"
        self.actionsLanguage["Chinese"] = "&Chinese"
        self.actionNew = "&New"
        self.tipActionNew = "Create an empty database."
        self.actionOpen = "&Open"
        self.tipActionOpen = "Open an existing database."
        self.actionSave = "&Save"
        self.tipActionSave = "Save data into current database."
        self.actionSaveas = "Save &As"
        self.tipActionSaveas = "Save data in a new database."
        self.actionAbout = "&About"

        self.labelMagicNumber = "&Magic Number:"
        self.labelService = "&Service:"
        self.labelAccount = "Acc&ount:"
        self.labelPassword = "&Password:"

        self.buttonAdd = "&Add"
        self.buttonRemove = "&Remove"
        self.buttonFind = "F&ind"
        self.buttonClear = "&Clear"

        self.dockWidgetServices = "List of Services"

        self.titleMainWindow = "Account Password Manager"

        self.messageTitle = "A voice from a piggy..."
        self.messageOkToContinue = "Would you like to save unsaved changes?"
        self.titleEmptyFile = "Unnamed"
        self.messageAddExistFile = u"I find an old one. Can I eat it (｡◕∀◕｡)?"
        self.messageCheckRemove = u"Cruelly kill it (ﾟ∀。)?",
        self.messageFindNoService = u'I can\'t find'
        self.messageSaveNothing = u'Please add at least one service (*´∀`)~♥'

        self.titleAbout = "About Account Password Manager"

    def setChinese(self):
        self.menuFile = u"檔案"
        self.menuLanguage = u"語言"

        self.toolbarFile = u"檔案"

        self.actionsLanguage["English"] = u"英文"
        self.actionsLanguage["Chinese"] = u"中文"
        self.actionNew = u"新檔案"
        self.tipActionNew = u"開啟新的空白資料庫。"
        self.actionOpen = u"開啟"
        self.tipActionOpen = u"打開已存在的資料庫。"
        self.actionSave = u"存檔"
        self.tipActionSave = u"儲存資料於當前資料庫。"
        self.actionSaveas = u"另存新檔"
        self.tipActionSaveas = u"儲存資料於新的資料庫。"
        self.actionAbout = u"關於"

        self.labelMagicNumber = u"魔法數字："
        self.labelService = u"服務："
        self.labelAccount = u"帳號："
        self.labelPassword = u"密碼："

        self.buttonAdd = u"加入"
        self.buttonRemove = u"移除"
        self.buttonFind = u"尋找"
        self.buttonClear = u"清除"

        self.dockWidgetServices = u"服務列表"

        self.titleMainWindow = u"帳號密碼管理器"

        self.messageTitle = u"天外飛來的豬叫聲..."
        self.messageOkToContinue = u"俺好想幫你儲存未儲存的改變，課以嗎？"
        self.titleEmptyFile = u"未命名"
        self.messageAddExistFile = u"發現相同的的服務，可以讓俺吃掉舊的嗎 (｡◕∀◕｡)?"
        self.messageCheckRemove = u"殘忍的宰了它嗎(ﾟ∀。)？",
        self.messageFindNoService = u"俺找不到"
        self.messageSaveNothing = u"至少添加一個服務嘛 (*´∀`)~♥"

        self.titleAbout = u"關於帳號密碼管理器"
