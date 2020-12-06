# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viva2.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets
import threading
import os
from googleapiclient.http import MediaFileUpload
from Google import Create_Service
import random
from record import start_AVrecording, stop_AVrecording, file_manager
stat=False

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
folder_id = '1o7VdLH6feRK9z6NzaDYef87Mtcclgetb'
mime_types = ['video/x-msvideo']

class Ui_SecondWindow(object):
    def __init__(self, message):
        self.message = message
        self.stat=False
        self.buttonClicked = 0
        self.recordStat = True
        file_manager(self.message)
        start_AVrecording(self.message)
        list = [1, 2, 3, 4, 5]
        setN = random.sample(list, 1)[0]
        self.loadQuestions(setN)

    def start_the_thread(self):
        t1 = threading.Thread(target=self.timer, args=())
        t1.start()
    def timer(self):
        i=120
        self.lcdNumber.show()
        self.lcdNumber.display(i)
        while self.stat and i > 0:
            sleep(1)  # waits 120 seconds
            self.lcdNumber.display(i)
            i-=1
        print('out of loop')
        print(self.buttonClicked)
        print(i)
        if self.buttonClicked < 4 and i == 0:
            self.startExam()
    def loadQuestions(self, serial):
        fName = str(serial) + '.txt'
        file = open(fName, "r")
        self.listQ = []
        for line in file:
            self.listQ.append(line)

    def startExam(self):
        _translate = QtCore.QCoreApplication.translate

        if self.buttonClicked == 0:
            self.stat = True
            self.start_the_thread()
            self.pushButton.setText(_translate("SecondWindow", "Next"))
            self.label_3.setText(_translate("SecondWindow", str(self.buttonClicked+1) + '. ' + str(self.listQ[self.buttonClicked])))
        elif self.buttonClicked == 1:
            self.stat = False
            sleep(2)
            self.stat = True
            self.start_the_thread()
            self.label_3.setText(_translate("SecondWindow", str(self.buttonClicked+1) + '. ' + str(self.listQ[self.buttonClicked])))
        elif self.buttonClicked == 2:
            self.stat = False
            sleep(2)
            self.stat = True
            self.start_the_thread()
            # self.label_3.setText(_translate("SecondWindow", str(random.sample(self.listQ,1)[0])))
            self.label_3.setText(_translate("SecondWindow", str(self.buttonClicked+1) + '. ' + str(self.listQ[self.buttonClicked])))
            self.pushButton.setText(_translate("SecondWindow", "End ViVa"))
        elif self.buttonClicked == 3:
            self.stat = False
            sleep(2)
            stop_AVrecording(self.message)
            f = self.message + '.avi'
            file_metadata = {
                'name': f,
                'parents': [folder_id]
            }
            wd = os.getcwd() + '\{0}'
            media = MediaFileUpload(wd.format(f), mimetype=mime_types[0])
            sleep(30)
            service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            self.pushButton.show()
            self.pushButton.setText(_translate("SecondWindow", "Log Out"))
            self.label_3.setText(
                _translate("SecondWindow", "Congratulations! You have completed your viva successfully"))
        elif self.buttonClicked == 4:
            sys.exit()
        self.buttonClicked += 1

    def setupUi(self, SecondWindow):
        SecondWindow.setObjectName("SecondWindow")
        SecondWindow.resize(919, 388)
        self.centralwidget = QtWidgets.QWidget(SecondWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 40, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(350, 50, 21, 261))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(780, 250, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.startExam)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 80, 301, 201))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("snapshots/kaiser.jpg"))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(390, 50, 481, 121))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        SecondWindow.setCentralWidget(self.centralwidget)
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(770, 0, 81, 41))
        self.lcdNumber.setObjectName("lcdNumber")
        SecondWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SecondWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 919, 26))
        self.menubar.setObjectName("menubar")
        self.menuViva_Exam_Management = QtWidgets.QMenu(self.menubar)
        self.menuViva_Exam_Management.setObjectName("menuViva_Exam_Management")
        SecondWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SecondWindow)
        self.statusbar.setObjectName("statusbar")
        SecondWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuViva_Exam_Management.menuAction())

        self.retranslateUi(SecondWindow)
        QtCore.QMetaObject.connectSlotsByName(SecondWindow)

    def retranslateUi(self, SecondWindow):
        _translate = QtCore.QCoreApplication.translate
        SecondWindow.setWindowTitle(_translate("SecondWindow", "Viva Exam Management"))
        self.label.setText(_translate("SecondWindow", self.message))
        self.pushButton.setText(_translate("SecondWindow", "Start ViVa"))
        self.lcdNumber.hide()
        image = self.message + ".jpg"
        wd = os.getcwd()
        os.chdir(wd + '\Snapshots')
        self.label_2.setPixmap(QtGui.QPixmap(image))
        os.chdir(wd)




if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--message', required=True,
                        help='name of the userid')
    args = parser.parse_args()
    app = QtWidgets.QApplication(sys.argv)
    SecondWindow = QtWidgets.QMainWindow()
    ui = Ui_SecondWindow(args.message)
    ui.setupUi(SecondWindow)
    SecondWindow.show()
    sys.exit(app.exec_())