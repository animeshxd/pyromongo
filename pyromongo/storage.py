import asyncio
import inspect
import time
from typing import List, Tuple, Any

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne
from pyrogram.storage.storage import Storage
from pyrogram.storage.sqlite_storage import get_input_peer


class MongoStorage(Storage):

    lock: asyncio.Lock
    USERNAME_TTL = 8 * 60 * 60

    def __init__(self, database: AsyncIOMotorDatabase, remove_peers: bool = False, peers_collection_name: str = "peers", session_collection_name: str = "session"):
        """
        Initialize a MongoStorage instance.

        Args:
            database (AsyncIOMotorDatabase): The database instance to use.
            remove_peers (bool, optional): Whether to remove peers on logout. Defaults to False.
            peers_collection_name (str, optional): Name of the peers collection. Defaults to "peers".
            session_collection_name (str, optional): Name of the session collection. Defaults to "session".
        """
        super().__init__('')
        self.lock = asyncio.Lock()
        self.database = database
        self._peer = database[peers_collection_name]
        self._session = database[session_collection_name]
        self._remove_peers = remove_peers

    async def open(self):
        """

        dc_id     INTEGER PRIMARY KEY,
        api_id    INTEGER,
        test_mode INTEGER,
        auth_key  BLOB,
        date      INTEGER NOT NULL,
        user_id   INTEGER,
        is_bot    INTEGER
        """
        await self._session.update_one(
            {'_id': 0},
            {
                '$setOnInsert': {
                    'dc_id': 2,
                    'api_id': None,
                    'test_mode': None,
                    'auth_key': b'',
                    'date': 0,
                    'user_id': 0,
                    'is_bot': 0,
                }
            },
            upsert=True,
        )
        await self._peer.create_index('id', unique=True)
        await self._peer.create_index('username', unique=True)
        await self._peer.create_index('phone_number', unique=True)

    async def save(self):
        pass

    async def close(self):
        pass

    async def delete(self):
        try:
            await self._session.delete_one({'_id': 0})
            if self._remove_peers:
                await self._peer.delete_many({})
                await self._peer.drop_indexes()
        except Exception as _:
            return

    async def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        """(id, access_hash, type, username, phone_number)"""
        s = int(time.time())
        bulk = [
            UpdateOne(
                {'_id': i[0]},
                {'$set': {
                    'access_hash': i[1],
                    'type': i[2],
                    'username': i[3],
                    'phone_number': i[4],
                    'last_update_on': s
                }},
                upsert=True
            ) for i in peers
        ]
        if not bulk:
            return
        await self._peer.bulk_write(
            bulk
        )

    async def get_peer_by_id(self, peer_id: int):
        # id, access_hash, type
        r = await self._peer.find_one({'_id': peer_id}, {'_id': 1, 'access_hash': 1, 'type': 1})
        if not r:
            raise KeyError(f"ID not found: {peer_id}")
        return get_input_peer(r['_id'], r['access_hash'], r['type'])

    async def get_peer_by_username(self, username: str):
        # id, access_hash, type, last_update_on,
        r = await self._peer.find_one({'username': username},
                                      {'_id': 1, 'access_hash': 1, 'type': 1, 'last_update_on': 1})

        if r is None:
            raise KeyError(f"Username not found: {username}")

        if abs(time.time() - r['last_update_on']) > self.USERNAME_TTL:
            raise KeyError(f"Username expired: {username}")

        return get_input_peer(r['_id'], r['access_hash'], r['type'])

    async def get_peer_by_phone_number(self, phone_number: str):

        #  _id, access_hash, type,
        r = await self._peer.find_one({'phone_number': phone_number},
                                      {'_id': 1, 'access_hash': 1, 'type': 1})

        if r is None:
            raise KeyError(f"Phone number not found: {phone_number}")

        return get_input_peer(r['_id'], r['access_hash'], r['type'])

    async def _get(self):
        attr = inspect.stack()[2].function
        d = await self._session.find_one({'_id': 0}, {attr: 1})
        if not d:
            return
        return d[attr]

    async def _set(self, value: Any):
        attr = inspect.stack()[2].function
        await self._session.update_one({'_id': 0}, {'$set': {attr: value}}, upsert=True)

    async def _accessor(self, value: Any = object):
        return await self._get() if value == object else await self._set(value)

    async def dc_id(self, value: int = object):
        return await self._accessor(value)

    async def api_id(self, value: int = object):
        return await self._accessor(value)

    async def test_mode(self, value: bool = object):
        return await self._accessor(value)

    async def auth_key(self, value: bytes = object):
        return await self._accessor(value)

    async def date(self, value: int = object):
        return await self._accessor(value)

    async def user_id(self, value: int = object):
        return await self._accessor(value)

    async def is_bot(self, value: bool = object):
        return await self._accessor(value)
