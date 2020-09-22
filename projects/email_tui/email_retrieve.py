import email
from imaplib import IMAP4_SSL
from pprint import pprint

class EmailReader():
	USER = "yasoob.khld@gmail.com"
	PASSWORD = "sumoepsahudhvvdc"
	HOST = "imap.gmail.com"
	PORT = 993

	def __init__(self,USER=None, PASSWORD=None, HOST=None, PORT=None):
		self.USER = USER or self.USER
		self.PASSWORD = PASSWORD or self.PASSWORD
		self.HOST = HOST or self.HOST
		self.PORT = PORT or self.PORT
		self.setup_connection()

	def setup_connection(self):
		self.server = IMAP4_SSL(self.HOST, port=self.PORT)
		self.server.login(self.USER, self.PASSWORD)

	def folder_list(self):
		rv, output = self.server.list()
		return output

	def open_inbox(self):
		rv, output = self.server.select('INBOX')

	def get_unread_emails(self):
		rv, output = self.server.search(None, 'UNSEEN')
		id_list = output[0].split()
		return id_list[::-1]

	def fetch_emails(self, id_list):
		email_data = []
		for e_id in id_list:
			rv, output = self.server.fetch(e_id, '(BODY.PEEK[])')
			msg = email.message_from_bytes(output[0][1])
			hdr = {}
			hdr['to'] = email.header.decode_header(msg['to'])[0][0]
			hdr['from'] = email.header.decode_header(msg['from'])[0][0]
			hdr['date'] = email.header.decode_header(msg['date'])[0][0]
			hdr['subject'] = email.header.decode_header(msg['subject'])[0][0]
			hdr['body'] = "No textual content found :("
			maintype = msg.get_content_maintype()
			if maintype == 'multipart':
				for part in msg.get_payload():
					if part.get_content_maintype() == 'text':
						hdr['body'] = part.get_payload()
						break
			elif maintype == 'text':
				hdr['body'] = msg.get_payload()
			if type(hdr['subject']) == bytes:
				hdr['subject'] = hdr['subject'].decode('utf-8')
			if type(hdr['from']) == bytes:
				hdr['from'] = hdr['from'].decode('utf-8')
			email_data.append(hdr)
		
		return email_data

