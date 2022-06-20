from functools import wraps
from flask import request
import bcrypt
import jwt
from dotenv import load_dotenv
# os module reads APP_SECRET from env
import os

load_dotenv()

SECRET_KEY = os.getenv('APP_SECRET')

# decorator extracts token from request header, prevents user from accessing the selected funtionality if a token is not present
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers['Authorization'].split(' ')[1]
        if token is None:
          return 'Access Denied'
        return f(*args, **kwargs)
    return decorated_function

def create_token(payload):
  # return new token
  return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
  # payload - contains user information to be stored
  # secret key (from env) is used with signing algorith to generate a unique signature for our tokens. Secret Key makes it unique to our app.
  
# grabs user data from a request header 
def read_token(req):
  try:
    token = req.headers['Authorization'].split(' ')[1]
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload
  except jwt.InvalidSignatureError:
    return 'Signature Invalid'
  except jwt.InvalidTokenError:
    return 'Token Invalid'

# hashing passwords
def gen_password(password):
  # encode ensures bcrypt format; decode decodes the characters attached by bcrypt when it restures
  # gensalt generates a random salt for each pw
  return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def compare_password(password, hashed_password):
  return bcrypt.checkpw(password.encode(), hashed_password.encode())