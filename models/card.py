from wsgiref import validate
from init import db, ma    #< cannot do, because db is in the def
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

VALID_PRIORITIES = ('Urgent' , 'High', 'Low', 'Medium')
VALID_STATUSES = ('To Do', 'Done', 'Ongoing', 'Testing', 'Deployed')

class Card(db.Model):   #Flask Alchemy data type , defining model
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))  #can put max length inside the string, dont need to put () if no length required
    description = db.Column(db.Text)  #because text is better than string here, can put more words.
    date = db.Column(db.Date)  #be careful the date function. need to use the package from python, so import
    status = db.Column(db.String, default=VALID_STATUSES[0])
    priority = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship('User', back_populates='cards') #one user can have many card'S'
    comments = db.relationship('Comment', back_populates='card', cascade='all, delete') #because comment only can be one single card
    # cascade delete, because no card, no comment.



# put the schema for easy to import together (for small project, otherwise, seperate different file)
class CardSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    comments = fields.List(fields.Nested('CommentSchema', exclude=['card']))
    title = fields.String(required=True, validate=And(
        Length(min=2, error= 'Title must be at least 2 characters long.'),
        #means the title is a string field and it must have a value, can't empty, but funnest thing is empty string, "" count have value.
        #so vaildate means the length minimum is 2 now.
        Regexp('^[a-zA-Z0-9 ]+$', error= 'Only letters, numbers and spaces are allowed.')
    )) 
    #And= , means can do more than one validation at the same time.
    #Regexp, regular expecation  ^= a-z, A-Z, 0-9     $ = apply up to
    #error= '', mean showing what error msg is.
    status = fields.String(load_default='To Do', validate=OneOf(VALID_STATUSES))
    # load_default > To Do   , it means if no status input, it will auto fill 'To Do'
    # can write load_default='To Do'  or  load_default=VAILD_STATUSES[0]

    priority = fields.String(required=True, validate=OneOf(VALID_PRIORITIES))

    @validates('status')
    def validate_status(self, value):
        if value == VALID_STATUSES[2]:
            stmt = db.select(db.func.count()).select_from(Card).filter_by(status=VALID_STATUSES[2])
            # ... and there's already an ongoing card in the db
            count = db.session.scalar(stmt)
            if count > 0:
                raise ValidationError('You already have an ongoing card.')


    class Meta:
        #this field only can show without the json one, so may create 2 field
        fields = ('id', 'title', 'description', 'status', 'priority', 'date', 'user', 'comments') 

        ordered = True

        # normally put in another new file, but schema is small so can put in here as well.