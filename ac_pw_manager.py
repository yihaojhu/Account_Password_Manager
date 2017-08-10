#!/usr/bin/env python
from PyQt4.QtGui import *
import os,sys,pickle
from Crypto.Cipher import DES3

fname='database.txt'


#----------  Functions for encrypt and decrypt --------------
def encrypt( string, key):
    pad_key = key
    if len(key)%24 !=0 or len(key)==0:
        pad_key += ' '*(24-len(key)%24)
    output = string
    des3 = DES3.new(pad_key, DES3.MODE_ECB)
    if len(string)%24 !=0 :
        output += ' ' * (24 - len(string)%24) 
    return des3.encrypt(output) 


def decrypt( string, key):
    pad_key = key
    if len(key)%24 !=0 or len(key)==0:
        pad_key += ' '*(24-len(key)%24)
    des3 = DES3.new(pad_key, DES3.MODE_ECB)
    return des3.decrypt(string)



#----------  Start our application --------------
class LOOKUP(QWidget):
    def __init__(self,parent=None,fname=None):
        super(LOOKUP,self).__init__(parent)

        self.fname = fname
        self.pop = None
        self.ans = {}
        if os.path.isfile(self.fname):
            fin = open(self.fname,'rb')
            self.ans = pickle.load(fin)
            fin.close()
        self.setWindowTitle("Welcome :)")
        self.layout_and_connection()
 

    def layout_and_connection(self):
        MN_text = QLabel("Magic Number:")
        self.MN_field = QLineEdit()
        self.MN_field.setEchoMode(QLineEdit.Password)
        h0 = QHBoxLayout()
        h0.addWidget(MN_text)
        h0.addWidget(self.MN_field)

        S_text = QLabel("Service:")
        self.S_field = QLineEdit()
        h1 = QHBoxLayout()
        h1.addWidget(S_text)
        h1.addWidget(self.S_field)

        AC_text = QLabel("AC or its hint:")
        self.AC_field = QLineEdit()
        h2 = QHBoxLayout()
        h2.addWidget(AC_text)
        h2.addWidget(self.AC_field)

        PW_text = QLabel("PW or its hint:")
        self.PW_field = QLineEdit()
        h3 = QHBoxLayout()
        h3.addWidget(PW_text)
        h3.addWidget(self.PW_field)

        add = QPushButton("Add")
        remove = QPushButton("Remove")
        find = QPushButton("Find")
        clear = QPushButton("Clear")
        display = QPushButton("Display")
        h4 = QHBoxLayout()
        h4.addWidget(add)
        h4.addWidget(remove)
        h4.addWidget(find)
        h4.addWidget(clear)
        h4.addWidget(display)

        layout = QVBoxLayout()
        layout.addLayout(h0)
        layout.addLayout(h1)
        layout.addLayout(h2)
        layout.addLayout(h3)
        layout.addLayout(h4)
        self.setLayout(layout)

        add.clicked.connect(self.addMethod)
        remove.clicked.connect(self.removeMethod)
        find.clicked.connect(self.findMethod)
        self.S_field.returnPressed.connect(self.findMethod)
        clear.clicked.connect(self.clearMethod)
        display.clicked.connect(self.displayMethod)


    def addMethod(self):
        key = str(self.S_field.text())
        mn = str(self.MN_field.text())
        ac = encrypt( str(self.AC_field.text()), mn )
        pw = encrypt( str(self.PW_field.text()), mn )
        self.S_field.selectAll()
        self.AC_field.selectAll()
        self.PW_field.selectAll()
        self.MN_field.selectAll()
        self.ans[key]=[ac,pw]
        self.save_and_read()
        self.setWindowTitle( 'Successfully adding the service into the data base !' )

    def removeMethod(self):
        key = str(self.S_field.text())
        self.S_field.selectAll()
        self.setWindowTitle( 'Successfully removing the service from the data base !' )
        try:
            del self.ans[key]
            self.save_and_read()
        except:
            self.setWindowTitle( 'The service is not found in the data base :(' )

    def findMethod(self):
        key = str(self.S_field.text())
        mn = str(self.MN_field.text())
        self.S_field.selectAll()
        try:
            self.AC_field.setText( decrypt(self.ans[key][0],mn).strip() )
            self.PW_field.setText( decrypt(self.ans[key][1],mn).strip() )
            self.setWindowTitle( 'Successfully finding the service !' )
        except:
            self.setWindowTitle( 'The service is not found in the data base :(' )
  
    def clearMethod(self):
        self.MN_field.clear()
        self.S_field.clear()
        self.AC_field.clear()
        self.PW_field.clear()
        self.setWindowTitle( 'Successfully clearing everything in the fields !' )

    def displayMethod(self):
        if self.ans=={}:
            self.setWindowTitle( 'No service in the data base now :(' )
        else:
            try:
                self.pop.close()
            except:
                pass
            self.setWindowTitle( 'Please check the pop window for the services !' )
            self.pop = QListWidget()
            self.pop.setWindowTitle('Saved services:')
            for keys in self.ans.keys():
                self.pop.addItem(keys)
            self.pop.itemClicked.connect(self.mouseclick)
            self.pop.show()
            

    def mouseclick(self):
        key = self.pop.currentItem().text()
        self.S_field.setText(key)
       
    
    def save_and_read(self):
        fin = open(self.fname,'wb')
        pickle.dump(self.ans,fin,pickle.HIGHEST_PROTOCOL)
        fin.close()
        fin = open(self.fname,'rb')
        self.ans = pickle.load(fin)
        fin.close()



app = QApplication(sys.argv)
main = LOOKUP(fname=fname)
main.show()
app.exec_()
