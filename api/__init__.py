from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import os
# import socketio
import json
import pymongo
# mongodb://admin:%40ccessDenied321@192.168.1.42:27017/gmrdbprod?authSource=admin

mongoClient = pymongo.MongoClient("mongodb://admin:%40ccessDenied321@192.168.1.42:27017/GMR_DB?authSource=admin")
gmrDB = mongoClient.get_database("GMR_DB")
gmrdata = gmrDB.get_collection("gmrdata")
weighbridgeDB= gmrDB.get_collection("weighbridge")
ucparam = gmrDB.get_collection("usecaseparameters")

short_mine_collection = gmrDB.get_collection("short_mine")

# ####################### 7704 ######################
gmrrequest = gmrDB.get_collection("gmrrequest")
email_development_check = gmrDB.get_collection("EmailDevelopmentCheck")
reportscheduler = gmrDB.get_collection("reportscheduler")
gmrdataHistoric = gmrDB.get_collection("gmrdataHistoric")
SapRecords = gmrDB.get_collection("SapRecords")
raildb = gmrDB.get_collection("raildb")
sapdb = gmrDB.get_collection("SapRecords")


def load_config():
    env_file = os.path.join(os.getcwd(), "envs", "env.json")
    f = open(env_file)
    config = json.load(f)
    return config

Config = load_config()

SECRET_KEY = "e61ce28e801e466eb3c1701432a8f60c6f7069d2602f43ebac3df93eb986bce8"
ALGORITHM = "HS256"
# mgr = socketio.AsyncRedisManager('redis://:91f7e0815477ae4e3ab95be4c9a513a1e69001b55a75a5360461b7b7ed34debf@{}:6379/0'.format(Config.get('HOST')), )
# asio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*", client_manager=mgr, async_handlers=True, engineio_logger=True)

def startup():
    '''
    call your startup function here
    '''
    

def shutdown():
    '''
    call your shutdown function here
    '''

@asynccontextmanager
async def lifespan(app: FastAPI):
    # run startup function
    startup()
    yield
    #run shutdown function
    shutdown()

def createapp():
    
    app = FastAPI(
        title="GMR Rail Operations",
        description="Rail Operations",
        version="2.0.0",
        openapi_url="/api/v2/gmr/rail_operations/openapi.json",
        docs_url="/api/v2/gmr/rail_operations/docs",
        lifespan=lifespan
    )

    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

    from api.service.routes import router
    app.include_router(router=router, prefix="/api/v2/gmr/rail_operations")
    return app

app = createapp()









# import mongoengine

# mongoengine.connect(
#     db="gmrdbprod1",
#     username="admin",
#     password="%40ccessDenied321",
#     host="192.168.1.42",       
#     port=27017,
#     authentication_source="admin"  
# )

# class GmrData(mongoengine.Document):
#     meta = {"collection": "gmrdata"}

# class Weighbridge(mongoengine.Document):
#     meta = {"collection": "weighbridge"}

# class UcParam(mongoengine.Document):
#     meta = {"collection": "usecaseparameters"}

# gmr_data = GmrData.objects()
# weighbridge_data = Weighbridge.objects()
# uc_param_data = UcParam.objects() 