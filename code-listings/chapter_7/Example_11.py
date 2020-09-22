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

import os
from download_trailers import (get_trailer_file_urls, 
                              download_trailer_file,
                              get_trailer_filename)
page_url = "https://trailers.apple.com/trailers/disney/incredibles-2/"
destdir = os.getcwd()
trailer_url = get_trailer_file_urls(page_url, "720", "single_trailer", [])[0]
trailer_file_name = get_trailer_filename(
                        trailer_url['title'], 
                        trailer_url['type'],
                        trailer_url['res']
                    )
if not os.path.exists(trailer_file_name):
    download_trailer_file(trailer_url['url'], destdir, trailer_file_name)
