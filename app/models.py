from .import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


#role
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'
#user
class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    quotes = db.relationship('Quote',backref='author', lazy='dynamic')
    upvote = db.relationship('Upvote',backref='user',lazy='dynamic')





    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)     


    def __repr__(self):
        return f'User {self.username}'


#quotes
class Quote(db.Model):
    __tablename__='quotes'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    upvote = db.relationship('Upvote',backref='usr',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='usr',lazy='dynamic')
    


    def save_quote(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_quotes(cls,id):
        quotes = Quote.query.filter_by(user_id=id).all()
        return quotes



#comments
class Comment(db.Model):
    __tablename__ = 'comments' 
    id = db.Column(db.Integer, primary_key = True)
    comments = db.Column(db.Text())
    quote_id = db.Column(db.Integer,db.ForeignKey('quotes.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def get_comments(cls,quote_id):
        comments = Comment.query.filter_by(quote_id=quote_id).all()

        return comments


    def __repr__(self):
        return f'Comment{self.comments}'

#upvote
class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    quote_id = db.Column(db.Integer,db.ForeignKey('quotes.id'))
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls,id):
        upvote = Upvote.query.filter_by(quote_id=id).all()
        return upvote


    def __repr__(self):
        return f'{self.user_id}:{self.quote_id}'

#downvote
class Downvote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    quote_id = db.Column(db.Integer,db.ForeignKey('quotes.id'))
    

    def save(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_downvotes(cls,id):
        downvote = Downvote.query.filter_by(quote_id=id).all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.quote_id}'
    




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

