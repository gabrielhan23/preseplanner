from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from otherFiles.setup import app

db = SQLAlchemy(app)

groups = db.Table('groups',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class User(db.Model, UserMixin):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)

  fname = db.Column(db.String(20), nullable=False)
  lname = db.Column(db.String(20), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  groups = db.relationship('Group', secondary=groups, lazy='subquery', backref=db.backref('users', lazy=True))
  wish = db.relationship('Wish', backref="user", lazy=True)
  get = db.relationship('Get', backref="user", lazy=True)

  def __repr__(self):
        return "User('{self.fname}', '{self.email}')"

class Group(db.Model):
  __tablename__ = 'group'
  id = db.Column(db.Integer, primary_key=True)

  hashID = db.Column(db.String(5), unique=True, nullable=False)
  name = db.Column(db.String(50), nullable=False)

  wish = db.relationship('Wish', backref="group", lazy=True)
  get = db.relationship('Get', backref="group", lazy=True)

  def __repr__(self):
        return "Group("+self.hashID+", "+self.name+")"

class Wish(db.Model):
  __tablename__ = 'wishes'
  id = db.Column(db.Integer, primary_key=True)

  name = db.Column(db.String(1000), nullable=False)
  get_user_id = db.Column(db.Integer, nullable=True)

  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
  get_id = db.Column(db.Integer, db.ForeignKey('gets.id'), nullable=True)

  def __repr__(self):
        return "Wish("+self.name+", "+str(self.user_id)+", "+str(self.group_id)+")"
class Get(db.Model):
  __tablename__ = 'gets'
  id = db.Column(db.Integer, primary_key=True)

  name = db.Column(db.String(1000), nullable=False)
  user_getting_for_id = db.Column(db.Integer, nullable=False)

  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
  wish = db.relationship('Wish', backref="get", lazy=True)

  def __repr__(self):
        return "Wish("+self.name+", "+str(self.user_id)+", "+str(self.group_id)+")"
db.create_all()
