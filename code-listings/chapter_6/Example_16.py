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

import praw
# ...
def send_message(token, recipient, text):
    """Send the message text to recipient with id recipient.
    """
    if b"meme" in text.lower():
        subreddit_name = "memes"
    elif b"shower" in text.lower():
        subreddit_name = "Showerthoughts"
    elif b"joke" in text.lower():
        subreddit_name = "Jokes"
    else:
        subreddit_name = "GetMotivated"
    # ....
    if subreddit_name == "Showerthoughts":
        for submission in reddit.subreddit(subreddit_name).hot(limit=None):
            payload = submission.url
            break
    # ...
    r = requests.post("https://graph.facebook.com/v3.3/me/messages",
            params={"access_token": token},
            data=json.dumps({
                "recipient": {"id": recipient},
                "message": {"attachment": {
                              "type": "image",
                              "payload": {
                                "url": payload
                              }}
            }),
            headers={'Content-type': 'application/json'})
    # ...
