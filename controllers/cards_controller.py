from flask import Blueprint, request
from init import db
from datetime import date
from models.card import Card, CardSchema
from models.comment import Comment, CommentSchema
from controllers.auth_controller import authorize
from flask_jwt_extended import jwt_required, get_jwt_identity


# it's a container, inside, which modules - __name__ , all the path below will attach as /cards 
cards_bp = Blueprint('cards', __name__, url_prefix='/cards')
# url_prefix=/cards   =  you dont need to type cards in route below,  /  =  /cards 



# already showed as /cards, so only need to put '/'
@cards_bp.route('/')
@jwt_required()  #it means we can get the token to know which user is login
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
    if card:
        return CardSchema().dump(card)  # single card, not card's'  , delete many = true
    else:
        return {'error': f"card not found with id {id}."}, 404


@cards_bp.route('/<int:id>/', methods=['DELETE'])   #delete card
@jwt_required()
def delete_one_card(id):
    authorize()

    stmt = db.select(Card).filter_by(id=id)  #specify id = id
    card = db.session.scalar(stmt)  # single card, single scalar
    if card:
        db.session.delete(card)  #delete
        db.session.commit()  #commit = update the data
        return {'message': f"Card '{card.title}' deleted successfully."}, 200
    else:
        return {'error': f"card not found with id {id}."}, 404


@cards_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])   #update card
@jwt_required()
def update_one_card(id):
    stmt = db.select(Card).filter_by(id=id)  #specify id = id
    card = db.session.scalar(stmt)  # single card, single scalar
    if card:
        # json.get = get = return none if it's not excits, means no error
        # but make sure change [ ]  to ( ) instead
        card.title = request.json.get('title') or card.title   #means, if the new update not success, will put the previous one
        card.description = request.json.get('description') or card.description
        card.status = request.json.get('status') or card.status
        card.priority = request.json.get('priority') or card.priority
        db.session.commit()  #commit = update the data
        return CardSchema().dump(card)  # single card, not card's'  , delete many = true
    else:
        return {'error': f"card not found with id {id}."}, 404


@cards_bp.route('/', methods=['POST'])   
@jwt_required()
def create_card():
    # Create a new card model instance
    data = CardSchema().load(request.json)   #load from the schema is apply the validation from the Schema
    card = Card(
        title = data['title'],
        description = data['description'],
        date = date.today(),
        status = data['status'],
        priority = data['priority'],
        user_id = get_jwt_identity()   #how to know who's from? from token..
    )
    #  Add and commit card to db
    db.session.add(card)
    db.session.commit()
    return CardSchema().dump(card), 201   #dump = out

@cards_bp.route('/<int:card_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(card_id):
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    if card:
        comment = Comment(
            message = request.json['message'],
            user_id = get_jwt_identity(),
            card = card,
            date = date.today()
        )
        db.session.add(comment)
        db.session.commit()
        return CommentSchema().dump(comment), 201
    else:
        return {'error': f'Card not found with id {id}'}, 404

    