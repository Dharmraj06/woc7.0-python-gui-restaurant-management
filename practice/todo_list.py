from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ToDolist(object):
    def setupUi(self, ToDolist):
        ToDolist.setObjectName("ToDolist")
        ToDolist.resize(431, 399)
        self.centralwidget = QtWidgets.QWidget(ToDolist)
        self.centralwidget.setObjectName("centralwidget")

        self.List_item_pb = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.add_task())
        self.List_item_pb.setGeometry(QtCore.QRect(20, 70, 111, 31))
        self.List_item_pb.setObjectName("List_item_pb")

        self.Delete_item_pb = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.delete_task())
        self.Delete_item_pb.setGeometry(QtCore.QRect(160, 70, 111, 31))
        self.Delete_item_pb.setObjectName("Delete_item_pb")

        self.Clear_list_pb = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.clear_list())
        self.Clear_list_pb.setGeometry(QtCore.QRect(302, 70, 111, 31))
        self.Clear_list_pb.setCheckable(False)
        self.Clear_list_pb.setObjectName("Clear_list_pb")

        self.Add_item = QtWidgets.QLineEdit(self.centralwidget)
        self.Add_item.setGeometry(QtCore.QRect(20, 10, 391, 51))
        self.Add_item.setObjectName("Add_item")

        self.mylist_listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.mylist_listWidget.setGeometry(QtCore.QRect(20, 110, 391, 231))
        self.mylist_listWidget.setObjectName("mylist_listWidget")

        ToDolist.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ToDolist)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 431, 26))
        self.menubar.setObjectName("menubar")
        ToDolist.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ToDolist)
        self.statusbar.setObjectName("statusbar")
        ToDolist.setStatusBar(self.statusbar)

        self.retranslateUi(ToDolist)
        QtCore.QMetaObject.connectSlotsByName(ToDolist)

    # add item to list
    def add_task(self):
        item = self.Add_item.text()  # grabbing the item from the list box
        self.mylist_listWidget.addItem(item)
        # clearing the item box for new item
        self.Add_item.setText("")

    # add item to list
    def delete_task(self):
        # grab the current task
        clicked = self.mylist_listWidget.currentRow()  # this code gives the index of the line selected
        # self.Add_item.setText(str(clicked))
        self.mylist_listWidget.takeItem(clicked)

    def clear_list(self):
        self.mylist_listWidget.clear()

    def retranslateUi(self, ToDolist):
        _translate = QtCore.QCoreApplication.translate
        ToDolist.setWindowTitle(_translate("ToDolist", "MainWindow"))
        self.List_item_pb.setText(_translate("ToDolist", "Add task"))
        self.Delete_item_pb.setText(_translate("ToDolist", "Delete Task"))
        self.Clear_list_pb.setText(_translate("ToDolist", "Clear List"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ToDolist = QtWidgets.QMainWindow()
    ui = Ui_ToDolist()
    ui.setupUi(ToDolist)
    ToDolist.show()
    sys.exit(app.exec_())
