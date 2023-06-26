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
        self.REPORTSLINK2.clicked.connect(self.reports2)
        self.TRAININGBACK.clicked.connect(self.tampilHalamanUtama)
        self.ATTENDANCEBACK.clicked.connect(self.tampilHalamanUtama)
        self.ATTENDANCEBACK2.clicked.connect(self.tampilHalamanUtama)
        self.REPORTSBACK.clicked.connect(self.tampilHalamanUtama)
        self.REPORTSBACK_2.clicked.connect(self.tampilHalamanUtama)
        self.TRAININGBUTTON.clicked.connect(self.start_training)
        self.RECORD.clicked.connect(self.record_attendance)
        self.RECORD2.clicked.connect(self.record_mahasiswa)
        self.dateEdit.setDate(date.today())
        self.dateEdit.dateChanged.connect(self.selectedDateReports)
        self.dateEdit_2.setDate(date.today())
        self.dateEdit_2.dateChanged.connect(self.selectedDateReports2)
        self.tabWidget.setStyleSheet("QTabWidget::pane{border:0}")






        # DATABASE UTK DOSEN
        try: 
            con = sqlite3.connect("face-reco.db")
            con.execute("CREATE TABLE IF NOT EXISTS attendance(attendanceid INTEGER, name Text, attendancedate TEXT)")
            con.commit()
            print("Tabel Berhasil Dibuat")
        except:
            print("Terdapat Error di Database")


        # DATABASE UTK Mahasiswa
        try:
            conn = sqlite3.connect("face-reco-mhsw.db")
            conn.execute("CREATE TABLE IF NOT EXISTS attendancemhsw(attendanceid INTEGER, name Text, attendancedate Text)")
            conn.commit()
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

    #-------Tabel Dosen--------#
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
               

        self.REPORTS.setHorizontalHeaderLabels(["Id", "Name", "Hari/Tanggal", "Waktu"])
        self.REPORTS.setColumnWidth(0,10)
        self.REPORTS.setColumnWidth(1,110)
        self.REPORTS.setColumnWidth(2,70)
        self.REPORTS.verticalHeader().setVisible(False)


    #-------Tabel Mahasiswa--------#
    def reports2(self):
        self.tabWidget.setCurrentIndex(6)
        self.REPORTS_2.setRowCount(0)
        self.REPORTS_2.clear()
        con = sqlite3.connect("face-reco-mhsw.db") #fetching data dri database ke tabel
        cursor = con.execute("SELECT * FROM attendancemhsw")
        result = cursor.fetchall()

        self.REPORTS_2.setColumnCount(len(result[0]))

        for row_number, row_data in enumerate(result):
            self.REPORTS_2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.REPORTS_2.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            
        self.REPORTS_2.setHorizontalHeaderLabels(["Id", "Name", "Hari/Tanggal", "Waktu"])
        self.REPORTS_2.setColumnWidth(0,10)
        self.REPORTS_2.setColumnWidth(1,110)
        self.REPORTS_2.setColumnWidth(2,70)
        self.REPORTS_2.verticalHeader().setVisible(False)

            


     #-------UTK MENAMPILKAN ABSEN DOSEN SESUAI TANGGAL--------#
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
        self.REPORTS.verticalHeader().setVisible(False)


       #-------UTK MENAMPILKAN ABSEN MAHASISWA SESUAI TANGGAL--------#
    def selectedDateReports2(self):
        self.REPORTS_2.setRowCount(0)
        self.REPORTS_2.clear()
        con = sqlite3.connect("face-reco-mhsw.db")
        cursor = con.execute("SELECT * FROM attendancemhsw WHERE attendancedate = '"+ str((self.dateEdit_2.date()).toPyDate()) +"'")
        result = cursor.fetchall()

        self.REPORTS_2.setColumnCount(len(result[0]))  # Mengatur jumlah kolom sesuai dengan jumlah data dalam baris pertama

        for row_number, row_data in enumerate(result):
            self.REPORTS_2.insertRow(row_number)  # Memasukkan baris baru sebelum memasukkan item ke dalam baris tersebut
            for column_number, data in enumerate(row_data):
                self.REPORTS_2.setItem(row_number, column_number, QTableWidgetItem(str(data)))
               

        self.REPORTS_2.setHorizontalHeaderLabels(["Id", "Name", "Date"])
        self.REPORTS_2.verticalHeader().setVisible(False)
            



    #--------PROSES TRAINING WAJAH---------#
    def start_training(self):
        datasets = 'datasets'
        sub_data = self.traineeName.text()
        path = os.path.join(datasets, sub_data)
        if not os.path.isdir(path):
            os.mkdir(path)
            print("Folder Baru Telah dibuat")
            (width, height) = (1280, 720)
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




    #------------ ABSEN DOSEN --------------- #
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
        (width, height) = (1280, 720)
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
                if(prediction[1]<50):
                    confidence = 100 - (prediction[1] / 1)
                    cv2.putText(im, '%s - %.2f%%' % (names[prediction[0]], confidence), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    print(names[prediction[0]])
                    self.currentprocess.setText("Wajah Terdaftar " + names[prediction[0]])
                    attendanceid=0
                    current_time = datetime.now().strftime("%H:%M:%S")
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
                            con.execute("INSERT INTO attendance VALUES("+ str(attendanceid) +",'"+ str(names[prediction[0]]) +"','"+ str(date.today()) + "','" + current_time + "')")
                            con.commit()
                    except:
                        print("Error saat memasukan ke database")
                    print("Berhasil absen ke databse")
                    self.currentprocess.setText(names[prediction[0]] + " Sudah Ter-absen")
                    cnt=0

                else:
                    cnt+=1
                    cv2.putText(im,"Tidak Dikenal",(x-10,y-10),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
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



        #----- ABSEN MAHASISWA ------ #
    def record_mahasiswa(self):
        self.currentprocess_3.setText("Proses Dimulai..Mohon Tunggu..")
        haar_file = 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(haar_file)
        datasets = 'datasets'
        (images,labels,names,id) =([],[],{},0)
        for(subdir,dirs,files) in os.walk(datasets):
            for subdir in dirs: #Perulangan untuk mengambil dataset
                names[id] = subdir
                subjectpath = os.path.join(datasets, subdir)
                for filename in os.listdir(subjectpath):
                    path = subjectpath + "/" + filename
                    label = id
                    images.append(cv2.imread(path,0))
                    labels.append(int(label))
                id += 1
        (images,labels) = [numpy.array(lis) for lis in [images,labels]]
        (width, height) = (1280, 720)
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
                if(prediction[1]<50): #nilai 800 ambang batas yg digunain, semakin kecil ambang batasnya semakin ketat kriteria pengenalan wajahnya
                    confidence = 100 - (prediction[1] / 1)
                    cv2.putText(im, '%s - %.2f%%' % (names[prediction[0]], confidence), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    print(names[prediction[0]])
                    self.currentprocess_3.setText("Wajah Terdaftar " + names[prediction[0]] + " - %.2f%%" % confidence)
                    attendanceid =0
                    current_time = datetime.now().strftime("%H:%M:%S")
                    available = False
                    try:
                        connections = sqlite3.connect("face-reco-mhsw.db")
                        cursor = connections.execute("SELECT MAX(attendanceid) from attendancemhsw")
                        result = cursor.fetchall()
                        if result:
                            for maxid in result:
                                attendanceid = int(maxid[0])+1
                                
                    except:
                        attendanceid=1
                    print(attendanceid)

                    try: #INI JIKA MAHASISWA SUDAH TERDAFTAR DI DATABASE /ABSEN DI HARI INI MAKA GABISA KE ABSEN LG
                        conn = sqlite3.connect("face-reco-mhsw.db")
                        cursor = conn.execute("SELECT * FROM attendancemhsw WHERE name='"+ str(names[prediction[0]]) +"' and attendancedate = '"+ str(date.today()) +"'")
                        result = cursor.fetchall()
                        if result:
                            available=True
                        if(available==False):
                            conn.execute("INSERT INTO attendancemhsw VALUES("+ str(attendanceid) +",'"+ str(names[prediction[0]]) +"','"+ str(date.today()) + "','" + current_time + "')")
                            conn.commit()
                    except:
                         print("Error saat memasukan ke database")
                    print("Berhasil absen ke databse")
                    self.currentprocess_3.setText(names[prediction[0]] + " Sudah Ter-absen")
                    cnt=0


                else:
                    cnt+=1
                    cv2.putText(im,"Wajah Tidak Dikenal",(x-10,y-10),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
                    if(cnt>100):
                        print("Wajah tidak dikenal")
                        self.currentprocess_3.setText("Wajah Tidak Dikenal")
                        cv2.imwrite("Unknown.jpg",im)
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


