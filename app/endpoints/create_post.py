from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.models.models import *
import app.models.pyrodb as pyrodb
from app.validation.auth import *
from app.validation.validator import Validate


router = APIRouter()
validate = Validate()


# --> Post Creation <--
@router.post("/create_post")
async def create_post(post_info: Post, user: User = Depends(get_current_active_user)) -> dict:

    user_email = user.model_dump()['email']

    if v := validate.post(post_info):
        raise HTTPException(400, detail=v)

    post_id = pyrodb.create_post(post_info, user_email)
    return {"status": 200, "detail": "Post created succesfully", "post_id": post_id}


@router.post("/create_post/pokemon")
async def add_pokemon(pokemon: Pokemon, user: User = Depends(get_current_active_user)) -> dict:
    
    user = user.model_dump()
    user_email = user['email']
    anuncio_id = pokemon.model_dump()['identifier']

    if v := validate.validate_post(anuncio_id, user):
        raise HTTPException(400, detail=v)
    
    if v := validate.validate_pokemon(pokemon):
        raise HTTPException(400, detail=v)
    
    pyrodb.insert_pokemon_to_post(user_email, pokemon)
    return {"status": 200, "detail": "Pokemon added to the post succesfully", 'user_data': user}


@router.post("/create_post/item")
async def add_item(item: Items, user: User = Depends(get_current_active_user)) -> dict:

    user_email = user.model_dump()['email']

    if v := validate.validate_items(item):
        raise HTTPException(400, detail=v)
    
    pyrodb.insert_item_to_post(user_email, item)
    return {"status": 200, "detail": "Item added to the post succesfully"}