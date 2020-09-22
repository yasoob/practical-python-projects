import npyscreen
from email_retrieve import EmailReader
import curses
from email.utils import parsedate_to_datetime


class loginForm(npyscreen.ActionPopup):

	def get_emails(self):
		self.client = EmailReader(self.username.value, 
								  self.password.value, 
								  self.imap_host.value, 
								  self.imap_port.value)
		self.client.open_inbox()
		email_ids = self.client.get_unread_emails()
		self.emails = self.client.fetch_emails(email_ids[:20])

	def on_ok(self):
		npyscreen.notify("Logging in..", title="Please Wait")
		self.get_emails()
		email_list = []
		for c, i in enumerate(self.emails):
			single_rec = "{count: <{width}}- {subject:80.74} {from_addr}".format(count=c+1, 
																			width=3, 
																			subject=i['subject'], 
																			from_addr=i['from']) 
			email_list.append(single_rec)
		
		self.parentApp.email_list_form.email_list.values = email_list
		self.parentApp.switchForm('EMAIL_LIST')
	
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
		data = self.parent.parentApp.login_form.emails[self.cursor_line]
		self.parent.parentApp.email_detail_form.from_addr.value = data['from']
		self.parent.parentApp.email_detail_form.subject.value = data['subject']
		self.parent.parentApp.email_detail_form.date.value = parsedate_to_datetime(data['date']).strftime("%a, %d %b")
		self.parent.parentApp.email_detail_form.content.value = "\n\n"+data['body']
		self.parent.parentApp.switchForm('EMAIL_DETAIL')
		

class emailListForm(npyscreen.ActionFormMinimal):

	OK_BUTTON_TEXT = 'Quit'

	def on_ok(self):
		self.parentApp.setNextForm(None)

	def create(self):
		self._header = self.add(npyscreen.FixedText, value='{:85} {:45}'.format('Subject', 'Sender'), editable=False)
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
		self.from_addr = self.add(npyscreen.TitleFixedText, name="From: ", value='', editable=False)
		self.subject = self.add(npyscreen.TitleFixedText, name="Subject: ", value='', editable=False)
		self.date = self.add(npyscreen.TitleFixedText, name="Date:  ", value='', editable=False)
		self.content = self.add(emailBody, value='')

class MyApplication(npyscreen.NPSAppManaged):
	def onStart(self):
		self.login_form = self.addForm('MAIN', loginForm, name='Email Client')
		self.email_list_form = self.addForm('EMAIL_LIST', emailListForm, name='Latest Unread Emails')
		self.email_detail_form = self.addForm('EMAIL_DETAIL', emailDetailForm, name='Email')

if __name__ == '__main__':
	TestApp = MyApplication().run()