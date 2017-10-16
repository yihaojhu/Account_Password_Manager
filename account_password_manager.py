#!/usr/bin/env python
# -*- coding: utf8 -*-

#from __future__ import print_function
import os, sys, platform
import pickle
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Crypto.Cipher import DES3
from functools import partial
import icons
from language import LanguagePack

__version__ = 2.0

#---- Functions for encrypt and decrypt ----
def encrypt(string, key):
    padingKey = key
    if len(key)%24 !=0 or len(key)==0:
        padingKey += ' '*(24-len(key)%24)
    padingString = string
    encryptor = DES3.new(padingKey, DES3.MODE_ECB)
    if len(string)%24 !=0 or len(string)==0:
        padingString += ' ' * (24 - len(string)%24)
    return encryptor.encrypt(padingString)

def decrypt(string, key):
    padingKey = key
    if len(key)%24 !=0 or len(key)==0:
        padingKey += ' '*(24-len(key)%24)
    decryptor = DES3.new(padingKey, DES3.MODE_ECB)
    return decryptor.decrypt(string)

class AccountPasswordManager(QMainWindow):
    def __init__(self, parent = None):
        super(AccountPasswordManager, self).__init__(parent)
        self.services = {}
        self.servicesFile = None
        self.dirty = False
        self.LanguagePack = LanguagePack()

        settings = QSettings()
        defaultLanguage = self.LanguagePack.defaultLanguage
        self.language = str( settings.value("language",
            QVariant(defaultLanguage)).toString() )

        self.createCentralWidget()
        self.createDockWidgets()
        self.createActions()
        self.createMenus()
        self.createToolbars()

        self.recentFiles = settings.value("recentFiles").toStringList()
        self.restoreGeometry( settings.value("geometry").toByteArray() )
        self.restoreState( settings.value("state").toByteArray() )

        self.updateLanguage(self.language)

        QTimer.singleShot(0, self.loadInitialFile)
        self.updateGUI("Ready")

    #---- Methods for creating the Mainwindow ----
    def createCentralWidget(self):
        labelMagicNumber = QLabel()
        self.fieldMagicNumber = QLineEdit()
        self.fieldMagicNumber.setEchoMode(QLineEdit.Password)
        self.fieldMagicNumber.setMaxLength(24)
        labelMagicNumber.setBuddy(self.fieldMagicNumber)
        labelMagicNumber.setObjectName('labelMagicNumber')

        labelService = QLabel()
        self.fieldService = QLineEdit()
        self.fieldService.textChanged.connect(self.updateButtons)
        labelService.setBuddy(self.fieldService)
        labelService.setObjectName('labelService')

        labelAccount = QLabel()
        self.fieldAccount = QLineEdit()
        self.fieldAccount.textChanged.connect(self.updateButtons)
        labelAccount.setBuddy(self.fieldAccount)
        labelAccount.setObjectName('labelAccount')

        labelPassword = QLabel()
        self.fieldPassword = QLineEdit()
        labelPassword.setBuddy(self.fieldPassword)
        labelPassword.setObjectName('labelPassword')

        self.buttonAdd = QPushButton()
        self.buttonRemove = QPushButton()
        self.buttonFind = QPushButton()
        buttonClear = QPushButton()
        buttonClear.setObjectName('buttonClear')
        self.buttonAdd.clicked.connect(self.addService)
        self.buttonRemove.clicked.connect(self.removeService)
        self.buttonFind.clicked.connect(self.findService)
        buttonClear.clicked.connect(self.clear)
        self.updateButtons()

        layout = QGridLayout()
        layout.addWidget(labelMagicNumber, 0, 0)
        layout.addWidget(self.fieldMagicNumber, 0, 1, 1, 3)
        layout.addWidget(labelService, 1, 0)
        layout.addWidget(self.fieldService, 1, 1, 1, 3)
        layout.addWidget(labelAccount, 2, 0)
        layout.addWidget(self.fieldAccount, 2, 1, 1, 3)
        layout.addWidget(labelPassword, 3, 0)
        layout.addWidget(self.fieldPassword, 3, 1, 1, 3)
        layout.addWidget(self.buttonAdd, 4, 0)
        layout.addWidget(self.buttonRemove, 4, 1)
        layout.addWidget(self.buttonFind, 4, 2)
        layout.addWidget(buttonClear, 4, 3)

        tempLayout = QHBoxLayout()
        tempLayout.addLayout(layout)
        tempLayout.addStretch()
        layout = QVBoxLayout()
        layout.addLayout(tempLayout)
        layout.addStretch()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def createDockWidgets(self):
        dockWidgetServices = QDockWidget("", self)
        dockWidgetServices.setObjectName("dockWidgetServices")
        #dockWidgetServices.setAllowedAreas(Qt.LeftDockWidgetArea|
        #    Qt.RightDockWidgetArea)
        self.listWidgetServices = QListWidget()
        dockWidgetServices.setWidget(self.listWidgetServices)
        self.addDockWidget(Qt.RightDockWidgetArea, dockWidgetServices)
        self.listWidgetServices.itemClicked.connect(self.setService)

    def createActions(self):
        actionNew = self.getAction("", self.newFile, QKeySequence.New,
            "new", "Create an empty database.")
        actionOpen = self.getAction("", self.openFile, QKeySequence.Open,
            "open", "Open an existing database.")
        actionSave = self.getAction("", self.saveFile, QKeySequence.Save,
            "save", "Save data into current database.")
        actionSaveAs = self.getAction("", self.saveasFile, "Ctrl+A",
            "saveas", "Save data in a new database.")
        self.actions = (actionNew, actionOpen, actionSave, actionSaveAs)
        actionGroupLanguage = QActionGroup(self)
        for language in self.LanguagePack.validLanguages:
            slot = partial(self.updateLanguage, language)
            action = self.getAction("", slot,
                checkable=True, signal="toggled(bool)")
            action.setObjectName("action%s" % language)
            actionGroupLanguage.addAction(action)
            if language == self.language:
                action.setChecked(True)

    def createMenus(self):
        self.menuFile = self.menuBar().addMenu("")
        for action in self.actions:
            self.menuFile.addAction(action)
        self.menuFile.aboutToShow.connect(self.updateMenuFile)
        menuLanguage = self.menuBar().addMenu("")
        menuLanguage.setObjectName('menuLanguage')
        for language in self.LanguagePack.validLanguages:
            action = self.findChild(QAction, 'action%s' % language)
            menuLanguage.addAction(action)
        actionAbout = self.getAction("", slot=self.about)
        actionAbout.setObjectName('actionAbout')
        self.menuBar().addAction(actionAbout)

    def createToolbars(self):
        toolbarFile = self.addToolBar('')
        toolbarFile.setObjectName("toolbarFile")
        for action in self.actions:
            toolbarFile.addAction(action)
    #---------------------------------------------

    #---- Methods for convenient ----
    def getAction(self, text, slot=None, shortcut=None, icon=None,
                 tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def loadInitialFile(self):
        settings = QSettings()
        lastServicesFile = unicode( settings.value("lastServicesFile").toString() )
        if lastServicesFile and QFile.exists(lastServicesFile):
            self.loadFile(lastServicesFile)

    def okToContinue(self):
        if self.dirty:
            reply = QMessageBox.question(self,
                        self.LanguagePack.messageTitle,
                        self.LanguagePack.messageOkToContinue,
                        QMessageBox.Yes|QMessageBox.No|
                        QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                self.saveFile()
        return True

    def addRecentFile(self, fname):
        if fname is None:
            return
        if not self.recentFiles.contains(fname):
            self.recentFiles.prepend(QString(fname))
            while self.recentFiles.count() > 9:
                self.recentFiles.takeLast()

    def setService(self):
        service = unicode( self.listWidgetServices.currentItem().text() )
        self.fieldService.setText(service)
        self.fieldService.selectAll()
        self.fieldAccount.clear()
        self.fieldPassword.clear()

    def updateLanguage(self, language):
        eval("self.LanguagePack.set%s()" % language)
        self.language = language

        text = self.LanguagePack.menuFile
        self.menuFile.setTitle(text)
        text = self.LanguagePack.menuLanguage
        menu = self.findChild(QMenu, "menuLanguage")
        menu.setTitle(text)

        text = self.LanguagePack.toolbarFile
        toolbar = self.findChild(QToolBar, "toolbarFile")
        toolbar.setWindowTitle(text)
        for validlanguage in self.LanguagePack.validLanguages :
            action = self.findChild(QAction, "action%s" % validlanguage)
            text = self.LanguagePack.actionsLanguage[validlanguage]
            action.setText(text)

        for i, name in enumerate(["New", "Open", "Save", "Saveas"]):
            text = eval( "self.LanguagePack.action%s" % name )
            self.actions[i].setText(text)
            text = eval( "self.LanguagePack.tipAction%s" % name )
            self.actions[i].setToolTip(text)
            self.actions[i].setStatusTip(text)
        text = self.LanguagePack.actionAbout
        action = self.findChild(QAction, "actionAbout")
        action.setText(text)

        objectnames = ["labelMagicNumber", "labelService",
            "labelAccount", "labelPassword"]
        for objectname in objectnames:
            text = eval( "self.LanguagePack.%s" % objectname )
            label = self.findChild(QLabel, objectname)
            label.setText(text)

        objectnames = ["buttonAdd", "buttonRemove", "buttonFind"]
        for objectname in objectnames:
            text = eval( "self.LanguagePack.%s" % objectname )
            eval( "self.%s.setText(text)" % objectname )
        text = self.LanguagePack.buttonClear
        button = self.findChild(QPushButton, "buttonClear")
        button.setText(text)

        text = self.LanguagePack.dockWidgetServices
        dockWidget = self.findChild(QDockWidget, 'dockWidgetServices')
        dockWidget.setWindowTitle(text)

        text = self.LanguagePack.titleMainWindow
        self.setWindowTitle(text)

    def updateButtons(self):
        service = unicode( self.fieldService.text() )
        account = unicode( self.fieldAccount.text() )
        self.buttonAdd.setEnabled(False)
        self.buttonRemove.setEnabled(False)
        self.buttonFind.setEnabled(False)

        if service.strip():
            self.buttonFind.setEnabled(True)
            self.buttonRemove.setEnabled(True)
            if account.strip():
                self.buttonAdd.setEnabled(True)

    def updateMenuFile(self):
        self.menuFile.clear()
        for action in self.actions:
            self.menuFile.addAction(action)
        currentFile = QString(self.servicesFile) \
            if self.servicesFile is not None else None
        recentFiles = []
        for fname in self.recentFiles:
            if currentFile != fname and QFile.exists(fname):
                recentFiles.append(fname)
        recentFiles.sort()
        if recentFiles:
            self.menuFile.addSeparator()
            for i, fname in enumerate(recentFiles):
                text = "&%d %s" % (i+1, QFileInfo(fname).fileName())
                action = self.getAction(text, slot=self.loadFile, icon="main")
                action.setData( QVariant(fname) )
                self.menuFile.addAction(action)

    def updateGUI(self, message=None):
        if message is not None:
            self.statusBar().showMessage(message, 5000)

        self.listWidgetServices.clear()
        services = self.services.keys()
        services.sort()
        for service in services:
            self.listWidgetServices.addItem(service)

        title = self.LanguagePack.titleMainWindow
        if self.servicesFile is not None:
            self.setWindowTitle( u"%s - %s[*]" % \
                (title, os.path.basename(self.servicesFile)) )
        elif not len(self.services)==0:
            titleEmptyFile = self.LanguagePack.titleEmptyFile
            self.setWindowTitle(u"%s - %s[*]" % (title, titleEmptyFile))
        else:
            self.setWindowTitle(u"%s[*]" % title)
        self.setWindowModified(self.dirty)

        self.fieldService.selectAll()
        self.fieldService.setFocus()
    #--------------------------------

    #---- Methods for Buttons ----
    def addService(self):
        service = unicode(self.fieldService.text()).strip()
        if service in self.services.keys():
            reply = QMessageBox.question(self,
                        self.LanguagePack.messageTitle,
                        self.LanguagePack.messageAddExistFile,
                        QMessageBox.Yes|QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return

        magicNumber = unicode(self.fieldMagicNumber.text()).strip()
        account = unicode(self.fieldAccount.text()).strip()
        account = encrypt(account, magicNumber)
        password = unicode(self.fieldPassword.text()).strip()
        password = encrypt(password, magicNumber)
        self.services[service] = [account, password]
        self.dirty = True
        self.updateGUI('Successfully adding "%s" into database.' % service)

    def removeService(self):
        service = unicode(self.fieldService.text()).strip()
        if service in self.services.keys():
            reply = QMessageBox.question(self,
                        self.LanguagePack.messageTitle,
                        self.LanguagePack.messageCheckRemove,
                        QMessageBox.Yes|QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return
            del self.services[service]
            self.dirty = True
            self.updateGUI('Successfully removing "%s" from database.' % service)
        else:
            text = u'%s "%s" (╥﹏╥)' % (self.LanguagePack.messageFindNoService, service)
            QMessageBox.warning(self, self.LanguagePack.messageTitle, text)

    def findService(self):
        service = unicode(self.fieldService.text()).strip()
        magicNumber = unicode(self.fieldMagicNumber.text()).strip()
        self.fieldService.selectAll()
        if service in self.services.keys():
            account = decrypt( self.services[service][0], magicNumber ).strip()
            password = decrypt( self.services[service][1], magicNumber ).strip()
            self.fieldAccount.setText(account)
            self.fieldPassword.setText(password)
            text = 'Successfully finding account and password of "%s".' % service
            self.updateGUI(text)
        else:
            text = u'%s "%s" (╥﹏╥)' % (self.LanguagePack.messageFindNoService, service)
            QMessageBox.warning(self, self.LanguagePack.messageTitle, text)

    def clear(self):
        self.fieldMagicNumber.clear()
        self.fieldService.clear()
        self.fieldAccount.clear()
        self.fieldPassword.clear()
        self.fieldMagicNumber.setFocus()
        text = 'All fields have been cleared.'
        self.statusBar().showMessage(text, 5000)
    #--------------------------

    #---- Methods for Actions ----
    def newFile(self):
        if not self.okToContinue():
            return
        self.services = {}
        self.servicesFile = None
        self.dirty = True
        self.updateGUI('Created an empty database.')

    def openFile(self):
        if not self.okToContinue():
            return
        directory = os.path.dirname(self.servicesFile) \
            if self.servicesFile is not None else "."
        fname = unicode( QFileDialog.getOpenFileName(self,
              "Open a database", directory,
              "ppb file (*.ppb)") )
        if fname:
            self.loadFile(fname)

    def saveFile(self):
        if len(self.services) == 0:
            text = self.LanguagePack.messageSaveNothing
            QMessageBox.warning(self, self.LanguagePack.messageTitle, text)
            return

        if self.servicesFile is None:
            self.saveasFile()
        else:
            fin = open(self.servicesFile,'wb')
            pickle.dump(self.services, fin, pickle.HIGHEST_PROTOCOL)
            fin.close()
            message = 'Database has been saved to "%s".' % self.servicesFile
            self.dirty = False
            self.updateGUI(message)

    def saveasFile(self):
        if len(self.services) == 0:
            text = self.LanguagePack.messageSaveNothing
            QMessageBox.warning(self, self.LanguagePack.messageTitle, text)
            return

        directory = os.path.dirname(self.servicesFile) \
            if self.servicesFile is not None else '.'
        fname = unicode( QFileDialog.getSaveFileName(self,
                    "Save the database", directory,
                    "ppb file (*.ppb)") )
        if fname:
            if "." not in fname:
                fname += '.ppb'
            self.addRecentFile(fname)
            self.servicesFile = fname
            self.saveFile()

    def loadFile(self, fname=None):
        if fname is None:
            action = self.sender()
            if isinstance(action, QAction):
                fname = unicode( action.data().toString() )
                if not self.okToContinue():
                    return
            else:
                return

        if fname:
            self.addRecentFile(fname)
            fin = open(fname,'rb')
            self.services = pickle.load(fin)
            fin.close()
            self.servicesFile = fname
            self.dirty = False
            text = 'Database has been loaded from "%s".' % fname
            self.updateGUI(text)

    def about(self):
        QMessageBox.about( self, self.LanguagePack.titleAbout,
                u"""
                <p>Coding by Python {1} - Qt {2} - PyQt {3}
                <p>Copyright &copy; 2017 All rights reserved.
                <p>Version: {0}
                <p>Author: 朱奕豪(Yi-Hao Jhu)
                <p>Github: <a href="https://github.com/yihaojhu">https://github.com/yihaojhu</a>
                <p>Contact: <a href="mailto:g9722525@gmail.com"><font color="blue"><u>g9722525@gmail.com</font></u></a>
                """.format(
                    __version__, platform.python_version(), QT_VERSION_STR,
                    PYQT_VERSION_STR) )
    #------------------------------

    #---- Reimplemented methods ----
    def closeEvent(self, event):
        if self.okToContinue():
            settings = QSettings()
            servicesFile = QVariant(self.servicesFile) \
                if self.servicesFile is not None else QVariant()
            settings.setValue('lastServicesFile', servicesFile)
            settings.setValue( 'language', QVariant(self.language) )
            recentFiles = QVariant(self.recentFiles) \
                if self.recentFiles else QVariant()
            settings.setValue('recentFiles', recentFiles)
            settings.setValue( 'geometry', QVariant(self.saveGeometry()) )
            settings.setValue( 'state', QVariant(self.saveState()) )
        else:
            event.ignore()
    #-------------------------------


app = QApplication(sys.argv)
app.setOrganizationName("Piggy")
app.setOrganizationDomain("piggy.org")
app.setApplicationName("Account Password Manager")
app.setWindowIcon(QIcon(":/main.png"))
form = AccountPasswordManager()
form.show()
app.exec_()
