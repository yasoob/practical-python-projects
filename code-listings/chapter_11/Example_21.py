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

import email
from imaplib import IMAP4_SSL
from pprint import pprint
USER = ""
PASSWORD = ""
server = IMAP4_SSL('imap.gmail.com')
server.login(USER, PASSWORD)
rv, output = server.select('INBOX')
rv, output = server.search(None, 'UNSEEN')
id_list = output[0].split()
email_data = []
for e_id in id_list[::-1][:10]:
    rv, output = server.fetch(e_id, '(BODY.PEEK[HEADER])')
    msg = email.message_from_bytes(output[0][1])
    hdr = {}
    hdr['to'] = email.header.decode_header(msg['to'])[0][0]
    hdr['from'] = email.header.decode_header(msg['from'])[0][0]
    hdr['date'] = email.header.decode_header(msg['date'])[0][0]
    hdr['subject'] = email.header.decode_header(msg['subject'])[0][0]
    email_data.append(hdr)
    pprint(hdr)
server.close()
server.logout()
