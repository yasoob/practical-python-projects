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

import smtplib
from string import Template
from email.message import EmailMessage
from email.headerregistry import Address
MY_ADDRESS = ''
PASSWORD = ''
def recipient_list():
    email_list = []
    with open('email_recipient.txt', 'r') as f:
        to_name, to_email = f.readline().split()
        username, domain = to_email.split('@')
        addr = Address(display_name=to_name, username=username, domain=domain)
        email_list.append(addr)
    return email_list
def get_template():
    with open('email_template.txt', 'r') as f:
        email_template = f.read()
    return Template(email_template)
def setup_smtp():
    s = smtplib.SMTP('smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    return s
def main():
    s = setup_smtp()
    for email_addr in recipient_list():
        msg = EmailMessage()
        msg['Subject'] = 'Birthday invitation!!!'
        msg['From'] = 'Yasoob <3'
        msg['To'] = email_addr
        msg.set_content(get_template().substitute(name=email_addr.display_name))
        s.send_message(msg)
        print("Message Sent to {}".format(email_addr.display_name))
    s.quit()
if __name__ == '__main__':
    main()
