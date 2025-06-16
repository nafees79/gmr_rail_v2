# from api import gmrdata
# import redis as cache
# from api import asio

# import datetime, os, requests, json

# # host = os.environ.get("HOST", "192.168.1.57")

# def load_config():
#     env_file = os.path.join(os.getcwd(), "envs", "env.json")
#     f = open(env_file)
#     config = json.load(f)
#     return config

# config = load_config()

# cacher = cache.Redis.from_url(
#     f"redis://{config.get('HOST')}",password="91f7e0815477ae4e3ab95be4c9a513a1e69001b55a75a5360461b7b7ed34debf", max_connections=10, decode_responses=True
#      )

# # print("------- socketcall [20] ----", f"{config.get('HOST')}")

# vehicle_data = []

# # async def send_pending_weight_vehicle(data):
# #     await asio.emit("frontend", data)

# async def send_pending_weight_vehicle(data):
#     await asio.emit("frontend", data)


# async def send_weight_bridge_status(data):
#     await asio.emit("wb_status", data)


# # async def send_weight_bridge_data(data):
# #     # print("-----socketcall [36] ---------------",data)
# #     await asio.emit("wb_data", data)


# # def get_truck_registration_details():
# #     # url = f"http://{host}/api/v1/frservice/groupwise/plates?group=default&page_no=1&page_size=100000&search="
# #     url = f"http://{config.get('HOST')}/api/v1/frservice/groupwise/plates?group=default&page_no=1&page_size=100000&search="
# #     response = requests.request("GET", url)
# #     data = json.loads(response.content)
# #     print("------- socketcall [45] --------------------",data)
# #     registered = []
    
# #     for i in data.get("data").get("plates"):
# #         registered.append(i.get("plate_no"))
# #     data = json.dumps({"data":registered})
# #     # print("getting registered vehicles:",data)
# #     cacher.set("registered_vehicle", data, ex=60*30)

# def get_truck_registration_details():
#     host = config.get('HOST')
#     page_no = 1
#     page_size = 1000
#     registered = []

#     while True:
#         url = f"http://{host}/api/v1/frservice/groupwise/plates?group=default&page_no={page_no}&page_size={page_size}&search="
#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#             data = response.json()

#             plates = data.get("data", {}).get("plates", [])
#             if not plates:
#                 break

#             for plate in plates:
#                 registered.append(plate.get("plate_no"))

#             page_no += 1         # next page

#         except requests.exceptions.HTTPError as http_err:
#             print(f"HTTP error occurred: {http_err}")
#             break
#         except Exception as err:
#             print(f"Other error occurred: {err}")
#             break

#     data = json.dumps({"data": registered})
#     cacher.set("registered_vehicle", data, ex=60 * 30)



# def GetPendingWeightVehicles():
#     data = cacher.get("registered_vehicle")

#     if not data or len(data) == 0:
#         get_truck_registration_details()
#     data = json.loads(cacher.get("registered_vehicle"))
#     # print(data)
#     pipeline = [
#         {
#             "$match": {
#                 'lr_fasttag': True,
#                 'gate_approved': True,
#                 'gate_fastag': True,
#                 'transporter_lr_no': {"$ne": None},
#                 'vehicle_in_time':{"$gt":datetime.datetime.utcnow() - datetime.timedelta(hours=4)},
#                 "$or": [
#                     {"actual_gross_qty": {"$eq": None}},
#                     {"actual_tare_qty": {"$eq": None}}
#                 ]
#             }
#         },
#         {
#             "$group": {
#                 "_id": "$vehicle_number",
#                 "status": {
#                     "$max": {
#                         "$cond": [
#                             {"$eq": ["$actual_gross_qty", None]},
#                             "pending",
#                             "in_progress"
#                         ]
#                     }
#                 }
#             }
#         },
#         {
#             "$sort": {"_id": 1}  # Sort by vehicle_number within each status group
#         },
#         {
#             "$facet": {
#                 "in_progress": [
#                     {"$match": {"status": "in_progress"}},
#                     {
#                         "$group": {
#                             "_id": None,
#                             "vehicles": {"$push": "$_id"}
#                         }
#                     },
#                     {"$project": {"_id": 0, "vehicles": 1}}
#                 ],
#                 "pending": [
#                     {"$match": {"status": "pending"}},
#                     {
#                         "$group": {
#                             "_id": None,
#                             "vehicles": {"$push": "$_id"}
#                         }
#                     },
#                     {"$project": {"_id": 0, "vehicles": 1}}
#                 ]
#             }
#         }
#     ]

#     result = list(gmrdata.aggregate(pipeline))
#     in_progress_registered = []
#     in_progress_unregistered = []
#     pending_registered = []
#     pending_unregistered = []
#     for k, v in result[0].items():
#         if k == "in_progress":
#             if len(v) > 0:
#                 # print("---------- socketcall 111 -------------",v[0].get("vehicles"), "data", data)
#                 in_progress_registered = list(set(v[0].get("vehicles")).intersection(set(data.get("data"))))
#                 in_progress_unregistered = list(set(v[0].get("vehicles")).difference(set(in_progress_registered)))
#         else:
#             if len(v) > 0:
#                 # print("---------- socketcall 116 -------------",v[0].get("vehicles"))
#                 pending_registered = list(set(v[0].get("vehicles")).intersection(set(data.get("data"))))
#                 pending_unregistered = list(set(v[0].get("vehicles")).difference(set(pending_registered)))
            
#     return {"outdata": {"progress_registerd":in_progress_registered,
#             "progress_unregisterd":in_progress_unregistered,
#             "pending_registered": pending_registered,
#             "pending_unregistered": pending_unregistered}}

