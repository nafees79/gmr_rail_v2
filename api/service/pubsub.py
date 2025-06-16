# import asyncio, json
# import aioredis.client
# import async_timeout
# import os
# from api.logger.logger import console_logger
# # from api.operations.redis_handler import redis_handler
# import aioredis


# STOPWORD = "STOP"


# def load_config():
#     env_file = os.path.join(os.getcwd(), "envs", "env.json")
#     f = open(env_file)
#     config = json.load(f)
#     return config

# config = load_config()

# # redis = aioredis.Redis.from_url(
# #      f"redis://{config.get('HOST')}",password="91f7e0815477ae4e3ab95be4c9a513a1e69001b55a75a5360461b7b7ed34debf", max_connections=10, decode_responses=True
# #      )

# #-----------
# # host = os.environ.get(config.get("HOST"), "172.21.97.33")
# # redis = aioredis.Redis.from_url(
# #         f"redis://{host}",password="91f7e0815477ae4e3ab95be4c9a513a1e69001b55a75a5360461b7b7ed34debf", max_connections=10, decode_responses=True
# #     )

# #-----------
# redis = aioredis.Redis.from_url(
#        f"redis://192.168.1.57",password="91f7e0815477ae4e3ab95be4c9a513a1e69001b55a75a5360461b7b7ed34debf", max_connections=10, decode_responses=True
#    )

# # psub = redis.pubsub()

# # async def pubsub():    
# #     async def reader(channel: aioredis.client.PubSub):
        
# #         while True:
# #             try:
                
                
# #                 async with async_timeout.timeout(1):
# #                     message = await channel.get_message(ignore_subscribe_messages=True)
# #                     if message is not None:
# #                         console_logger.debug(f"(Reader) --------------------------------------------- Message Received: {message}")
# #                         if message.get("channel") == "GMR_Fasttag":
# #                             if message.get("channel") == "GMR_Dash_lr":
# #                                 lr_data = json.loads(message.get("data"))
# #                                 # console_logger.debug("----------------------------------------------------", lr_data)
# #                             fastag_data = json.loads(message.get("data"))
# #                             console_logger.debug(fastag_data)
# #                             # await fastag_update(fastag_data)
# #                             # await track_fastag(fastag_data=fastag_data)
# #                             await redis_handler.register_fastag(fastag_data)
# #                             # await test_fastag(fastag_data=fastag_data)
# #                             await redis_handler.SetFTData(fastag_data)
# #                             # console_logger.debug(json.loads(message.get("data")))
# #                         if message.get("channel") == "WeighBridge":
# #                             fastag_data = json.loads(message.get("data"))
# #                             # await track_fastag(WeightData=fastag_data)
# #                             # await test_fastag(WeightBridge=fastag_data)
# #                             # await test_weighbridge(WeightBridge=fastag_data)
# #                             await redis_handler.SetWBData(fastag_data)
# #                         if message["data"] == STOPWORD:
# #                             console_logger.debug(" Reader STOP")
# #                             break                        
# #                     await asyncio.sleep(0.01)
# #             except Exception as e:
# #                 console_logger.debug(e)
# #                 pass

# #     async with psub as p:
# #         await p.subscribe("GMR_Fasttag")
# #         await p.subscribe("GMR_portal")
# #         await p.subscribe("WeighBridge")
# #         output = await reader(p)  # wait for reader to complete
# #         # console_logger.debug(output.get("data"))
# #         # await p.unsubscribe("GMR_Dash")


# #     # closing all open connections
# #     await psub.close()
