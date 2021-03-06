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

class DownloadThread(QThread):
    def __init__(self, directory, url, row_position):
        super(DownloadThread, self).__init__()
        self.ydl_opts = {
            'logger': MyLogger(),
            'outtmpl': os.path.join(directory,'%(title)s.%(ext)s'),
            'progress_hooks': [self.my_hook],
        }
        self.url = url
        self.row_position = row_position
        
    def my_hook(self, data):
        filename = data.get('filename').split('/')[-1].split('.')[0]
        print(filename, data.get('_percent_str', '100%'), \
        self.row_position)
    def run(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])
