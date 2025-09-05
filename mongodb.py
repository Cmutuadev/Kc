import traceback
import pymongo

# Use your actual Atlas connection details below.
mongodb_uri = (
    "mongodb://myproject:myproject@"
    "cluster0-shard-00-00.wqcf3.mongodb.net:27017,"
    "cluster0-shard-00-01.wqcf3.mongodb.net:27017,"
    "cluster0-shard-00-02.wqcf3.mongodb.net:27017/"
    "MASTER_DATABASE?ssl=true&replicaSet=atlas-xxxxxx-shard-0&authSource=admin&retryWrites=true&w=majority"
)

try:
    client = pymongo.MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
    # Force a call to check connection
    client.server_info()
    print("MONGODB CONNECTED SUCCESSFULLY ✅")
except Exception as e:
    print("MONGODB CONNECTION FAILED ❌")
    print(traceback.format_exc())
    exit(1)

folder = client["MASTER_DATABASE"]
usersdb = folder.USERSDB
chats_auth = folder.CHATS_AUTH
gcdb = folder.GCDB
sksdb = client["SKS_DATABASE"].SKS
confdb = client["SKS_DATABASE"].CONF_DATABASE
