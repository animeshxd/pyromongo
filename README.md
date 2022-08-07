# pyromongo
## INTRODUCTION 
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
  ❌ It doesn't delete peers from the database on logout ( on purpose ).

  ❌ It will not work with the pyrogram context manager.
   ```python
   async def main():
       async with Client(..) as client:
           client.storage = MongoStorage(..)
   
   # It will only store peers
   ```
 ### INSTALLATION:
  ```bash
  pip install git+https://github.com/animeshxd/pyromongo
  ```
  Install dnspython for `mongo+srv://..` URIs
   ```bash
   pip install dnspython
    
   # for Termux use dnspython fork
   apt install resolv-conf
   pip install git+https://github.com/animeshxd/dnspython
   ```
  Check other required dependencies for motor
  https://motor.readthedocs.io/en/stable/installation.html#dependencies
  
