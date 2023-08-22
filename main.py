from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import pickle
import sys


class Student:
    # student array
    students = [[None for i in range(1)] for j in range(373)]

    def __init__(self, firstName, lastName, studentNum, gpa, subject):
        self.firstName = firstName
        self.lastName = lastName
        self.studentNum = studentNum
        self.gpa = gpa
        self.subject = subject

    def __hash__(self):
        # calculate key and insert std in array with the key
        part1 = int(self.studentNum[:6])
        mod1 = part1 % 373
        part2 = int(self.studentNum[6:])
        mod2 = part2 % 373
        key = (mod1 + mod2) % 373
        # add student into array
        if self.students[key][0] is None:
            Student.students[key][0] = self
        else:
            Student.students[key].append(self)
        return key

    def remove(self, key):
        if len(Student.students[key]) == 1:
            Student.students[key][0] = None
        else:
            for i in len(Student.students[key]):
                if self.studentNum == Student.students[key][i]:
                    Student.students[key].pop(i)


class Node:
    def __init__(self, data):
        self.data = data
        self.subNode = [None] * 10
        self.flag = False

    def hasSubNode(self):
        for x in self.subNode:
            if x is not None:
                return True
        return False


class trieTree:
    def __init__(self):
        self.root = Node(None)

    def search(self, data):
        current = self.root
        for i in range(len(data)):
            if current.subNode[int(data[i])] is None:
                return None
            else:
                current = current.subNode[int(data[i])]
            if current.flag and i == len(data) - 1:
                return current.data

    def insert(self, data, key):
        current = self.root
        for i in range(len(data)):
            if current.subNode[int(data[i])] is None:
                current.subNode[int(data[i])] = Node(None)

            current = current.subNode[int(data[i])]
            if i == len(data) - 1:
                current.flag = True
                current.data = key

    def delete(self, node, data, i):
        if node is None:
            return None
        # if its the last element of data
        if i == len(data):
            # if this node is the end of num
            if node.flag:
                node.flag = False
            # if node doesnt have any sub nodes (is not the prefix of a num)
            if not node.hasSubNode():
                node = None

            return node

        # if node is not the lost element data
        index = int(data[i])
        node.subNode[index] = self.delete(node.subNode[index], data, i + 1)

        # if node doesnt have any sub node and is not end of a num
        if not node.hasSubNode() and not node.flag:
            node = None

        return node

    def suggestionsRec(self, node, num, l):
        # Method to recursively traverse the trie
        # and return a whole word.
        if node.flag:
            l.append(num)

        for i in range(len(node.subNode)):
            if node.subNode[i] is None:
                continue
            self.suggestionsRec(node.subNode[i], num + str(i), l)


# submenu is the things user can do after searching  student
class subMenu(object):
    def __init__(self):
        self.window = QtWidgets.QMainWindow()

    # ui creator
    def setupUi(self, Form, std, key):
        Form.setObjectName("Form")
        Form.resize(500, 400)
        Form.setStyleSheet("background-color: rgb(170, 255, 127)")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(170, 180, 171, 181))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.showProfileButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showProfileButton.sizePolicy().hasHeightForWidth())
        self.showProfileButton.setSizePolicy(sizePolicy)
        self.showProfileButton.setStyleSheet("background-color:white\n")
        self.showProfileButton.setObjectName("showProfileButton")
        self.showProfileButton.clicked.connect(lambda: switch.subMenuToStudentProfile(std, key))
        self.verticalLayout.addWidget(self.showProfileButton)
        self.editStudentButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.editStudentButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editStudentButton.sizePolicy().hasHeightForWidth())
        self.editStudentButton.setSizePolicy(sizePolicy)
        self.editStudentButton.setStyleSheet("background-color:white")
        self.editStudentButton.setObjectName("editStudentButton")
        self.editStudentButton.clicked.connect(lambda: switch.subMenuToEditStudent(std, key))
        self.verticalLayout.addWidget(self.editStudentButton)
        self.removeStudentButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removeStudentButton.sizePolicy().hasHeightForWidth())
        self.removeStudentButton.setSizePolicy(sizePolicy)
        self.removeStudentButton.setStyleSheet("background-color:white")
        self.removeStudentButton.setObjectName("removeStudentButton")
        self.removeStudentButton.clicked.connect(lambda: self.removeStudent(std, key))
        self.verticalLayout.addWidget(self.removeStudentButton)
        self.exitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exitButton.sizePolicy().hasHeightForWidth())
        self.exitButton.setSizePolicy(sizePolicy)
        self.exitButton.setStyleSheet("background-color: white")
        self.exitButton.setObjectName("exitButton")
        self.exitButton.clicked.connect(lambda: switch.subMenuToMenu())
        self.verticalLayout.addWidget(self.exitButton)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(190, 20, 131, 131))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("img/user.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Sub Menu"))
        self.showProfileButton.setText(_translate("Form", "Show Profile"))
        self.editStudentButton.setText(_translate("Form", "Edit Student"))
        self.removeStudentButton.setText(_translate("Form", "Remove Student"))
        self.exitButton.setText(_translate("Form", "Exit to Menu "))

    def removeStudent(self, std, key):
        tree.delete(tree.root, std.studentNum, 0)
        std.remove(key)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("The student removed successfully!")
        msg.setWindowTitle("Information Message")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()
        switch.subMenuToMenu()


