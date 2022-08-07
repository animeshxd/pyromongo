# pyromongo
Persistent Session Storage for Pyrogram with MongoDB

```python
from pyrogram.client import Client
from pyromongo import MongoStorage
from motor.motor_asyncio import AsyncIOMotorClient

client = Client(..)
mongo = AsyncIOMotorClient("mongodb+srv://..")
client.storage = MongoStorage(mongo["pyrogram"])


client.run()
```

## Note:
  ❌ It will not work with pyrogram context manager  
   ```python
   async def main():
       async with Client(..) as client:
           client.storage = MongoStorage(..)
   
   # It will only store peers
   ```
