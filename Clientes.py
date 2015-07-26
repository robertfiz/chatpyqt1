'''
Created on 11/7/2015

@author: ksi
'''
import threading
import sys
from socket import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4.QtCore import *
from Tkinter import Widget
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot
import quopri

class QWid(QWidget):
    def __init__(self):
        super(QWid, self).__init__()
        self.setWindowTitle("Clientes")
        self.direccion=QLineEdit()
        #QTextEdit()
        self.boton= QPushButton ("mandar mesaje", self)
        self.re=QTextEdit()
        self.mensa=QTextEdit()
        self.boton_conectar=QPushButton("conectarse",self)
        self.boton_cerrar= QPushButton ("cerrar", self)
        self.reci=None
         


        grilla=QGridLayout(self)
        
        grilla.addWidget(self.mensa,0,0)
        grilla.addWidget(self.re,0,1)
        grilla.addWidget(self.boton,0,2)
        grilla.addWidget(self.direccion)
        grilla.addWidget(self.boton_conectar)
        grilla.addWidget(self.boton_cerrar)

        
        #layout_horizontal=QHBoxLayout(self)
        #layout_horizontal.addWidget(self.mensa)   
        #layout_horizontal.addWidget(self.re)
        #layout_horizontal.addWidget(self.boton)
        
        #layout_vertical=QVBoxLayout(self)
        #layout_vertical.addWidget(self.direccion)
        #layout_vertical.addWidget(self.boton_conectar)
        
        #layout_horizontal.addWidget(self.direccion)
        #layout_vertical.addWidget(self.boton_conectar)
        self.resize(800,600)

        #self.direccion.setGeometry(0,0,50,50)
        #self.boton_conectar.move(500,0)
        #f=threading.Thread(target=self.conectar_a,())
        #f.daemon=True

        #z=threading.Thread(target=self.miboton)
        #z.daemon=True        
        self.boton.clicked.connect(self.miboton)
        self.boton_cerrar.clicked.connect(self.close)
        self.boton_conectar.clicked.connect(self.conectar_a)
        #f=threading.Thread(target=self.run)
        #f.start()
        
    
    def conectar_a(self):
        self.addrl=self.direccion.text()
        #self.addrl=str(self.direccion.toPlainText())
        #self.addrl=self.addrl.rstrip("\n")
        self.s=socket(AF_INET,SOCK_STREAM)
        self.s.connect((self.addrl, 1685))
        self.boton_conectar.setEnabled(False)
        self.c=comunicate()
        self.c.comuni.connect(self.set_message)
        self.c.comu.connect(self.get_message)
        
        self.cliente=servidor_1(self.s,self.c)
        self.cliente.start()
        
        
    def miboton(self):
         self.cliente.send()
         self.boton.setEnabled(False)
         self.cliente.recv()
         self.boton.setEnabled(True)
         
    def get_message(self,so):
         data=str(self.mensa.toPlainText())
         so.socketclient.send(data)
         self.mensa.setPlainText("")

    def set_message(self,data):
        self.re.setPlainText(str(data))
        
    
            
class servidor_1(threading.Thread):
     def __init__(self,s,c):
         threading.Thread.__init__(self)
         self.socketclient = s
         self.c=c
         #self.socketclient.settimeout(1)
     def send(self):
         self.c.comu.emit(self,("comu(PyQt_PyObject)"))
     def recv(self):
         self.data=""
         #while self.data is None:
         self.data=str(self.socketclient.recv(1024))
         self.c.comuni.emit(self.data,("comuni(PyQt_PyObject)"))
         
     
class comunicate(QtCore.QObject):
     comuni=QtCore.pyqtSignal(object,type(""))
     comu=QtCore.pyqtSignal(object,object)
     def __init__(self, parent = None):
        super(comunicate, self).__init__(parent)
     def run(self):
        pass  
      
if __name__=='__main__':
    app= QApplication(sys.argv)
    w= QWid()
    w.show()
    sys.exit(app.exec_())