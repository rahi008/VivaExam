# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viva1.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
import mysql.connector
import cv2
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
import numpy as np
from viva2 import Ui_SecondWindow

#ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'JPG'}


class Ui_MainWindow(object):

    def predict(self, X_frame, knn_clf=None, model_path=None, distance_threshold=0.5):

        if knn_clf is None and model_path is None:
            raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

        # Load a trained KNN model (if one was passed in)
        if knn_clf is None:
            with open(model_path, 'rb') as f:
                knn_clf = pickle.load(f)

        X_face_locations = face_recognition.face_locations(X_frame)

        # If no faces are found in the image, return an empty result.
        if len(X_face_locations) == 0:
            return []

        # Find encodings for faces in the test image
        faces_encodings = face_recognition.face_encodings(X_frame, known_face_locations=X_face_locations)

        # Use the KNN model to find the best matches for the test face
        closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
        are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

        # Predict classes and remove classifications that aren't within the threshold
        return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

    def show_prediction_labels_on_image(self, frame, predictions):

        pil_image = Image.fromarray(frame)
        draw = ImageDraw.Draw(pil_image)

        for name, (top, right, bottom, left) in predictions:
            # enlarge the predictions for the full sized image.

            # Draw a box around the face using the Pillow module
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

            # There's a bug in Pillow where it blows up with non-UTF-8 text
            # when using the default bitmap font
            name = name.encode("UTF-8")

            # Draw a label with a name below the face
            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

        # Remove the drawing library from memory as per the Pillow docs.
        del draw
        # Save image in open-cv format to be able to show it.

        opencvimage = np.array(pil_image)
        return opencvimage



    def warning(self, title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec()

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="viva"
        )
        mycursor = mydb.cursor()
        query = "select * from examinees where username=%s and password=%s"
        data = mycursor.execute(query, (username, password))
        cap = cv2.VideoCapture(0)
        state=""
        process_this_frame = 29
        if (len(mycursor.fetchall()) > 0):
            while state != username:
                ret, frame = cap.read()

                # Different resizing options can be chosen based on desired program runtime.
                # Image resizing for more stable streaming
                img = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                process_this_frame = process_this_frame + 1
                if process_this_frame % 30 == 0:
                    predictions = self.predict(img, model_path="trained_knn_model.clf")
                    if predictions:
                        x = str(predictions[0])
                        print(x)
                        y = x.split("'")
                        state = y[1]
                        print(state)
                        frame = self.show_prediction_labels_on_image(img, predictions)
                self.frame=frame
            if state == username:
                #self.messagebox("congrats", "you are logged in")
                wd=os.getcwd()
                os.chdir(wd+'\Snapshots')
                filename=username+'.jpg'
                cv2.imwrite(filename, self.frame)
                os.chdir(wd)
                self.message=username
                self.window=QtWidgets.QMainWindow()
                self.ui = Ui_SecondWindow(self.message)
                self.ui.setupUi(self.window)
                MainWindow.hide()
                self.window.show()
                cap.release()
                cv2.destroyAllWindows()
            else:
                self.warning("Alert", "Face Mismatch")
                cap.release()
                cv2.destroyAllWindows()
        else:

            self.warning("Alert", "enter correct details")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(482, 392)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 110, 81, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(90, 200, 67, 17))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(290, 110, 113, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(290, 200, 113, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(310, 280, 89, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.login)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 482, 22))
        self.menubar.setObjectName("menubar")
        self.menuViva_Exam_Management = QtWidgets.QMenu(self.menubar)
        self.menuViva_Exam_Management.setObjectName("menuViva_Exam_Management")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuViva_Exam_Management.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Viva Exam Management"))
        self.label.setText(_translate("MainWindow", "UserName"))
        self.label_2.setText(_translate("MainWindow", "Password"))
        self.pushButton.setText(_translate("MainWindow", "Login"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
