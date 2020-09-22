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

from flask_sqlalchemy import SQLAlchemy
# ...
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
# ...
relationship_table=db.Table('relationship_table',                            
    db.Column('user_id', db.Integer,db.ForeignKey('users.id'), nullable=False),
    db.Column('post_id',db.Integer,db.ForeignKey('posts.id'),nullable=False),
    db.PrimaryKeyConstraint('user_id', 'post_id') )
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),nullable=False)
    posts=db.relationship('Posts', secondary=relationship_table, backref='users' )  
    def __init__(self, name):
        self.name = name
class Posts(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, unique=True, nullable=False)
    url=db.Column(db.String, nullable=False)
    def __init__(self, name, URL):
        self.name = name
        self.url = url
