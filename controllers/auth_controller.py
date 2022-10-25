from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import timedelta
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity



auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register/', methods=['POST'])    #because we want this route should be POST request instead of route, so set the method to POST
def auth_register():  #encode and python object, can use json to convert as well
    try:
        # Load the posted user info and parse the JSON
        # user_info = UserSchema().load(request.json)   #need to request data
        # print(user_info)
        # Create a new User Model instance from the user_info
        user = User(
            email = request.json['email'],     #those using [ ] instead of  user_info.email  < can't use it
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),    #encrypt the password, hash the password
            name = request.json.get('name')
        )
        # add and commit user to DB
        db.session.add(user)
        db.session.commit()
        # respond to client
        return UserSchema(exclude=['password']).dump(user), 201   #normally use 201     , need to exculde the password here as dont want to show the password hash

        # In this case (complex multi-running flow) after client input, will check the db, and see any data already in the database, if yes, then return the error
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409



# Login route  only for POST
@auth_bp.route('/login/', methods=['POST'])   
def auth_login():   #check any account/email/user name in DB first.
    #  Find a use by email address
    stmt = db.select(User).filter_by(email=request.json['email'])   # or using  db.select(User).where(User.email == request.json['email'])  < comparison, so need  ==
    user = db.session.scalar(stmt)

    # create a statement first  ,  and search the email and password (CANNOT USE generate_password_hash) >>> the generate_salt will produce random, so can't match the original pw hash
    # check_password_hash        
    # If user exists and password is correct  
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        # return UserSchema(exclude=['password']).dump(user)   #200 = default
        #what we want to identity for the user, by email? by the ID number?
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))    #set the id will be a string from user.id, and expires in one days
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}   #using this instead of Schema because we dont want to return all the details and also want to have token.
    # If user exists and password is not correct,   security reason, dont specifically say what's wrong, pw or email.
    else:
        return {'error': 'Invalid password or email'}, 401


def authorize():
    user_id = get_jwt_identity()   #return the user id into the token
    stmt = db.select(User).filter_by(id=user_id)  #check the statement
    user = db.session.scalar(stmt)  #check the db statement
    if not user.is_admin:
        abort(401)