from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --> Token Models <--
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str or None = None #type: ignore


# --> User Models <--
class User(BaseModel):
    username: str
    email: EmailStr or None = None #type: ignore

class UserInDB(User):
    posts: Optional[list] = []
    isAdmin: Optional[bool] = False
    disabled: Optional[bool] = False
    isVerified: Optional[bool] = False
    key: str
    hashed_password: str

class UserInSignup(User):
    password: str

class UserProfile(BaseModel):
    username: str
    posts: list


# --> Plugin File Models <--
class PluginInDB(BaseModel):
    filename: str
    owner: EmailStr
    identifier: str
    total_downloads: int


class DownloadInfo(BaseModel):
    path: str
    name: str

class DownloadCache(BaseModel):
    identifier: str
    filename: str
    path: str
    expiry: datetime


# --> Post Models <--
class Post(BaseModel):
    title: str
    description: str
    datetime: int

class Pokemon(BaseModel):
    post_identifier: str
    name: str
    level: int
    nature: str
    pokeball: str
    shiny: bool
    addon: str
    boost: int

class Item(BaseModel):
    post_identifier: str
    type: str
    name: str

class PostInDB(Post):
    owner: EmailStr
    identifier: str
    elements: int = 0

class PostDetails(PostInDB):
    items: List[Item]  # Corrigido para ser uma lista de Items
    pokemons: List[Pokemon]  # Corrigido para ser uma lista de Pokemons

class ItemInDB(Item):
    identifier: str
    owner: EmailStr

class PokemonInDB(Pokemon):
    identifier: str
    owner: EmailStr