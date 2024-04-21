# pyromongo
## INTRODUCTION 
Persistent Session Storage for Pyrogram with MongoDB

```python
from pyrogram.client import Client
from pyromongo import MongoStorage
from motor.motor_asyncio import AsyncIOMotorClient

client = Client(..)
mongo = AsyncIOMotorClient("mongodb+srv://..")
client.storage = MongoStorage(mongo["pyrogram"], remove_peers=False) # use remove_peers=True to remove all peers on logout


client.run()
```
## Note:
  ❌ It will not work with the pyrogram context manager.
   ```python
   async def main():
       async with Client(..) as client:
           client.storage = MongoStorage(..)
   
   # It will only store peers
   ```
 ### INSTALLATION:
  ```bash
  pip install pyromongo

  # Install from git
  pip install git+https://github.com/animeshxd/pyromongo
  ```
  Install dnspython for `mongo+srv://..` URIs
   ```bash
   pip install dnspython
   # or pip install -U pyromongo[srv]
    
   # for Termux use dnspython fork
   apt install resolv-conf
   pip install git+https://github.com/animeshxd/dnspython
   ```
   Install with all extra dependencies
   ```bash
   pip install "pyromongo[gssapi,aws,ocsp,snappy,srv,zstd,encryption]"
   ```
  Check other required dependencies for motor
  https://motor.readthedocs.io/en/stable/installation.html#dependencies
  