# shows student profile after search
class studentProfile(object):
    def __init__(self):
        self.window = QtWidgets.QMainWindow()

    def setupUi(self, Form, std, key):
        Form.setObjectName("Form")
        Form.resize(500, 400)
        Form.setStyleSheet("background-color: rgb(170, 255, 127)")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(70, 160, 95, 161))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.firstnameLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.firstnameLabel.setFont(font)
        self.firstnameLabel.setObjectName("firstnameLabel")
        self.verticalLayout_2.addWidget(self.firstnameLabel)
        self.lastnameLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lastnameLabel.setFont(font)
        self.lastnameLabel.setObjectName("lastnameLabel")
        self.verticalLayout_2.addWidget(self.lastnameLabel)
        self.studentNumberLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.studentNumberLabel.setFont(font)
        self.studentNumberLabel.setObjectName("studentNumberLabel")
        self.verticalLayout_2.addWidget(self.studentNumberLabel)
        self.GPALabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.GPALabel.setFont(font)
        self.GPALabel.setObjectName("GPALabel")
        self.verticalLayout_2.addWidget(self.GPALabel)
        self.subjectLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.subjectLabel.setFont(font)
        self.subjectLabel.setObjectName("subjectLabel")
        self.verticalLayout_2.addWidget(self.subjectLabel)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(170, 160, 261, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.firstnameField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.firstnameField.setText(std.firstName)
        self.firstnameField.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.firstnameField.sizePolicy().hasHeightForWidth())
        self.firstnameField.setSizePolicy(sizePolicy)
        self.firstnameField.setStyleSheet("background-color:white\n")
        self.firstnameField.setObjectName("firstnameField")
        self.verticalLayout.addWidget(self.firstnameField)
        self.lastnameField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lastnameField.setText(std.lastName)
        self.lastnameField.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lastnameField.sizePolicy().hasHeightForWidth())
        self.lastnameField.setSizePolicy(sizePolicy)
        self.lastnameField.setStyleSheet("background-color:white\n")
        self.lastnameField.setObjectName("lastnameField")
        self.verticalLayout.addWidget(self.lastnameField)
        self.studentNumberField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.studentNumberField.setText(std.studentNum)
        self.studentNumberField.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.studentNumberField.sizePolicy().hasHeightForWidth())
        self.studentNumberField.setSizePolicy(sizePolicy)
        self.studentNumberField.setStyleSheet("background-color:white\n")
        self.studentNumberField.setObjectName("studentNumberField")
        self.verticalLayout.addWidget(self.studentNumberField)
        self.GPAField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.GPAField.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GPAField.sizePolicy().hasHeightForWidth())
        self.GPAField.setSizePolicy(sizePolicy)
        self.GPAField.setStyleSheet("background-color:white\n")
        self.GPAField.setObjectName("GPAField")
        self.GPAField.setText(std.gpa)
        self.verticalLayout.addWidget(self.GPAField)
        self.subjectField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.subjectField.setText(std.subject)
        self.subjectField.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjectField.sizePolicy().hasHeightForWidth())
        self.subjectField.setSizePolicy(sizePolicy)
        self.subjectField.setStyleSheet("background-color:white\n")
        self.subjectField.setObjectName("subjectField")
        self.verticalLayout.addWidget(self.subjectField)
        self.backButton = QtWidgets.QPushButton(Form)
        self.backButton.setGeometry(QtCore.QRect(220, 340, 81, 31))
        self.backButton.setStyleSheet("background-color: white")
        self.backButton.setObjectName("backButton")
        self.backButton.clicked.connect(lambda: switch.studentProfileToSubMenu(std, key))
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(190, 20, 121, 121))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("img/user.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.firstnameLabel.setText(_translate("Form", "Firstname:"))
        self.lastnameLabel.setText(_translate("Form", "Lastname: "))
        self.studentNumberLabel.setText(_translate("Form", "Student Number:"))
        self.GPALabel.setText(_translate("Form", "GPA: "))
        self.subjectLabel.setText(_translate("Form", "Subject: "))
        self.backButton.setText(_translate("Form", "Back"))


# edit student after search
class editStudentData(object):
    def __init__(self):
        self.window = QtWidgets.QMainWindow()

    def setupUi(self, Form, std, key):
        Form.setObjectName("Form")
        Form.resize(500, 400)
        Form.setStyleSheet("background-color: rgb(170, 255, 127)")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(70, 150, 95, 161))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.firstnameLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.firstnameLabel.setFont(font)
        self.firstnameLabel.setObjectName("firstnameLabel")
        self.verticalLayout_2.addWidget(self.firstnameLabel)
        self.lastnameLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lastnameLabel.setFont(font)
        self.lastnameLabel.setObjectName("lastnameLabel")
        self.verticalLayout_2.addWidget(self.lastnameLabel)
        self.studentNumberLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.studentNumberLabel.setFont(font)
        self.studentNumberLabel.setObjectName("studentNumberLabel")
        self.verticalLayout_2.addWidget(self.studentNumberLabel)
        self.GPALabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.GPALabel.setFont(font)
        self.GPALabel.setObjectName("GPALabel")
        self.verticalLayout_2.addWidget(self.GPALabel)
        self.subjectLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.subjectLabel.setFont(font)
        self.subjectLabel.setObjectName("subjectLabel")
        self.verticalLayout_2.addWidget(self.subjectLabel)
        self.cancelButton = QtWidgets.QPushButton(Form)
        self.cancelButton.setGeometry(QtCore.QRect(160, 330, 91, 31))
        self.cancelButton.setStyleSheet("background-color:white\n")
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(lambda: switch.editStudentToSubMenu(std, key))
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(170, 150, 261, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.firstnameField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.firstnameField.setText(std.firstName)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.firstnameField.sizePolicy().hasHeightForWidth())
        self.firstnameField.setSizePolicy(sizePolicy)
        self.firstnameField.setStyleSheet("background-color:white\n")
        self.firstnameField.setObjectName("firstnameField")
        self.verticalLayout.addWidget(self.firstnameField)
        self.lastnameField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lastnameField.setText(std.lastName)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lastnameField.sizePolicy().hasHeightForWidth())
        self.lastnameField.setSizePolicy(sizePolicy)
        self.lastnameField.setStyleSheet("background-color:white\n")
        self.lastnameField.setObjectName("lastnameField")
        self.verticalLayout.addWidget(self.lastnameField)
        self.studentNumberField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.studentNumberField.sizePolicy().hasHeightForWidth())
        self.studentNumberField.setSizePolicy(sizePolicy)
        self.studentNumberField.setStyleSheet("background-color:white\n")
        self.studentNumberField.setObjectName("studentNumberField")
        self.studentNumberField.setText(std.studentNum)
        self.verticalLayout.addWidget(self.studentNumberField)
        self.GPAField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GPAField.sizePolicy().hasHeightForWidth())
        self.GPAField.setSizePolicy(sizePolicy)
        self.GPAField.setStyleSheet("background-color:white\n")
        self.GPAField.setObjectName("GPAField")
        self.GPAField.setText(std.gpa)
        self.verticalLayout.addWidget(self.GPAField)
        self.subjectField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjectField.sizePolicy().hasHeightForWidth())
        self.subjectField.setSizePolicy(sizePolicy)
        self.subjectField.setStyleSheet("background-color:white\n")
        self.subjectField.setObjectName("subjectField")
        self.subjectField.setText(std.subject)
        self.verticalLayout.addWidget(self.subjectField)
        self.submitButton = QtWidgets.QPushButton(Form)
        self.submitButton.setGeometry(QtCore.QRect(270, 330, 91, 31))
        self.submitButton.setStyleSheet("background-color:white\n")
        self.submitButton.setObjectName("submitButton")
        self.submitButton.clicked.connect(lambda: self.editStudent(std, key))
        self.editIcon = QtWidgets.QLabel(Form)
        self.editIcon.setGeometry(QtCore.QRect(210, 40, 91, 81))
        self.editIcon.setText("")
        self.editIcon.setPixmap(QtGui.QPixmap("img/edit.png"))
        self.editIcon.setScaledContents(True)
        self.editIcon.setObjectName("editIcon")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Edit Student"))
        self.firstnameLabel.setText(_translate("Form", "Firstname:"))
        self.lastnameLabel.setText(_translate("Form", "Lastname: "))
        self.studentNumberLabel.setText(_translate("Form", "Student Number:"))
        self.GPALabel.setText(_translate("Form", "GPA: "))
        self.subjectLabel.setText(_translate("Form", "Subject: "))
        self.cancelButton.setText(_translate("Form", "Cancel"))
        self.submitButton.setText(_translate("Form", "Submit"))

    # edit after submit button clicked
    def editStudent(self, std, key):
        # get inputs
        stdNum = self.studentNumberField.text()
        stdFirstName = self.firstnameField.text()
        stdLastName = self.lastnameField.text()
        stdGPA = self.GPAField.text()
        stdSub = self.subjectField.text()
        # edit with no student umber change
        if std.studentNum == stdNum:
            std.firstName = stdFirstName
            std.lastName = stdLastName
            std.gpa = stdGPA
            std.subject = stdSub
            # success message
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("The student edited successfully!")
            msg.setWindowTitle("Information Message")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
            switch.editStudentToSubMenu(std, key)
        # edit with student number change
        else:
            if tree.search(stdNum) is not None:
                # unavailable std num message
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("This student number is not available!!")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
            else:
                # delete previous student
                tree.delete(tree.root, std.studentNum, 0)
                std.remove(key)
                # creat new student with new data
                std = Student(stdFirstName, stdLastName, stdNum, stdGPA, stdSub)
                key = hash(std)
                tree.insert(stdNum, key)
                # success message
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("The student edited successfully!")
                msg.setWindowTitle("Information Message")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                switch.editStudentToSubMenu(std, key)


