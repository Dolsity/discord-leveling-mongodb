from dotenv import load_dotenv
from pymongo import MongoClient
import os

from .config import message_rate

load_dotenv()
mongo_uri = os.getenv('MONGO_URI')
cluster = MongoClient(mongo_uri)
db = cluster["leveling"]

async def create_collection(guild_id):

    find_collection = db.list_collection_names()
    if f'{guild_id}' in find_collection:
        return

    db.create_collection(f'{guild_id}')

async def create_user_guild(user_id, guild_id):
    await create_collection(guild_id)

    fetch_data = db[f'{guild_id}'].find_one({'_id': user_id})
    if fetch_data:
        return
    
    db[f'{guild_id}'].insert_one({
        "_id": user_id,
        "level": 0,
        "xp": 0
    })

async def increase_xp_guild(guild_id, user_id, rate=message_rate):
    await create_user_guild(user_id, guild_id)

    fetch_data = db[f'{guild_id}'].find_one({'_id': user_id})

    xp = fetch_data["xp"]
    level = fetch_data["level"]
    new_level = int((xp + rate) / 100)

    if new_level > level:
        new_level = new_level
    else:
        new_level = level

    db[f'{guild_id}'].update_one(
        {"_id": user_id}, {"$set": {"level": new_level, "xp": xp + rate}}
    )

async def get_user_data_guild(user_id, guild_id):
    await create_user_guild(user_id, guild_id)
    fetch_data = db[f'{guild_id}'].find_one({"_id": user_id})

    return dict(fetch_data)

async def get_rank_guild(user_id, guild_id):
    await create_user_guild(user_id, guild_id)

    fetch_data = db[f'{guild_id}'].find_one({"_id": user_id})
    
    rank = 0
    for x in fetch_data:
        rank += 1
        if x["user_id"] == user_id:
            break

    return rank