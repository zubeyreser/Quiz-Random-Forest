from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import * 
from PyQt4.QtCore import *
import numpy as np
from PyQt4 import QtCore,QtGui
from tasarim import Ui_Dialog
import cv2
import random
import copy
import pickle
import os
from PIL import Image
from sklearn import cross_validation# bunu ekle
from sklearn.cross_validation import train_test_split
from sklearn.cross_validation import KFold
    
class MainWindow(QtGui.QMainWindow, Ui_Dialog):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        self.statusBar().showMessage(unicode("Hazir\n"))
        self.btn_veriYukle.clicked.connect(self.dosyaYukle)
        self.btn_bol.clicked.connect(self.bol)
        self.btn_basr.clicked.connect(self.bak)
        self.label_2.setVisible(False)
        self.label_3.setVisible(False)
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.label_6.setVisible(False)
        self.label_13.setVisible(False)

    def bak(self):
        sira= random.sample([0,1,2,3,4], 4)
        test=10
        sonuc=[0,0,0,0,0]
        for i in range(len(sira)):
            test=test-sira[i]
        sonuc[test]=self.hesapla(sira,test)
        for degistir in range(len(sira)):
            tut = test
            test=sira[degistir]
            sira[degistir]=tut
            sonuc[test]=self.hesapla(sira,test)
        print "Butun sunuclar " ,sonuc
        
        
        self.label_2.setVisible(True)
        self.label_3.setVisible(True)
        self.label_4.setVisible(True)
        self.label_5.setVisible(True)
        self.label_6.setVisible(True)
        self.label_13.setVisible(True)
        self.label_2.setText("Basarisi : "+str(sonuc[0]))
        self.label_3.setText("Basarisi : "+str(sonuc[1]))
        self.label_4.setText("Basarisi : "+str(sonuc[2]))
        self.label_5.setText("Basarisi : "+str(sonuc[3]))
        self.label_6.setText("Basarisi : "+str(sonuc[4]))
        toplam=0.0
        for item in enumerate(sonuc):
            toplam=toplam+item[1]
        self.label_13.setText("Basarilarin Ortalamasi : "+str(float("{0:.2f}".format(toplam/5))))
        
        
            
    def hesapla(self,sira,test):
        print sira,test
        train_x_1=[]   
        train_y_1=[]         
        test_x_1=[]   
        test_y_1=[]         
        
        
        for deger in enumerate(sira):
            print deger[1]
            for i in range(len(self.sozluk[deger[1]])):
                liet=[]
                
                for item in enumerate(self.sozluk[deger[1]][i][0:8]):
                    liet.append( item[1])
                train_x_1.append(liet)
                for item in enumerate(self.sozluk[deger[1]][i][8:9]):
                    train_y_1.append( item[1])
            
            
        np.asarray(train_x_1)
        np.asarray(train_y_1)
        np.asarray(test_x_1)
        np.asarray(test_y_1)
        
        
        for i in range(len(self.sozluk[test])):
            liet=[]
            for item in enumerate(self.sozluk[test][i][0:8]):
                liet.append( item[1])
            test_x_1.append(liet)
            for item in enumerate(self.sozluk[test][i][8:9]):
                test_y_1.append( item[1])
                
        self.X_train, self.X_test, self.y_train, self.y_test =train_x_1, test_x_1, train_y_1, test_y_1         
        
        
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score
        clf = RandomForestClassifier(max_depth=None, random_state=0)
        clf.fit(self.X_train, self.y_train)
        results=clf.predict(self.X_test)
        print "Basari",accuracy_score(self.y_test,results)
        
        return float("{0:.2f}".format(accuracy_score(self.y_test,results)*100))
        
        
    def dosyaYukle(self):
        
        f = open('./data/veri.data')
        X=[]
        for i,row in enumerate(f.readlines()):
            currentline = row.split(",")   
            temp=[]
            for column_value in currentline:
                temp.append(column_value)
            X.append(temp)
        X=np.array(X)
        self.X=X[:,:9]
        self.verileri_dok(self.X,self.table)
        self.label.setText("Sistemde "+ str(X.shape[0])+" adet veri bulunmaktadir.")
        ###############################################
        self.btn_bol.setEnabled(True)
    def verileri_dok(self,X,tablo):
        num_rows=len(X)
        tablo.clear()    
        tablo.setColumnCount(9)
        tablo.setRowCount(num_rows) ##set number of rows

        for rowNumber,row in enumerate(X):
            #row[1].encode("utf-8")
            tablo.setItem(rowNumber, 0, QtGui.QTableWidgetItem(str(row[0])))
            tablo.setItem(rowNumber, 1, QtGui.QTableWidgetItem(str(row[1])))
            tablo.setItem(rowNumber, 2, QtGui.QTableWidgetItem(str(row[2])))
            tablo.setItem(rowNumber, 3, QtGui.QTableWidgetItem(str(row[3])))
            tablo.setItem(rowNumber, 4, QtGui.QTableWidgetItem(str(row[4])))
            tablo.setItem(rowNumber, 5, QtGui.QTableWidgetItem(str(row[5])))
            tablo.setItem(rowNumber, 6, QtGui.QTableWidgetItem(str(row[6])))
            tablo.setItem(rowNumber, 7, QtGui.QTableWidgetItem(str(row[7])))
            tablo.setItem(rowNumber, 8, QtGui.QTableWidgetItem(str(row[8])))
        
            
    def bol(self):
        
        deger =len(self.X)
        adet=deger/5
        liste=[]
        for i in range(5):
            liste.append(adet)
        for i in range(deger-adet*5):
            liste[i]=liste[i]+1
        dene=self.X
        dene = dene.tolist()
        self.sozluk={}
        for i in range(len(liste)):
            self.sozluk[i]=random.sample(dene, int(liste[i]))
            for item in range(len(self.sozluk[i])):
                dene.remove(self.sozluk[i][item])

        num_rows=len(self.sozluk[0])
        self.table_0.clear()    
        self.table_0.setColumnCount(9)
        self.table_0.setRowCount(num_rows)
        for rowNumber,row in enumerate(self.sozluk[0]):
            self.table_0.setItem(rowNumber, 0, QtGui.QTableWidgetItem(str(row[0])))
            self.table_0.setItem(rowNumber, 1, QtGui.QTableWidgetItem(str(row[1])))
            self.table_0.setItem(rowNumber, 2, QtGui.QTableWidgetItem(str(row[2])))
            self.table_0.setItem(rowNumber, 3, QtGui.QTableWidgetItem(str(row[3])))
            self.table_0.setItem(rowNumber, 4, QtGui.QTableWidgetItem(str(row[4])))
            self.table_0.setItem(rowNumber, 5, QtGui.QTableWidgetItem(str(row[5])))
            self.table_0.setItem(rowNumber, 6, QtGui.QTableWidgetItem(str(row[6])))
            self.table_0.setItem(rowNumber, 7, QtGui.QTableWidgetItem(str(row[7])))
            self.table_0.setItem(rowNumber, 8, QtGui.QTableWidgetItem(str(row[8])))
            
        num_rows=len(self.sozluk[1])
        self.table_1.clear()    
        self.table_1.setColumnCount(9)
        self.table_1.setRowCount(num_rows)
        for rowNumber,row in enumerate(self.sozluk[1]):
            self.table_1.setItem(rowNumber, 0, QtGui.QTableWidgetItem(str(row[0])))
            self.table_1.setItem(rowNumber, 1, QtGui.QTableWidgetItem(str(row[1])))
            self.table_1.setItem(rowNumber, 2, QtGui.QTableWidgetItem(str(row[2])))
            self.table_1.setItem(rowNumber, 3, QtGui.QTableWidgetItem(str(row[3])))
            self.table_1.setItem(rowNumber, 4, QtGui.QTableWidgetItem(str(row[4])))
            self.table_1.setItem(rowNumber, 5, QtGui.QTableWidgetItem(str(row[5])))
            self.table_1.setItem(rowNumber, 6, QtGui.QTableWidgetItem(str(row[6])))
            self.table_1.setItem(rowNumber, 7, QtGui.QTableWidgetItem(str(row[7])))
            self.table_1.setItem(rowNumber, 8, QtGui.QTableWidgetItem(str(row[8])))
            
    
        num_rows=len(self.sozluk[2])
        self.table_2.clear()    
        self.table_2.setColumnCount(9)
        self.table_2.setRowCount(num_rows)
        for rowNumber,row in enumerate(self.sozluk[2]):
            self.table_2.setItem(rowNumber, 0, QtGui.QTableWidgetItem(str(row[0])))
            self.table_2.setItem(rowNumber, 1, QtGui.QTableWidgetItem(str(row[1])))
            self.table_2.setItem(rowNumber, 2, QtGui.QTableWidgetItem(str(row[2])))
            self.table_2.setItem(rowNumber, 3, QtGui.QTableWidgetItem(str(row[3])))
            self.table_2.setItem(rowNumber, 4, QtGui.QTableWidgetItem(str(row[4])))
            self.table_2.setItem(rowNumber, 5, QtGui.QTableWidgetItem(str(row[5])))
            self.table_2.setItem(rowNumber, 6, QtGui.QTableWidgetItem(str(row[6])))
            self.table_2.setItem(rowNumber, 7, QtGui.QTableWidgetItem(str(row[7])))
            self.table_2.setItem(rowNumber, 8, QtGui.QTableWidgetItem(str(row[8])))
            
        num_rows=len(self.sozluk[3])
        self.table_3.clear()    
        self.table_3.setColumnCount(9)
        self.table_3.setRowCount(num_rows)
        for rowNumber,row in enumerate(self.sozluk[3]):
            self.table_3.setItem(rowNumber, 0, QtGui.QTableWidgetItem(str(row[0])))
            self.table_3.setItem(rowNumber, 1, QtGui.QTableWidgetItem(str(row[1])))
            self.table_3.setItem(rowNumber, 2, QtGui.QTableWidgetItem(str(row[2])))
            self.table_3.setItem(rowNumber, 3, QtGui.QTableWidgetItem(str(row[3])))
            self.table_3.setItem(rowNumber, 4, QtGui.QTableWidgetItem(str(row[4])))
            self.table_3.setItem(rowNumber, 5, QtGui.QTableWidgetItem(str(row[5])))
            self.table_3.setItem(rowNumber, 6, QtGui.QTableWidgetItem(str(row[6])))
            self.table_3.setItem(rowNumber, 7, QtGui.QTableWidgetItem(str(row[7])))
            self.table_3.setItem(rowNumber, 8, QtGui.QTableWidgetItem(str(row[8])))
            
        num_rows=len(self.sozluk[4])
        self.table_4.clear()    
        self.table_4.setColumnCount(9)
        self.table_4.setRowCount(num_rows)
        for rowNumber,row in enumerate(self.sozluk[4]):
            self.table_4.setItem(rowNumber, 0, QtGui.QTableWidgetItem(str(row[0])))
            self.table_4.setItem(rowNumber, 1, QtGui.QTableWidgetItem(str(row[1])))
            self.table_4.setItem(rowNumber, 2, QtGui.QTableWidgetItem(str(row[2])))
            self.table_4.setItem(rowNumber, 3, QtGui.QTableWidgetItem(str(row[3])))
            self.table_4.setItem(rowNumber, 4, QtGui.QTableWidgetItem(str(row[4])))
            self.table_4.setItem(rowNumber, 5, QtGui.QTableWidgetItem(str(row[5])))
            self.table_4.setItem(rowNumber, 6, QtGui.QTableWidgetItem(str(row[6])))
            self.table_4.setItem(rowNumber, 7, QtGui.QTableWidgetItem(str(row[7])))
            self.table_4.setItem(rowNumber, 8, QtGui.QTableWidgetItem(str(row[8])))
        self.btn_basr.setEnabled(True)