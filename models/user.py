from init import db, ma    #< cannot do, because db is in the def
from marshmallow import fields




class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)  #false mean cannot null, must write the email.   unique = only can register one
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)   #admin had authorization, so no default.

    cards = db.relationship('Card',back_populates='user', cascade='all, delete')
    # Class Name 'Card', not tablename 'cards' ***
    #it's 'user' not 'users' because we need to know each one, not all
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete')


class UserSchema(ma.Schema):
    cards = fields.List(fields.Nested('CardSchema', exclude=['user']))
    comments = fields.List(fields.Nested('CommentSchema', exclude=['user']))

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin', 'cards')   # know we need password but not it json.
    