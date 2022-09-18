from enum import unique
from time import time
from app import db
from datetime import datetime
import re
from flask_security import UserMixin,RoleMixin


def slugify(s: str) ->str:
    if "#" in s:
        s = s.replace("#","sharp")
    pattern = r'[^\w+]'
    return re.sub(pattern,'-',s)


role_users = db.Table('roles_users',
                    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                    db.Column('role_id',db.Integer,db.ForeignKey('role.id')))

post_tag = db.Table('post_tag',
                    db.Column('post_id',db.Integer,db.ForeignKey('posts.id')),
                    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id')))

class Posts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(150))
    slug = db.Column(db.String(150),unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime,default = datetime.now())
    tags = db.relationship('Tag',secondary=post_tag,backref = db.backref('posts'),lazy='dynamic')
    
    def __init__(self,title,body):
        self.title = title
        self.body = body
        self.generate_slug()
    
    def __repr__(self) ->str:
        return f'<PostID: {self.id}, title: {self.title}'
    
    def generate_slug(self) ->None:
        if self.title:
            self.slug = slugify(self.title)
        else:
            self.slug = str(int(time()))
            
    @classmethod
    def add_to_db(cls,title,body):
        post = cls(title,body)
        db.session.add(post)
        db.session.commit()

class Tag(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(250))
    slug = db.Column(db.String(250),unique=True)
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.slug = slugify(self.title)
    
    def __repr__(self):
        return f'<TagID: {self.id}, title: {self.title}'
    
    
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    role = db.relationship('Role',secondary=role_users,backref = db.backref('users'),lazy='dynamic')
    

class Role(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),unique=True)
