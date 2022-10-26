from init import db, ma    #< cannot do, because db is in the def
from marshmallow import fields


class Card(db.Model):   #Flask Alchemy data type , defining model
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))  #can put max length inside the string, dont need to put () if no length required
    description = db.Column(db.Text)  #because text is better than string here, can put more words.
    date = db.Column(db.Date)  #be careful the date function. need to use the package from python, so import
    status = db.Column(db.String)
    priority = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('User', back_populates='cards') #one user can have many card'S'
    comments = db.relationship('Comment', back_populates='card', cascade='all, delete') #because comment only can be one single card
    # cascade delete, because no card, no comment.



# put the schema for easy to import together (for small project, otherwise, seperate different file)
class CardSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    comments = fields.List(fields.Nested('CommentSchema', exclude=['card']))


    class Meta:
        fields = ('id', 'title', 'description', 'status', 'priority', 'date', 'user', 'comments')
        ordered = True

        # normally put in another new file, but schema is small so can put in here as well.