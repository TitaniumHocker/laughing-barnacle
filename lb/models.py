# -*- coding: utf-8 -*-
from datetime import date, datetime
from flask_security import RoleMixin, UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


chats_members = db.Table(
    'chats_members',
    db.Column('chat_id', db.Integer, db.ForeignKey('chats.id')),
    db.Column('member_id', db.Integer, db.ForeignKey('users.id'))
)


friends = db.Table(
    'friends',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('friend_id', db.Integer, db.ForeignKey('users.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False, index=True)
    description = db.Column(db.String(256), nullable=True)


    def __repr__(self):
        return f'<Role {self.name}>'


    def __str__(self):
        return f'{self.name}'


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password = db.Column(db.String(256), nullable=False)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship(
        'Role', secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )
    messages = db.relationship('Message', backref='owner', lazy='dynamic')
    chats = db.relationship(
        'Chat', secondary=chats_members,
        backref=db.backref('members', lazy='dynamic')
    )
    friends = db.relationship(
        'User', secondary=friends,
        primaryjoin=(friends.c.user_id == id),
        secondaryjoin=(friends.c.friend_id == id),
        lazy='dynamic'
    )
    profile = db.relationship('Profile', uselist=False, backref='owner')


    def __repr__(self):
        return f'<User email:{self.email}>'


    def __str__(self):
        return f'{self.email}'


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True)
    birthdate = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(256), nullable=True, index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


    def __repr__(self):
        return f'<Profile id:{self.id} name:{self.name}>'


    def __str__(self):
        return f'{self.name}'


    @property
    def age(self):
        return date.today() - self.birthdate


class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True, index=True)
    messages = db.relationship('Message', backref='chat', lazy='dynamic')


    def __repr__(self):
        return f'<Chat id:{self.id}>'


    def __str__(self):
        return f'Chat {self.id}'


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)
    text = db.Column(db.Text(), nullable=False, index=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)


    def __repr__(self):
        return f'<Message id:{self.id} owner:{self.owner} created:{self.created}>'


    def __str__(self):
        return f'Message from {self.owner}'
