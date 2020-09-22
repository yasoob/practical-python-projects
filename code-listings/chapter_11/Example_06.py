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
import imghdr
from email.message import EmailMessage
from email.headerregistry import Address
MY_ADDRESS = ''
PASSWORD = ''
to_address = (
    Address(
        display_name='Yasoob Khalid',
        username='yasoobkhld',
        domain='gmail.com'
    ), 
)
msg = EmailMessage()
msg['Subject'] = 'Testing Testing 1.2.3'
msg['From'] = 'Yasoob <3'
msg['To'] = to_addr
msg.set_content("""Hi Yasoob!! 
I am just trying to send some emails using SMTP.
Regards
Yasoob""")
with open('some_image_file', 'rb') as fp:
    img_data = fp.read()
msg.add_attachment(img_data,
                        maintype='image',
                        subtype=imghdr.what(None, img_data), 
                        filename="some_image_file")
with smtplib.SMTP('smtp.gmail.com', port=587) as s:
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    s.send_message(msg)
print("Message Sent Successfully!")