# search student with student  num and shows suggestions
class searchStudent(object):
    def __init__(self):
        self.window = QtWidgets.QMainWindow()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 400)
        Form.setStyleSheet("background-color: rgb(170, 255, 127)")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(220, 15, 71, 71))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("img/search.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(80, 85, 261, 30))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.searchLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.searchLabel.setFont(font)
        self.searchLabel.setObjectName("searchLabel")
        self.horizontalLayout.addWidget(self.searchLabel)
        self.searchField = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.searchField.setStyleSheet("background-color:white")
        self.searchField.setObjectName("searchField")
        self.horizontalLayout.addWidget(self.searchField)
        self.searchButton = QtWidgets.QPushButton(Form)
        self.searchButton.setGeometry(QtCore.QRect(360, 80, 51, 41))
        self.searchButton.setStyleSheet("background-color:white")
        self.searchButton.setObjectName("searchButton")
        self.searchButton.clicked.connect(lambda: self.search())
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setStyleSheet("background-color:white")
        self.listWidget.setGeometry(QtCore.QRect(100, 140, 291, 191))
        self.listWidget.setObjectName("listWidget")
        self.backButton = QtWidgets.QPushButton(Form)
        self.backButton.setGeometry(QtCore.QRect(210, 340, 81, 31))
        self.backButton.setStyleSheet("background-color: white")
        self.backButton.setObjectName("backButton")
        self.backButton.clicked.connect(lambda: switch.searchStudentToMenu())

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Search Student"))
        self.searchLabel.setText(_translate("Form", "Student Number:"))
        self.searchButton.setText(_translate("Form", "Search"))
        self.backButton.setText(_translate("Form", "Back"))

    # search after search button clicked
    def search(self):
        # std num input
        stdNum = self.searchField.text()
        # if user entered complete student number
        if len(stdNum) == 12:
            key = tree.search(stdNum)
            if key is None:
                # warning message for not finding any student number
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("No student with this student number!!")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
            else:
                # find student with key (due to collision)
                for s in Student.students[key]:
                    if s.studentNum == stdNum:
                        break
                switch.searchStudentToSubMenu(s, key)
        # if user entered a prefix of student number
        else:
            # find student numbers with given prefix
            self.suggestStudentNum(stdNum)

    # suggest student numbers due to given prefix
    def suggestStudentNum(self, stdNum):
        # list of suggestions
        l = []
        existedPrefix = False
        current = tree.root
        # check if prefix exists in tree
        for i in range(len(stdNum)):
            if current.subNode[int(stdNum[i])] is None:
                break
            else:
                current = current.subNode[int(stdNum[i])]
            if i == len(stdNum) - 1:
                existedPrefix = True
        # warn that there is no std num with given prefix
        if not existedPrefix:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No student number wih given prefix!!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
        # creat student num strings with recursive function if exist
        else:
            tree.suggestionsRec(current, stdNum, l)
            # warn that there is no std num with given prefix
            if len(l) == 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("No student number wih given prefix!!")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
            else:
                # clear previous data
                self.listWidget.clear()
                # add each student num to list widget
                for i in range(len(l)):
                    self.listWidget.addItem("\n" + str(i + 1) + "." + l[i])


# add student
class addStudent(object):
    def __init__(self):
        self.window = QtWidgets.QMainWindow()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 400)
        Form.setStyleSheet("background-color:rgb(170, 255, 127)")
        self.addUserIcon = QtWidgets.QLabel(Form)
        self.addUserIcon.setGeometry(QtCore.QRect(190, 20, 111, 131))
        self.addUserIcon.setText("")
        self.addUserIcon.setPixmap(QtGui.QPixmap("img/addUser.png"))
        self.addUserIcon.setScaledContents(True)
        self.addUserIcon.setObjectName("addUserIcon")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(170, 170, 261, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.firstnameField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.firstnameField.sizePolicy().hasHeightForWidth())
        self.firstnameField.setSizePolicy(sizePolicy)
        self.firstnameField.setStyleSheet("background-color:white\n")
        self.firstnameField.setObjectName("firstnameField")
        self.verticalLayout.addWidget(self.firstnameField)
        self.lastnameField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lastnameField.sizePolicy().hasHeightForWidth())
        self.lastnameField.setSizePolicy(sizePolicy)
        self.lastnameField.setStyleSheet("background-color:white\n")
        self.lastnameField.setObjectName("lastnameField")
        self.verticalLayout.addWidget(self.lastnameField)
        self.studentNumberField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.studentNumberField.sizePolicy().hasHeightForWidth())
        self.studentNumberField.setSizePolicy(sizePolicy)
        self.studentNumberField.setStyleSheet("background-color:white\n")
        self.studentNumberField.setObjectName("studentNumberField")
        self.verticalLayout.addWidget(self.studentNumberField)
        self.GPAField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.GPAField.sizePolicy().hasHeightForWidth())
        self.GPAField.setSizePolicy(sizePolicy)
        self.GPAField.setStyleSheet("background-color:white\n")
        self.GPAField.setObjectName("GPAField")
        self.verticalLayout.addWidget(self.GPAField)
        self.subjectField = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subjectField.sizePolicy().hasHeightForWidth())
        self.subjectField.setSizePolicy(sizePolicy)
        self.subjectField.setStyleSheet("background-color:white\n")
        self.subjectField.setObjectName("subjectField")
        self.verticalLayout.addWidget(self.subjectField)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(70, 170, 95, 161))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.firstnameLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.firstnameLabel.setFont(font)
        self.firstnameLabel.setObjectName("firstnameLabel")
        self.verticalLayout_2.addWidget(self.firstnameLabel)
        self.lastnameLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lastnameLabel.setFont(font)
        self.lastnameLabel.setObjectName("lastnameLabel")
        self.verticalLayout_2.addWidget(self.lastnameLabel)
        self.studentNumberLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.studentNumberLabel.setFont(font)
        self.studentNumberLabel.setObjectName("studentNumberLabel")
        self.verticalLayout_2.addWidget(self.studentNumberLabel)
        self.GPALabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.GPALabel.setFont(font)
        self.GPALabel.setObjectName("GPALabel")
        self.verticalLayout_2.addWidget(self.GPALabel)
        self.subjectLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.subjectLabel.setFont(font)
        self.subjectLabel.setObjectName("subjectLabel")
        self.verticalLayout_2.addWidget(self.subjectLabel)
        self.submitButton = QtWidgets.QPushButton(Form)
        self.submitButton.setGeometry(QtCore.QRect(270, 350, 91, 31))
        self.submitButton.setStyleSheet("background-color:white\n")
        self.submitButton.setObjectName("submitButton")
        self.submitButton.clicked.connect(lambda: self.submit())
        self.cancelButton = QtWidgets.QPushButton(Form)
        self.cancelButton.setGeometry(QtCore.QRect(160, 350, 91, 31))
        self.cancelButton.setStyleSheet("background-color:white\n")
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(lambda: switch.addStudentToMenu())

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Add Student"))
        self.firstnameLabel.setText(_translate("Form", "Firstname:"))
        self.lastnameLabel.setText(_translate("Form", "Lastname: "))
        self.studentNumberLabel.setText(_translate("Form", "Student Number:"))
        self.GPALabel.setText(_translate("Form", "GPA: "))
        self.subjectLabel.setText(_translate("Form", "Subject: "))
        self.submitButton.setText(_translate("Form", "Submit"))
        self.cancelButton.setText(_translate("Form", "Cancel"))

    # add student after submit button clicked
    def submit(self):
        # empty field check
        if not (self.firstnameField.text() and self.lastnameField.text() and self.studentNumberField.text()
                and self.subjectField.text() and self.GPAField.text()):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Fill out all fields!!")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.exec_()
        else:
            stdNum = self.studentNumberField.text()
            if tree.search(stdNum) is not None:
                # unavailable std num message
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("This student number is not available!!")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
            else:
                stdFirstName = self.firstnameField.text()
                stdLastName = self.lastnameField.text()
                stdGPA = self.GPAField.text()
                stdSub = self.subjectField.text()
                std = Student(stdFirstName, stdLastName, stdNum, stdGPA, stdSub)
                key = hash(std)
                tree.insert(stdNum, key)
                # success message
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("The student added successfully!")
                msg.setWindowTitle("Information Message")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.exec_()
                switch.addStudentToMenu()


