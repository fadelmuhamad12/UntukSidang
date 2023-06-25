from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sys
import sqlite3
from datetime import date, datetime
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
        self.RECORD.clicked.connect(self.record_attendance)
        self.dateEdit.setDate(date.today())
        self.dateEdit.dateChanged.connect(self.selectedDateReports)
        self.tabWidget.setStyleSheet("QTabWidget::pane{border:0}")

        try: 
            con = sqlite3.connect("face-reco.db")
            con.execute("CREATE TABLE IF NOT EXISTS attendance(attendanceid INTEGER, name Text, attendancedate TEXT)")
            con.commit()
            print("Tabel Berhasil Dibuat")
        except:
            print("Terdapat Error di Database")
    





    #-------LOGIN PROSES--------#
    def login(self):
        kataSandi = self.PASSWORD.text()
        if (kataSandi == "1"):
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
        self.currentprocess.setText("Belum Melakukan Absensi")
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

    #-------REPORTS--------#
    def reports(self):
        self.tabWidget.setCurrentIndex(5)
        self.REPORTS.setRowCount(0)
        self.REPORTS.clear()
        con = sqlite3.connect("face-reco.db")
        cursor = con.execute("SELECT * FROM attendance")
        result = cursor.fetchall()

        self.REPORTS.setColumnCount(len(result[0]))  # Mengatur jumlah kolom sesuai dengan jumlah data dalam baris pertama

        for row_number, row_data in enumerate(result):
            self.REPORTS.insertRow(row_number)  # Memasukkan baris baru sebelum memasukkan item ke dalam baris tersebut
            for column_number, data in enumerate(row_data):
                self.REPORTS.setItem(row_number, column_number, QTableWidgetItem(str(data)))
               

        self.REPORTS.setHorizontalHeaderLabels(["Id", "Name", "Date"])
        self.REPORTS.setColumnWidth(0,10)
        self.REPORTS.setColumnWidth(1,150)
        self.REPORTS.setColumnWidth(2,90)
        self.REPORTS.verticalHeader().setVisible(False)



     #-------SEleceted Date Reports--------#
    def selectedDateReports(self):
        self.REPORTS.setRowCount(0)
        self.REPORTS.clear()
        con = sqlite3.connect("face-reco.db")
        cursor = con.execute("SELECT * FROM attendance WHERE attendancedate = '"+ str((self.dateEdit.date()).toPyDate()) +"'")
        result = cursor.fetchall()

        self.REPORTS.setColumnCount(len(result[0]))  # Mengatur jumlah kolom sesuai dengan jumlah data dalam baris pertama

        for row_number, row_data in enumerate(result):
            self.REPORTS.insertRow(row_number)  # Memasukkan baris baru sebelum memasukkan item ke dalam baris tersebut
            for column_number, data in enumerate(row_data):
                self.REPORTS.setItem(row_number, column_number, QTableWidgetItem(str(data)))
               

        self.REPORTS.setHorizontalHeaderLabels(["Id", "Name", "Date"])
        self.REPORTS.setColumnWidth(0,10)
        self.REPORTS.setColumnWidth(1,150)
        self.REPORTS.setColumnWidth(2,90)
        self.REPORTS.verticalHeader().setVisible(False)

            



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
    #             ret ,im = webcam.read()
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

    # Face Recognition #
    def record_attendance(self):
        self.currentprocess.setText("Proses Dimulai..Mohon Tunggu..")
        haar_file = 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(haar_file)
        datasets = "datasets"
        (images,labels,names,id) =([],[],{},0)
        for(subdirs,dirs,files) in os.walk(datasets):
            for subdir in dirs:
                names[id] = subdir
                subjectpath =os.path.join(datasets,subdir)
                for filename in os.listdir(subjectpath):
                    path = subjectpath + "/" + filename 
                    label = id
                    images.append(cv2.imread(path,0)) #ini untuk nambahin nama ke daftar absen
                    labels.append(int(label)) #ini untuk nambahin id ke daftar absen
                id += 1
        (images,labels) = [numpy.array(lis) for lis in [images,labels]]
        print(images,labels) 
        (width, height) = (130,100)
        model = cv2.face.LBPHFaceRecognizer_create() #membuat variabel model dari algoritma LBPH
        model.train(images,labels)
        webcam = cv2.VideoCapture(0)
        cnt = 0
        while True:
            (_,im) = webcam.read()
            gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.3,5) #untuk mendeteksi semua muka yg ada di frame
            for (x,y,w,h) in faces:
                cv2.rectangle(im,(x,y),(x+w,y+h),(255,255,0),2)
                face = gray[y:y+h,x:x+w]
                face_resize = cv2.resize(face,(width,height))
                prediction =  model.predict(face_resize) #ini untuk level of prediction
                cv2.rectangle(im,(x,y),(x+w, y+h),(0,255,0),3)
                if(prediction[1]<800):
                    cv2.putText(im,'%s-%.0f'%(names[prediction[0]],prediction[1]),(x-10,y-10),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
                    print(names[prediction[0]])
                    self.currentprocess.setText("Wajah Terdaftar " + names[prediction[0]])
                    attendanceid=0
                    available = False
                    try:
                        connection = sqlite3.connect('face-reco.db')
                        cursor = connection.execute("SELECT MAX(attendanceid) from attendance")
                        result = cursor.fetchall()
                        if result:
                            for maxid in result:
                                attendanceid = int(maxid[0])+1
                    except:
                        attendanceid=1
                    print(attendanceid)
                   

                    try:
                        con = sqlite3.connect("face-reco.db")
                        cursor = con.execute("SELECT * FROM attendance WHERE name='"+ str(names[prediction[0]]) +"' and attendancedate = '"+ str(date.today()) +"'")
                        result = cursor.fetchall()
                        if result:
                            available=True
                        if(available==False):
                            con.execute("INSERT INTO attendance VALUES("+ str(attendanceid) +",'"+ str(names[prediction[0]]) +"','"+ str(date.today()) +"')")
                            con.commit()
                    except:
                        print("Error saat memasukan ke database")
                    print("Berhasil absen ke databse")
                    self.currentprocess.setText(names[prediction[0]] + " Sudah Ter-absen")
                    cnt=0

                else:
                    cnt+=1
                    cv2.putText(im,"Tidak Dikenal",(x-10,y-10),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
                    if(cnt>100):
                        print("Wajah Tidak Dikenal")
                        self.currentprocess.setText("Wajah Tidak Dikenal" + names[prediction[0]])
                        cv2.imwrite("unKnown.jpg",im)
                        cnt=0
            cv2.imshow("Face Recognition",im)
            key = cv2.waitKey(10)
            if key==27:
                break
        webcam.release()
        cv2.destroyAllWindows()















def main():
    app = QApplication(sys.argv)
    window = MainApp() #Ini untuk Window yang digunakan Main APP
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()


