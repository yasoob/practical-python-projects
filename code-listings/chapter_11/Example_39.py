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

class emailList(npyscreen.MultiLine):
    # ...
    def handle_selection(self, k):
        data = self.parent.parentApp.login_form.emails[self.cursor_line]
        self.parent.parentApp.email_detail_form.from_addr.value = data['from']
        self.parent.parentApp.email_detail_form.subject.value = data['subject']
        self.parent.parentApp.email_detail_form.date.value = parsedate_to_datetime(data['date']).strftime("%a, %d %b")
        self.parent.parentApp.email_detail_form.content.value = "\n\n"+data['body']
        self.parent.parentApp.switchForm('EMAIL_DETAIL')
rsor_line`` instance variable gives us the line no of the line under selection when the user pressed enter. We use that to index into the ``emails`` instance variable of the ``login_form``. This gives us all of the email data associated with the email under selection. We use this data to set the values of the different widgets in the ``email_detail_form``. We use the ``parsedate_to_datetime`` method of the ``email.utils`` package to format the date/time into the desired format. You can explore some other directives on `this page <https://strftime.org/>`__ to customize the time further. Lastly, we switch the form on display by calling the ``switchForm`` method.
