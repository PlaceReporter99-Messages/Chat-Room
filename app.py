from pymongo import MongoClient
import os
import get_config

db = MongoClient(f"mongodb://HMS_coveryouth:{os.environ["DB_PASSWORD"]}@qxw.h.filess.io:27018/HMS_coveryouth")["HMS_coveryouth"]