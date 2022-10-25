from init import db, ma    #< cannot do, because db is in the def


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)  #false mean cannot null, must write the email.   unique = only can register one
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)   #admin had authorization, so no default.

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin')   # know we need password but not it json.
    