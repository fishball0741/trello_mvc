from flask import Blueprint
from db import db
from models.card import Card, CardSchema

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')
# url_prefix=/cards   =  you dont need to type cards in route below,  /  =  /cards 


@cards_bp.route('/')
# @jwt_required()  #it means we can get the token to know which user is login
def all_cards():
    # return 'all_cards route'
    # if not authorize():
    #     return {'erroe': 'You must be an admin'}, 401
    # select * from cards;
    # cards = Card.query.all()
    # stmt = db.select(Card).where(Card.status == 'To Do')
    
    stmt = db.select(Card).order_by(Card.priority.desc(), Card.title)   # statement =stmt
    cards = db.session.scalars(stmt)  # same as execute , to the statement,  ( different when choose certain columns, but scalars is better)
    return CardSchema(many=True).dump(cards)  # we used scalars, we know will show a list, 

@cards_bp.route('/<int:id>/')   #do it for single card, read 1 card only
def one_card(id):
    stmt = db.select(Card).filter_by(id=id)  #specify id = id
    card = db.session.scalar(stmt)  # single card, single scalar
    return CardSchema().dump(card)  # single card, not card's'  , delete many = true
