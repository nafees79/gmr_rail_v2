# from api import asio

# async def push_update_transporter(update: dict, data_type: str):
#     try:
#         # print("[sioclient]--- 22 ---", update, "emitteddd_data")

#         if data_type == "pending_gate":
#             await asio.emit("update-transport", data={"update": update, "type": data_type})

#         elif data_type == "pending_lr":
#             await asio.emit("update-transport", data={"update": update, "type": data_type})

#         elif data_type == "inqueue_lr":
#             await asio.emit("update-transport", data={"update": update, "type": data_type})
#     except Exception as e:
#         print("[sioclient]--- 33 ---", e)