import sys
from PySide2.QtWidgets import (QWidget, QPushButton, 
    QLabel, QLineEdit, QMainWindow,
    QHBoxLayout, QVBoxLayout, QApplication)


class MainWidget(QWidget):
    
    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.initUI()
        
        
    def initUI(self):
        
        self.name_label = QLabel(self)
        self.name_label.setText('Name:')
        self.line_input = QLineEdit(self)
        self.okButton = QPushButton("OK")

        hbox = QHBoxLayout()
        hbox.addWidget(self.name_label)
        hbox.addWidget(self.line_input)
#        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.okButton)
        vbox.addStretch(1)
        
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