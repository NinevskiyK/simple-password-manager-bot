import os
import motor.motor_asyncio

def get_client():
    return motor.motor_asyncio.AsyncIOMotorClient('mongodb://mongodb:27017',
                     username=os.environ.get('MONGO_USER'),
                     password=os.environ.get('MONGO_PASSWORD'),
                     authSource='admin',
                     authMechanism='SCRAM-SHA-256')

def get_user_collection():
    return get_client()['main']['info']

async def post_new_user(collection, id):
    await collection.insert_one({'id': id, 'info': {}})

async def get_all_document(collection, id):
    c = await collection.find_one({'id': id})
    if c is None:
        await post_new_user(collection, id)
        c = await collection.find_one({'id': id})
    return c

async def get_info(collection, id, name):
    c = await get_all_document(collection, id)
    if name not in c['info']:
        return None
    return c['info'][name]

async def post_password(collection, id, name, info):
    doc = await get_all_document(collection, id)
    if name in doc['info']:
        return False
    doc['info'][name] = info
    await collection.replace_one({'id': id}, doc)
    return True

async def delete_password(collection, id, name):
    doc = await get_all_document(collection, id)
    if name not in doc['info']:
        return False
    del doc['info'][name]
    await collection.replace_one({'id': id}, doc)
    return True


