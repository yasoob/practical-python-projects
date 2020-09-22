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

import npyscreen
from email_retrieve import EmailReader
import curses
from email.utils import parsedate_to_datetime
class loginForm(npyscreen.ActionPopup):
    def on_ok(self):
        self.parentApp.setNextForm('EMAIL_LIST')
    
    def on_cancel(self):
        self.parentApp.setNextForm(None)
        
    def create(self):
        self.username = self.add(npyscreen.TitleText, name='Name')
        self.password = self.add(npyscreen.TitlePassword, name='Password')
        self.imap_host = self.add(npyscreen.TitleText, name='IMAP host')
        self.imap_port = self.add(npyscreen.TitleText, name='IMAP port')
class emailList(npyscreen.MultiLine):
    
    def set_up_handlers(self):
        super(emailList, self).set_up_handlers()
        self.handlers.update({
            curses.ascii.CR: self.handle_selection,
             curses.ascii.NL: self.handle_selection,
             curses.ascii.SP: self.handle_selection,
        })
    def handle_selection(self, k):
        self.parent.parentApp.switchForm('EMAIL_DETAIL')
        #npyscreen.notify_wait('Handler is working!')
        
class emailListForm(npyscreen.ActionFormMinimal):
    OK_BUTTON_TEXT = 'Quit'
    def on_ok(self):
        self.parentApp.setNextForm(None)
    def create(self):
        self._header = self.add(npyscreen.FixedText, 
            value='{:85} {:45}'.format('Subject', 'Sender'), 
            editable=False)
        self.email_list = self.add(emailList, name="Latest Unread Emails", 
            values=["Email No {}".format(i) for i in range(30)])    
class emailBody(npyscreen.MultiLineEdit):
    def h_addch(self, d):
        return
class emailDetailForm(npyscreen.ActionForm):
    CANCEL_BUTTON_TEXT = 'Back'
    OK_BUTTON_TEXT = 'Quit'
    def on_cancel(self):
        self.parentApp.switchFormPrevious()
    def on_ok(self):
        self.parentApp.switchForm(None)
    
    def create(self):
        self.from_addr = self.add(npyscreen.TitleFixedText, 
            name="From: ", value='', editable=False)
        self.subject = self.add(npyscreen.TitleFixedText, 
            name="Subject: ", value='', editable=False)
        self.date = self.add(npyscreen.TitleFixedText, name="Date:  ", 
            value='', editable=False)
        self.content = self.add(emailBody, value='')
class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.login_form = self.addForm('MAIN', loginForm, 
            name='Email Client')
        self.email_list_form = self.addForm('EMAIL_LIST', 
            emailListForm, name='Latest Unread Emails')
        self.email_detail_form = self.addForm('EMAIL_DETAIL', 
            emailDetailForm, name='Email')
if __name__ == '__main__':
    TestApp = MyApplication().run()        
