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

from moviepy.editor import (
    VideoFileClip,
    concatenate_videoclips
)
clip1 = VideoFileClip('Woman Walks Ahead.Trailer.720p.mov')
clip2 = VideoFileClip('Incredibles 2.Trailer.720p.mov')
clip3 = VideoFileClip('turn-off.mkv')
clip4 = VideoFileClip('countdown.mp4')
final_clip = concatenate_videoclips([clip1, clip2, clip3, clip4])
final_clip.write_videofile("combined trailers.mp4")
