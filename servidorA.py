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
from array import array
import quopri
from time import sleep

  
class QWid(QWidget):
    def __init__(self):
        super(QWid, self).__init__()
        self.setWindowTitle("Servidor")
        self.boton= QPushButton ("mandar mesaje", self)
        #self.boton_cerrar=QPushButton("cerrar",self)
        #self.boton_conectar=QPushButton("Comenzar",self)
        self.re=QTextEdit()
        self.mensa=QTextEdit()
        self.reci=None
        self.threads=[10]
         
        layout_horizontal=QHBoxLayout(self)
        layout_horizontal.addWidget(self.mensa)   
        layout_horizontal.addWidget(self.re)
        layout_horizontal.addWidget(self.boton)
        #layout_horizontal.addWidget(self.boton_cerrar)
        #layout_horizontal.addWidget(self.boton_conectar)
        self.resize(800,600)
        
        #self.connect()
        #self.boton_cerrar.clicked.connect(self.close)
        self.boton.clicked.connect(self.miboton)
        #self.boton_conectar.clicked.connect(self.run)
        f=threading.Thread(target=self.run)
        f.daemon=True
        f.start()
         
    def run(self):
        #bandera=False
        #self.boton_conectar.setEnabled(True)
        #self.boton_conectar.setText("Cerrar")
        #self.boton_conectar.clicked.connect(self.close)
        j=1
        i=1
        s=socket(AF_INET,SOCK_STREAM)
        s.bind(("", 1685))
        s.listen(10)
        self.c=comunicate()
        self.c.comuni.connect(self.set_message)
        self.c.comu.connect(self.get_message)
        self.c.co.connect(self.get_status_botton)
        while 1:
            (self.clientsocket,self.direct) = s.accept()
            self.luck=threading.Lock()
            self.cond=threading.Condition()
            self.cliente=cliente_1(self.luck,self.clientsocket,self.direct,self.c,i,self.cond)
            self.threads.append(self.cliente)
            self.threads[i].start
            #if i > 1 and (self.boton.isEnabled() is False):
            #    self.threads[i-1].lock.acquire()
            #    (self.clientsocket,self.direct) = s.accept()
            #    self.lock=threading.Lock()
            #    self.cliente=cliente_1(self.lock,self.clientsocket,self.direct,self.c,i,bandera)
            #    self.threads.append(self.cliente)
            #    self.threads[i].start
            #else:
            #    (self.clientsocket,self.direct) = s.accept()
            #    self.lock=threading.Lock()
            #    self.cliente=cliente_1(self.lock,self.clientsocket,self.direct,self.c,i,bandera)
            #    self.threads.append(self.cliente)
            #    self.threads[i].start
            i=i+1
        s.close()
        
        
    def miboton(self):
         cuantos_son=len(self.threads)
         i=1
         self.boton.setEnabled(False)
         while i<cuantos_son:
            self.threads[i].send()
            i=i+1
         self.cliente.recv()
         #self.threads[1].recv()
         self.boton.setEnabled(True)

    def get_message(self,so):
         
         data=str(self.mensa.toPlainText())
         #self.mensa.setPlainText("")
         so.socketclient.send(data)


    def set_message(self,data):
         #data+="\n"+self.re.toPlainText()
         #self.re.setPlainText("")
         data+="\n"
         data+=self.re.toPlainText()
         self.re.setPlainText(str(data))
         
    def get_status_botton(self,cond):
        self.cond.acquire()
        if self.boton.isEnabled() is False:
            self.cond.wait()
            #data+=
            #self.re.toPlainText(data)
            #self.boton.setEnabled(True)
        self.cond.notify()
        self.cond.release()
        #self.recv()

  
class cliente_1(threading.Thread):
     def __init__(self, lock, socketclient, addr,c,cantidad_de_hilos,cond):
         threading.Thread.__init__(self)
         self.lock=lock
         self.socketclient = socketclient
         self.addr = addr
         self.c=c
         self.cond=cond
 
         #self.c.co.emit(self,("co(PyQt_PyObject)"))
         #cond.acquire()
         if cantidad_de_hilos>1:
             self.c.co.emit(self,self.cond,("co(PyQt_PyObject)"))
        
         self.recv()     
     def send(self):
         self.c.comu.emit(self,("comu(PyQt_PyObject)"))
                      
     def recv(self):
         data=""#ACA HAY UN PROBLEMA
         #while self.data is None:
         data=str(self.socketclient.recv(1024))
         #print self.data
         self.c.comuni.emit(data,("comuni(PyQt_PyObject)"))
   

class comunicate(QtCore.QObject):
     comuni = QtCore.pyqtSignal(object,type(""))
     comu=QtCore.pyqtSignal(object,object)
     co=QtCore.pyqtSignal(object,object,object)
     def __init__(self, parent = None):
        super(comunicate, self).__init__(parent)
     def run(self):
        pass  


class mi_ventana():
    app= QApplication(sys.argv)
    w= QWid()
    w.show()
    sys.exit(app.exec_())

      
if __name__=='__main__':
    mi_ventana=mi_ventana()
    d=threading.Thread(target=mi_ventana)
    d.daemon=True
    d.start()
    
