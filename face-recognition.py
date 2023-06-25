from turtle import width
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import sqlite3
from datetime import date
import cv2, os, numpy 


ui,_= loadUiType('face-rec skripsi.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.LOGINBUTTON.clicked.connect(self.login)
        self.CLOSEBUTTON.clicked.connect(self.closeWindow)
        self.LOGOUTBUTTON.clicked.connect(self.logout)
        self.TRAINLINK1.clicked.connect(self.trainingWajah)
        self.ATTLINK1.clicked.connect(self.absenDosen)
        self.ATTLINK2.clicked.connect(self.absenMahasiswa)
        self.REPORTSLINK1.clicked.connect(self.reports)
        self.TRAININGBACK.clicked.connect(self.tampilHalamanUtama)
        self.ATTENDANCEBACK.clicked.connect(self.tampilHalamanUtama)
        self.ATTENDANCEBACK2.clicked.connect(self.tampilHalamanUtama)
        self.REPORTSBACK.clicked.connect(self.tampilHalamanUtama)
        self.TRAININGBUTTON.clicked.connect(self.start_training)




    #-------LOGIN PROSES--------#
    def login(self):
        kataSandi = self.PASSWORD.text()
        if (kataSandi == "Gunadarma2019"):
            self.PASSWORD.setText("")
            self.LOGININFO.setText("")
            self.tabWidget.setCurrentIndex(1) #jika Passwordnya true maka akan ke halaman utama
        else:
            self.LOGININFO.setText("Password Salah")
            self.PASSWORD.setText("")

       #-------LOGOUT PROSES--------#
    def logout(self):
        self.tabWidget.setCurrentIndex(0)

      #-------Close Window Prosses--------#
    def closeWindow(self):
        self.close()

        #-------Absen Mahasiswa Prosses--------#
    def tampilHalamanUtama(self):
        self.tabWidget.setCurrentIndex(1)



      #-------Training Prosses--------#
    def trainingWajah(self):
        self.tabWidget.setCurrentIndex(2)

      #-------Absen Dosen Prosses--------#
    def absenDosen(self):
        self.tabWidget.setCurrentIndex(3)

    #-------Absen Mahasiswa Prosses--------#
    def absenMahasiswa(self):
        self.tabWidget.setCurrentIndex(4)

    #-------Absen Mahasiswa Prosses--------#
    def reports(self):
        self.tabWidget.setCurrentIndex(5)



    #--------PROSES TRAINING WAJAH---------#
    # def start_training(self):
    #     haar_file = 'haarcascade_frontalface_default.xml'
    #     datasets = 'datasets'
    #     sub_data = self.traineeName.text() #Ini agar datasetnya tersimpan sesuai dengan nama yang dimasukan pada saat training
    #     path = os.path.join(datasets,sub_data)
    #     if not os.path.isdir(path): #jika foldderbya gaada maka dibuat folder
    #         os.mkdir(path)
    #         print("Folder Baru Telah dibuat")
    #         (width,height) = (130,100)
    #         face_cascade = cv2.CascadeClassifier(haar_file)
    #         webcam = cv2.VideoCapture(0) #0 itu artinya kamera utama
    #         count = 1
    #         while count < int(self.trainingCount.text()) + 1:
    #             print(count)
    #             (_,im) = webcam.read()
    #             gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #ini untuk convert image training menjadi warna greysacle
    #             faces = face_cascade.detectMultiScale(gray,1.3,4)
    #             for (x,y,w,h) in faces:
    #                 cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
    #                 face = gray[y:y+h,x:x+w]
    #                 face_resize =cv2.resize(face,(width,height))
    #                 cv2.imwrite("%s/%s.png"%(path,count),face_resize) #untuk menyimpan gambar
    #             count += 1
    #             cv2.imshow("OpenCV",im) #untuk menunjukan gambar
    #             key = cv2.waitkey(10)
    #             if key == 27:
    #                 break
    #         webacam.release()
    #         cv2.destroyAllWindows()
    #         path=""
    #         QMessageBox.information(self, "Training Wajah Berhasil")
    #         self.traineeName.setText("") #ini untuk inputan di training ketika udh diisini dan ngeklik training wajah maka akan ksoong
    #         self.trainingCount.setText("100")
    def start_training(self):
        datasets = 'datasets'
        sub_data = self.traineeName.text()
        path = os.path.join(datasets, sub_data)
        if not os.path.isdir(path):
            os.mkdir(path)
            print("Folder Baru Telah dibuat")
            (width, height) = (130, 100)
            cascade_dir = os.path.dirname(cv2.__file__)
            haar_file = os.path.join(cascade_dir, 'data', 'haarcascade_frontalface_default.xml')
            face_cascade = cv2.CascadeClassifier(haar_file)
            webcam = cv2.VideoCapture(0)
            count = 1
            while count < int(self.trainingCount.text()) + 1:
                print(count)
                ret, im = webcam.read()
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 4)
                for (x, y, w, h) in faces:
                    cv2.rectangle(im, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    face = gray[y:y+h, x:x+w]
                    face_resize = cv2.resize(face, (width, height))
                    cv2.imwrite(os.path.join(path, "{}.png".format(count)), face_resize)
                count += 1
                cv2.imshow("OpenCV", im)
                key = cv2.waitKey(10)
                if key == 27:
                    break
            webcam.release()
            cv2.destroyAllWindows()
            QMessageBox.information(self, "Training Wajah Berhasil", "Training wajah telah selesai.")
            self.traineeName.setText("")
            self.trainingCount.setText("100")







def main():
    app = QApplication(sys.argv)
    window = MainApp() #Ini untuk Window yang digunakan Main APP
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()


