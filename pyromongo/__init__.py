import asyncio
import inspect
import time
from typing import List, Tuple, Any

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import UpdateOne
from pyrogram.storage import Storage
from pyrogram.storage.sqlite_storage import get_input_peer


class MongoStorage(Storage):
    lock: asyncio.Lock
    USERNAME_TTL = 8 * 60 * 60

    def __init__(self, database: AsyncIOMotorDatabase):
        super().__init__('')
        self.lock = asyncio.Lock()
        self.database = database
        self._peer = database['peers']
        self._session = database['session']
        # self._dc_id = 2
        # self._api_id = None
        # self._test_mode = None
        # self._auth_key = b''
        # self._date = None
        # self._user_id = None
        # self._is_bot = False

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
        if await self._session.find_one({'_id': 0}, {}):
            return
        await self._session.upate_one(
            {'_id': 0},
            {
                'dc_id': 2,
                'api_id': 0,
                'test_mode': 0,
                'auth_key': b'',
                'date': 0,
                'user_id': 0,
                'is_bot': 0,

            }
        )

    async def save(self):
        pass

    async def close(self):
        pass

    async def delete(self):
        try:
            await self._session.delete_one({'_id': 0})
        except Exception as _:
            return

    async def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        """(id, access_hash, type, username, phone_number)"""
        s = int(time.time())
        bulk = [
                UpdateOne(
                    {'_id': i[0]},
                    {'$set': {'access_hash': i[1], 'type': i[2], 'username': i[3], 'phone_number': i[4],
                              'last_update_on': s}},
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
        return get_input_peer(*r.values())

    async def get_peer_by_username(self, username: str):
        # id, access_hash, type, last_update_on,
        r = await self._peer.find_one({'username': username},
                                      {'_id': 1, 'access_hash': 1, 'type': 1, 'last_update_on': 1})

        if r is None:
            raise KeyError(f"Username not found: {username}")

        if abs(time.time() - r['last']) > self.USERNAME_TTL:
            raise KeyError(f"Username expired: {username}")

        return get_input_peer(*r.values()[:3])

    async def get_peer_by_phone_number(self, phone_number: str):

        #  _id, access_hash, type,
        r = await self._peer.find_one({'phone_number': phone_number},
                                      {'_id': 1, 'access_hash': 1, 'type': 1})

        if r is None:
            raise KeyError(f"Phone number not found: {phone_number}")

        return get_input_peer(*r)

    async def _get(self):
        attr = inspect.stack()[2].function
        return await self._session.find_one({'_id': 0}, {attr: 1})[attr]

    async def _set(self, value: Any):
        attr = inspect.stack()[2].function
        await self._session.update({'_id': 0}, {'$set': {attr: value}})

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