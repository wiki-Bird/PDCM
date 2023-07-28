from werkzeug.security import generate_password_hash, check_password_hash
from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User

from time import time

class NameNotUniqueException(Exception):
    pass

class UnknownUserException(Exception):
    pass

class AuthenticationException(Exception):
    pass

def add_user(user_name: str, password: str, repo: AbstractRepository):
    print(password)
    user = repo.get_user(user_name)
    if user:
        raise NameNotUniqueException

    password_hash = generate_password_hash(password)

    user = User(round(time() * 1000), user_name, password_hash)

    repo.add_user(user)

def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if not user:
        raise UnknownUserException
    
    return user_to_dict(user)

def authenticate_user(user_name: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(user_name)
    if user:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException

# ===================================================
# Functions to convert model entities to dictionaries
# ===================================================

def user_to_dict(user: User):
    user_dict = {
        'user_name': user.user_name,
        'password': user.password
    }
    return user_dict