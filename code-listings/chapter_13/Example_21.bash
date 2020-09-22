# Using This Code Example
# =========================
# The code examples are provided by Yasoob Khalid to help you 
# reference Practical Python Projects book. Code samples follow
# PEP-0008, with exceptions made for the purposes of improving book
# formatting. Example code is provided "as is".
# Permissions
# ============
# In general, you may use the code we've provided with this book in your
# programs . You do not need to contact us for permission unless you're
# reproducing a significant portion of the code and using it in educational
# distributions. Examples:
# * Writing an education program or book that uses several chunks of code from
#     this course requires permission. 
# * Selling or distributing a digital package from material taken from this
#     book does require permission.
# * Answering a question by citing this book and quoting example code does not
#     require permission.
# Attributions usually include the title, author, publisher and an ISBN. For
# example, "Practical Python Projects, by Yasoob Khalid. Copyright 2020 Yasoob."
# If you feel your use of code examples falls outside fair use of the permission
# given here, please contact me at hi@yasoob.me.

docker run -d --restart=always -p 80:80 -t flask_image
`-d`` tell docker to run this container in detached mode so that even when we close the terminal the container will keep on running. We can view the logs using ``docker logs`` command
`--restart=always`` tells Docker to restart the container if it shuts down/crashes or system restarts
