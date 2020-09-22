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
from PySide2.QtWidgets import (QWidget, QPushButton, QFileDialog,
    QLabel, QLineEdit, QMainWindow, QGridLayout, QTableWidget, 
    QTableWidgetItem, QHeaderView, QTableView, QHBoxLayout, 
    QVBoxLayout, QApplication)
from PySide2 import QtGui, QtCore
from PySide2.QtCore import QThread, Signal, Slot
import requests
import youtube_dl
import os
class MyLogger(object):
    def debug(self, msg):
        print(msg)
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)
class DownloadThread(QThread):
    data_downloaded = Signal(object)
    
    def __init__(self, directory, url, row_position):
        super(DownloadThread, self).__init__()
        self.ydl_opts = {
            'logger': MyLogger(),
            'outtmpl': os.path.join(directory,'%(title)s.%(ext)s'),
            'progress_hooks': [self.my_hook],
        }
        self.url = url
        self.row_position = row_position
    def my_hook(self, d):
        filename = d.get('filename').split('/')[-1].split('.')[0]
        self.data_downloaded.emit((filename, d.get('_percent_str', '100%'),
            self.row_position))
    def run(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])
class MainWidget(QWidget):
    
    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.threads = []
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
        self.tableWidget.setColumnCount(2)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, \
            QHeaderView.Stretch)
        self.tableWidget.setColumnWidth(1, 140)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Downloaded"])
        
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
        self.setup_connections()
        self.setLayout(vbox)
    def setup_connections(self):
        self.browse_btn.clicked.connect(self.pick_location)
        self.download_btn.clicked.connect(self.start_download)
    def pick_location(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(self, "Select Folder")
        self.location_input.setText(folder_path)
        return folder_path
    def start_download(self):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setItem(row_position,0, 
            QTableWidgetItem(self.url_input.text()))
        self.tableWidget.setItem(row_position,1, 
            QTableWidgetItem("0%"))
        downloader = DownloadThread(self.location_input.text() or os.getcwd(), 
            self.url_input.text(), row_position)
        downloader.data_downloaded.connect(self.on_data_ready)
        self.threads.append(downloader)
        downloader.start()
    def on_data_ready(self, data):
        self.tableWidget.setItem(data[2],0, QTableWidgetItem(data[0]))
        self.tableWidget.setItem(data[2],1, QTableWidgetItem(data[1]))
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        m_widget = MainWidget(self)
        self.setCentralWidget(m_widget)
        self.setGeometry(300, 300, 700, 350)
        self.setWindowTitle('Buttons')    
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    m_window = MainWindow()
    m_window.show()
    sys.exit(app.exec_())
