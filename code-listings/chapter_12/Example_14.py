"""
Using This Code Example
=========================
The code examples are provided by Yasoob Khalid to help you 
reference Practical Python Projects book. Code samples follow
PEP-0008, with exceptions made for the purposes of improving book
formatting. Example code is provided "as is".
Permissions
============
In general, you may use the code we've provided with this book in your
programs . You do not need to contact us for permission unless you're
reproducing a significant portion of the code and using it in educational
distributions. Examples:
* Writing an education program or book that uses several chunks of code from
    this course requires permission. 
* Selling or distributing a digital package from material taken from this
    book does require permission.
* Answering a question by citing this book and quoting example code does not
    require permission.
Attributions usually include the title, author, publisher and an ISBN. For
example, "Practical Python Projects, by Yasoob Khalid. Copyright 2020 Yasoob."
If you feel your use of code examples falls outside fair use of the permission
given here, please contact me at hi@yasoob.me.
"""

import sys
from PySide2.QtWidgets import (QWidget, QPushButton, 
    QLabel, QLineEdit, QMainWindow, QGridLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QTableView, QHBoxLayout, QVBoxLayout, QApplication)
from PySide2 import QtGui, QtCore
class MainWidget(QWidget):
    
    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.initUI()
        
        
    def initUI(self):
        
        self.logo_label = QLabel(self)
        self.url_label = QLabel(self)
        self.url_label.setText('Url:')
        self.url_input = QLineEdit(self)
        
        self.location_label = QLabel(self)
        self.location_label.setText('Location:')
        self.location_input = QLineEdit(self)
        self.browse_btn = QPushButton("Browse")
        self.download_btn = QPushButton("Download")
        logo = QtGui.QPixmap("logo.png")
        self.logo_label.setPixmap(logo)
        logoBox = QHBoxLayout()
        logoBox.addStretch(1)
        logoBox.addWidget(self.logo_label)
        logoBox.addStretch(1)
        self.tableWidget = QTableWidget()
        #self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.tableWidget.setColumnWidth(1, 140)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Downloaded"])
        
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        self.tableWidget.setItem(rowPosition,0, QTableWidgetItem("Cell (1,1)"))
        self.tableWidget.setItem(rowPosition,1, QTableWidgetItem("Cell (1,2)"))
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.url_label, 0, 0)
        grid.addWidget(self.url_input, 0, 1, 1, 2)
        
        grid.addWidget(self.location_label, 1, 0)
        grid.addWidget(self.location_input, 1, 1)
        grid.addWidget(self.browse_btn, 1, 2)        
        grid.addWidget(self.download_btn, 2, 0, 1, 3)
        vbox = QVBoxLayout()
        vbox.addLayout(logoBox)
        vbox.addLayout(grid)
        vbox.addWidget(self.tableWidget)
        self.setLayout(vbox)
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        m_widget = MainWidget(self)
        self.setCentralWidget(m_widget)
        self.setGeometry(300, 300, 400, 150)
        self.setWindowTitle('Buttons')    
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    m_window = MainWindow()
    m_window.show()
    sys.exit(app.exec_())