# menu
class menu(object):
    def __init__(self):
        self.window = QtWidgets.QMainWindow()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(170, 255, 127)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(170, 200, 171, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addStudentButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addStudentButton.sizePolicy().hasHeightForWidth())
        self.addStudentButton.setSizePolicy(sizePolicy)
        self.addStudentButton.setStyleSheet("background-color:white\n")
        self.addStudentButton.setObjectName("addStudentButton")
        self.addStudentButton.clicked.connect(lambda: switch.menuToAddStudent())
        self.verticalLayout.addWidget(self.addStudentButton)
        self.searchStudentButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.searchStudentButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchStudentButton.sizePolicy().hasHeightForWidth())
        self.searchStudentButton.setSizePolicy(sizePolicy)
        self.searchStudentButton.setStyleSheet("background-color:white")
        self.searchStudentButton.setObjectName("searchStudentButton")
        self.searchStudentButton.clicked.connect(lambda: switch.menuToSearchStudent())
        self.verticalLayout.addWidget(self.searchStudentButton)
        self.exitButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exitButton.sizePolicy().hasHeightForWidth())
        self.exitButton.setSizePolicy(sizePolicy)
        self.exitButton.setStyleSheet("background-color:white")
        self.exitButton.setObjectName("exitButton")
        self.exitButton.clicked.connect(lambda: self.exitApp())
        self.verticalLayout.addWidget(self.exitButton)
        self.userIcon = QtWidgets.QLabel(self.centralwidget)
        self.userIcon.setGeometry(QtCore.QRect(180, 10, 151, 151))
        self.userIcon.setText("")
        self.userIcon.setPixmap(QtGui.QPixmap("img/user.png"))
        self.userIcon.setScaledContents(True)
        self.userIcon.setObjectName("userIcon")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Menu"))
        self.addStudentButton.setText(_translate("MainWindow", "Add Student"))
        self.searchStudentButton.setText(_translate("MainWindow", "Search Student"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))

    def exitApp(self):
        writeTree = open("tree.pkl", "wb")
        pickle.dump(tree, writeTree)
        writeTree.close()
        writeStd = open("student.pkl", "wb")
        pickle.dump(Student.students, writeStd)
        writeStd.close()
        exit()


