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

class MainWidget(QWidget):
    # ...
    
    def initUI(self):
        # ...
        self.url_label = QLabel(self)
        self.url_label.setText('Url:')
        self.url_input = QLineEdit(self)
        
        self.location_label = QLabel(self)
        self.location_label.setText('Location:')
        self.location_input = QLineEdit(self)
        self.browse_btn = QPushButton("Browse")
        self.download_btn = QPushButton("Download")
        
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.url_label, 0, 0)
        grid.addWidget(self.url_input, 0, 1, 1, 2)
        
        grid.addWidget(self.location_label, 1, 0)
        grid.addWidget(self.location_input, 1, 1)
        grid.addWidget(self.browse_btn, 1, 2)        
        grid.addWidget(self.download_btn, 2, 0, 1, 3)
