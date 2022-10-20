from db import db, ma    #< cannot do, because db is in the def


class Card(db.Model):   #Flask Alchemy data type , defining model
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))  #can put max length inside the string, dont need to put () if no length required
    description = db.Column(db.Text)  #because text is better than string here, can put more words.
    date = db.Column(db.Date)  #be careful the date function. need to use the package from python, so import
    status = db.Column(db.String)
    priority = db.Column(db.String)


# put the schema for easy to import together (for small project, otherwise, seperate different file)
class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'status', 'priority', 'date')
        ordered = True