from decouple import config
from fastapi import HTTPException, UploadFile
from pymongo.mongo_client import MongoClient
from passlib.context import CryptContext
from app.models.models import *
from uuid import uuid4
from jose import jwt

# --> MongoDB Stuff <--
uri = config("URI_LINK")
db_con = MongoClient(uri)
db = db_con["PyroDB"]
users = db["Users"]
items = db["Items"]
pokemons = db["Pokemons"]
files = db["Files.files"]
posts = db["Posts"]


# --> Cache <--
cache_duration = float(config("CACHE_EXPIRE_MINUTES"))
cache = []


# --> Encryption <--
SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


# --> User Handling <--
def get_user(email: str):
    user = users.find_one({'email': email})
    if user:
        return UserInDB(**user)
    
def get_user_by_post(identifier: str) -> UserInDB:
    user: dict = users.find_one({'posts': [identifier]})
    if user:
        return UserProfile(username=user["username"], posts=user["posts"])
    return user

def add_user(username: str, email: str, password: str):
    hashed_password = get_password_hash(password)
    key = str(uuid4())
    user = UserInDB(username=username, email=email, key=key, hashed_password=hashed_password).model_dump()
    to_encode = {"email": email, "key": key}
    verification_code = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    if users.find_one({"email": user['email']}):
        return False
    users.insert_one(user)
    return verification_code

def append_post_to_owner(user_email: str, post_identifier: str):
    user = users.find_one({'email': user_email})
    if user:
        user_posts: list = user['posts']
        user_posts.append(post_identifier)
        users.update_one({'email': user_email}, {'$set': {'posts': user_posts}})
    else:
        raise HTTPException(400, "Couldn't append post to the user")
    
def verify_user(key) -> None:
    users.update_one({"key": key}, {"$set": {'isVerified': True}})


# --> Post Handling <--
def create_post(post: Post, user_email: str) -> str:
    identifier = str(uuid4())
    post_to_create = PostInDB(identifier=identifier, owner=user_email, **post.model_dump()).model_dump()
    
    posts.insert_one(post_to_create)
    append_post_to_owner(user_email, identifier)

    return identifier

def insert_pokemon_to_post(user_email: str, pokemon: Pokemon):
    insert_pokemon = PokemonInDB(owner=user_email, **pokemon.model_dump()).model_dump()
    
    pokemons.insert_one(insert_pokemon)
    # append_post_to_owner(user_email)

def insert_item_to_post(user_email: str, item: Items):
    insert_item = ItemInDB(owner=user_email, **item.model_dump()).model_dump()
    
    items.insert_one(insert_item)
    # append_post_to_owner(user_email)

def get_post_by_identifier(identifier: str):
    post_data = posts.find_one({'identifier': identifier})
    if post_data:
        return PostInDB(**post_data)

def get_post_by_owner(user_email: str):
    posts_data = posts.find({'owner': user_email})

    if posts_data:
        return [PostInDB(**post_data) for post_data in posts_data]
    else:
        return []

def increase_qnt(post_identifier: str, qnt: int):
    posts.update_one({
    'identifier': post_identifier,   
    },
    { "$set": { "elements": qnt + 1 } }
    )