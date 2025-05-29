
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
# Create a new client and connect to the server
MONGODB_URI = "mongodb+srv://vercel-admin-user:sgBvgwOj8K5cl29M@campus-face.rhsjkmy.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

# o de baixo é o pessoal
# uri = "mongodb+srv://henrique12095:campusfacedb@campus-face.rhsjkmy.mongodb.net/?retryWrites=true&w=majority&appName=campus-face"
LOCAL_URI = "mongodb://localhost:27017"
client = MongoClient(LOCAL_URI, server_api=ServerApi('1'))

db = client.campusFace

usersCollection = db['users']
hubsCollection = db['hubs']

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)



# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)