# window switcher for changing windows of program
class windowSwitch:
    def __init__(self):
        self.menu = menu()
        self.addStudent = addStudent()
        self.searchStudent = searchStudent()
        self.editStudent = editStudentData()
        self.studentProfile = studentProfile()
        self.subMenu = subMenu()

    def openMenuWindow(self):
        self.menu.setupUi(self.menu.window)
        self.menu.window.show()

    def menuToAddStudent(self):
        self.menu.window.close()
        self.addStudent.setupUi(self.addStudent.window)
        self.addStudent.window.show()

    def addStudentToMenu(self):
        self.addStudent.window.close()
        self.openMenuWindow()

    def menuToSearchStudent(self):
        self.menu.window.close()
        self.searchStudent.setupUi(self.searchStudent.window)
        self.searchStudent.window.show()

    def searchStudentToMenu(self):
        self.searchStudent.window.close()
        self.openMenuWindow()

    def searchStudentToSubMenu(self, std, key):
        self.searchStudent.window.close()
        self.subMenu.setupUi(self.subMenu.window, std, key)
        self.subMenu.window.show()

    def subMenuToMenu(self):
        self.subMenu.window.close()
        self.openMenuWindow()

    def subMenuToStudentProfile(self, std, key):
        self.subMenu.window.close()
        self.studentProfile.setupUi(self.studentProfile.window, std, key)
        self.studentProfile.window.show()

    def studentProfileToSubMenu(self, std, key):
        self.studentProfile.window.close()
        self.subMenu.setupUi(self.subMenu.window, std, key)
        self.subMenu.window.show()

    def subMenuToEditStudent(self, std, key):
        self.subMenu.window.close()
        self.editStudent.setupUi(self.editStudent.window, std, key)
        self.editStudent.window.show()

    def editStudentToSubMenu(self, std, key):
        self.editStudent.window.close()
        self.subMenu.setupUi(self.subMenu.window, std, key)
        self.subMenu.window.show()


# tree creation
tree = trieTree()
# file read
readTree = open("tree.pkl", "rb")
tree = pickle.load(readTree)
readTree.close()
readStd = open("student.pkl", "rb")
Student.students = pickle.load(readStd)
readStd.close()
# make an app for running program
app = QtWidgets.QApplication(sys.argv)
# creat a window switcher
switch = windowSwitch()
switch.openMenuWindow()
sys.exit(app.exec_())
