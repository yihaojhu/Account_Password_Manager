#!/usr/bin/env python
# -*- coding: utf8 -*-
import os, sys, platform
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Crypto.Cipher import DES3
import pickle
import icons

__version__ = 2.0
lengthCharacter = 40

#---- Functions for encrypt and decrypt ----
def encrypt(string, key):
    padingKey = key
    if len(key)%24 !=0 or len(key)==0:
        padingKey += ' '*(24-len(key)%24)
    padingString = string
    encryptor = DES3.new(padingKey, DES3.MODE_ECB)
    if len(string)%24 !=0 :
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

        self.createCentralWidget()
        self.createDockWidgets()

        actionNew = self.getAction("&New", self.newFile, QKeySequence.New,
            "new", "Create an empty database.")
        actionOpen = self.getAction("&Open", self.openFile, QKeySequence.Open,
            "open", "Open an existing database.")
        actionSave = self.getAction("&Save", self.saveFile, QKeySequence.Save,
            "save", "Save data into current database.")
        actionSaveAs = self.getAction("Save &As", self.saveasFile, "Ctrl+A",
            "saveas", "Save data in a new database.")

        self.actions = (actionNew, actionOpen, actionSave, actionSaveAs)
        self.createMenus()
        self.createToolbars()

        settings = QSettings()
        self.recentFiles = settings.value("recentFiles").toStringList()
        self.restoreGeometry( settings.value("geometry").toByteArray() )
        self.restoreState( settings.value("state").toByteArray() )

        QTimer.singleShot(0, self.loadInitialFile)
        self.updateGUI("Ready")

    #---- Methods for creating the Mainwindow ----
    def createCentralWidget(self):
        labelMagicNumber = QLabel("&Magic Number:")
        self.fieldMagicNumber = QLineEdit()
        self.fieldMagicNumber.setEchoMode(QLineEdit.Password)
        self.fieldMagicNumber.setMaxLength(24)
        labelMagicNumber.setBuddy(self.fieldMagicNumber)

        labelService = QLabel("&Service:")
        self.fieldService = QLineEdit()
        self.fieldService.textChanged.connect(self.updateButtons)
        labelService.setBuddy(self.fieldService)

        labelAccount = QLabel("Acc&ount:")
        self.fieldAccount = QLineEdit()
        self.fieldAccount.textChanged.connect(self.updateButtons)
        labelAccount.setBuddy(self.fieldAccount)

        labelPassword = QLabel("&Password:")
        self.fieldPassword = QLineEdit()
        #self.fieldPassword.setMaxLength(24)
        labelPassword.setBuddy(self.fieldPassword)

        self.addButton = QPushButton("&Add")
        self.removeButton = QPushButton("&Remove")
        self.findButton = QPushButton("F&ind")
        clearButton = QPushButton("&Clear")
        self.addButton.clicked.connect(self.addService)
        self.removeButton.clicked.connect(self.removeService)
        self.findButton.clicked.connect(self.findService)
        clearButton.clicked.connect(self.clear)
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
        layout.addWidget(self.addButton, 4, 0)
        layout.addWidget(self.removeButton, 4, 1)
        layout.addWidget(self.findButton, 4, 2)
        layout.addWidget(clearButton, 4, 3)

        layoutTemp = QHBoxLayout()
        layoutTemp.addLayout(layout)
        layoutTemp.addStretch()
        layout = QVBoxLayout()
        layout.addLayout(layoutTemp)
        layout.addStretch()

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def createDockWidgets(self):
        servicesDockWidget = QDockWidget("Saved Services", self)
        servicesDockWidget.setObjectName("servicesDockWidget")
        #servicesDockWidget.setAllowedAreas(Qt.LeftDockWidgetArea|
        #    Qt.RightDockWidgetArea)
        self.servicesListWidget = QListWidget()
        servicesDockWidget.setWidget(self.servicesListWidget)
        self.addDockWidget(Qt.RightDockWidgetArea, servicesDockWidget)
        self.servicesListWidget.itemClicked.connect(self.setService)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        for action in self.actions:
            self.fileMenu.addAction(action)
        self.fileMenu.aboutToShow.connect(self.updateFileMenu)
        aboutAction = self.getAction("A&bout", slot=self.about)
        self.menuBar().addAction(aboutAction)

    def createToolbars(self):
        fileToolbar = self.addToolBar('File')
        fileToolbar.setObjectName("fileToolbar")
        for action in self.actions:
            fileToolbar.addAction(action)
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
                        "Unsaved Changes",
                        "Save unsaved changes?",
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
        service = unicode( self.servicesListWidget.currentItem().text() )
        self.fieldService.setText(service)
        self.fieldService.selectAll()
        self.fieldAccount.clear()
        self.fieldPassword.clear()

    def updateButtons(self):
        service = unicode( self.fieldService.text() )
        account = unicode( self.fieldAccount.text() )
        self.addButton.setEnabled(False)
        self.removeButton.setEnabled(False)
        self.findButton.setEnabled(False)

        if service.strip():
            self.findButton.setEnabled(True)
            self.removeButton.setEnabled(True)
            if account.strip():
                self.addButton.setEnabled(True)

    def updateFileMenu(self):
        self.fileMenu.clear()
        for action in self.actions:
            self.fileMenu.addAction(action)
        currentFile = QString(self.servicesFile) \
            if self.servicesFile is not None else None
        recentFiles = []
        for fname in self.recentFiles:
            if currentFile != fname and QFile.exists(fname):
                recentFiles.append(fname)
        recentFiles.sort()
        if recentFiles:
            self.fileMenu.addSeparator()
            for i, fname in enumerate(recentFiles):
                text = "&%d %s" % (i+1, QFileInfo(fname).fileName())
                action = self.getAction(text, slot=self.loadFile, icon="main")
                action.setData( QVariant(fname) )
                self.fileMenu.addAction(action)

    def updateGUI(self, message=None):
        if message is not None:
            self.statusBar().showMessage(message, 5000)

        self.servicesListWidget.clear()
        services = self.services.keys()
        services.sort()
        for service in services:
            self.servicesListWidget.addItem(service)

        if self.servicesFile is not None:
            self.setWindowTitle("Account Password Manager - %s[*]" % \
                os.path.basename(self.servicesFile))
        elif not len(self.services)==0:
            self.setWindowTitle("Account Password Manager - Unnamed[*]")
        else:
            self.setWindowTitle("Account Password Manager[*]")
        self.setWindowModified(self.dirty)

        self.fieldService.selectAll()
        self.fieldService.setFocus()
    #--------------------------------

    #---- Methods for Buttons ----
    def addService(self):
        service = unicode(self.fieldService.text()).strip()
        if service in self.services.keys():
            text = u"I find an old one. Can I eat it (｡◕∀◕｡)?"
            reply = QMessageBox.question(self,
                        "A voice from a piggy...",
                        text,
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
                        "A voice from a piggy...",
                        u"Cruelly kill it (ﾟ∀。)?",
                        QMessageBox.Yes|QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return
            del self.services[service]
            self.dirty = True
            self.updateGUI('Successfully removing "%s" from database.' % service)
        else:
            text = u'I can\'t find "%s" (╥﹏╥)' % service
            QMessageBox.warning(self, 'A voice from a piggy...', text)

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
            text = u'I can\'t find "%s" (╥﹏╥)' % service
            QMessageBox.warning(self, 'A voice from a piggy...', text)

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
              "txt file (*.txt)") )
        if fname:
            self.loadFile(fname)

    def saveFile(self):
        if len(self.services) == 0:
            text = u'Please add at least one service (*´∀`)~♥'
            QMessageBox.warning(self, 'A voice from a piggy...', text)
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
            text = u'Please add at least one service (*´∀`)~♥'
            QMessageBox.warning(self, 'A voice from a piggy...', text)
            return

        directory = os.path.dirname(self.servicesFile) \
            if self.servicesFile is not None else '.'
        fname = unicode( QFileDialog.getSaveFileName(self,
                    "Save the database", directory,
                    "txt file (*.txt)") )
        if fname:
            if "." not in fname:
                fname += '.txt'
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
        QMessageBox.about( self, "About Account Password Manager",
                """
                <p>Coding by Python {1} - Qt {2} - PyQt {3}
                <p>Copyright &copy; 2017 All rights reserved.
                <p>Version: {0}
                <p>Author: Yi-Hao Jhu
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
            recentFiles = QVariant(self.recentFiles) \
                if self.recentFiles else QVariant()
            settings.setValue('recentFiles', recentFiles)
            settings.setValue( 'geometry', QVariant(self.saveGeometry()) )
            settings.setValue( 'state', QVariant(self.saveState()) )
        else:
            event.ignore()
    #-------------------------------

    #def toUnicode(self, magicNumber):
    #    services = {}
    #    for service in self.services.keys():
    #        mn = magicNumber
    #        ac = decrypt(self.services[service][0], mn)
    #        pw = decrypt(self.services[service][1], mn)
    #        ac = encrypt(unicode(ac), unicode(mn))
    #        pw = encrypt(unicode(pw), unicode(mn))
    #        services[unicode(service)] = [ac, pw]
    #    self.services = services


app = QApplication(sys.argv)
app.setOrganizationName("Piggy")
app.setOrganizationDomain("piggy.org")
app.setApplicationName("Account Password Manager")
app.setWindowIcon(QIcon(":/main.png"))
form = AccountPasswordManager()
form.show()
app.exec_()
