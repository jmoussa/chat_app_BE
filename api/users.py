import logging

from fastapi import Depends, APIRouter

from requests import FavoriteRequest

from controllers import (
    add_favlist_to_user,
    remove_favorite_from_user,
    get_current_active_user,
    get_user_favorites,
)
from models import User
from mongodb import get_nosql_db, MongoClient

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/favorites", tags=["User"])
async def alter_favorite_room(
    request: FavoriteRequest,
    current_user: User = Depends(get_current_active_user),
    client: MongoClient = Depends(get_nosql_db),
):
    """
    Add or remove a favorite room from a user
    the request.type should be either "add" or "remove"
    """
    try:
        if request.type == "add":
            new_user_obj = await add_favlist_to_user(request.username, request.favorites)
        elif request.type == "remove":
            new_user_obj = await remove_favorite_from_user(request.username, request.favorite)

        logger.info(f"Updated User Favorites\n{new_user_obj['favorites']}\n-----------------------")
        return new_user_obj
    except Exception as e:
        logger.error(f"/favorites: {e}")
        pass


@router.get("/favorites/{user_name}", tags=["User"])
async def get_favorite_rooms(
    user_name: str, current_user: User = Depends(get_current_active_user), client: MongoClient = Depends(get_nosql_db),
):
    """
    Get all favorite Room objects from a user
    """
    try:
        rooms_list = await get_user_favorites(user_name)
        return rooms_list
    except Exception as e:
        logger.error(f"/favorites: {e}")
