'''

'''

import pyTigerGraph as tg
import requests
import json
import configs

guild = 640707678297128980

conn = tg.TigerGraphConnection(host="https://discord.i.tgcloud.io",
                               password="tigergraph", gsqlVersion="3.0.5", useCert=True)

conn.graphname = "DiscordGraph"
conn.apiToken = conn.getToken(conn.createSecret())
# print(conn.apiToken)

# # Get the User
# url = "https://discord.com/api/v8/users/133999391085166592"

# headers = {
#     "Authorization": f"Bot {configs.token}"
# }

# r = requests.get(url, headers=headers)
# res = eval(r.__dict__["_content"].decode("utf-8").replace("null", "None").replace("false", "False").replace("true", "True"))
# print(res)
# # I'm not getting the email quite yet. 

# # Get all members
url = f"https://discord.com/api/v8/guilds/{guild}/members?limit=1000"

headers = {
    "Authorization": f"Bot {configs.token}"
}

r = requests.get(url, headers=headers)
res = eval(r.__dict__["_content"].decode(
    "utf-8").replace("null", "None").replace("false", "False").replace("true", "True"))
print(len(res))

for user_info in res:
    user = user_info["user"]
    if user["avatar"]:
        url = f"https://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png"
        conn.upsertVertex("User", user["id"], attributes={
                          "id": user["id"], "username": user["username"], "avatar": url, "discriminator": user["discriminator"]})
        conn.upsertVertex("Year", user_info['joined_at'][:4], attributes={
            "year": user_info['joined_at'][:4]
        })
        conn.upsertEdge("User", user["id"], "USER_YEAR",
                        "Year", user_info['joined_at'][:4])
        conn.upsertVertex("Month", user_info['joined_at'][8:10], attributes={
            "month": user_info['joined_at'][8:10]
        })
        conn.upsertEdge("Year", user_info['joined_at'][:4], "YEAR_MONTH",
                        "Month", user_info['joined_at'][8:10])
        conn.upsertEdge("User", user["id"], "USER_MONTH",
                        "Month", user_info['joined_at'][8:10])
        conn.upsertVertex("Day", user_info['joined_at'][5:7], attributes={
            "day": user_info['joined_at'][5:7]
        })
        conn.upsertEdge("Month", user_info['joined_at'][8:10], "MONTH_DAY",
                        "Day", user_info['joined_at'][5:7])
        conn.upsertEdge("User", user["id"], "USER_DAY",
                        "Day", user_info['joined_at'][5:7])
    else: 
        url = f"https://cdn.discordapp.com/embed/avatars/{str(int(user['discriminator']) % 5)}.png"
        conn.upsertVertex("User", user["id"], attributes={
                          "id": user["id"], "username": user["username"], "avatar": url, "discriminator": user["discriminator"]})
    # print(url)


# # conn = tg.TigerGraphConnection(host="https://discord.i.tgcloud.io",
# #                                password="tigergraph", gsqlVersion="3.0.5", useCert=True)

# # conn.graphname = "DiscordGraph"
# # conn.apiToken = conn.getToken(conn.createSecret())
# # # print(conn.apiToken)

# # # conn.upsertVertex("User", res["id"], attributes={
# # #                   "id": res["id"], "username": res["username"], "avatar": res["avatar"], "discriminator": res["discriminator"]})

# # Get the member count
# url = f"https://discord.com/api/v8/guilds/{guild}/preview"
# headers = {
#     f"Bot {configs.token}"
# }

# r = requests.get(url, headers=headers)
# res = (eval(r.__dict__["_content"].decode(
#     "utf-8").replace("null", "None").replace("false", "False").replace("true", "True")))
# print("Approx: ", res["approximate_member_count"])

# # # Get the members
# # url = f"https://discord.com/api/v8/guilds/{guild}/members?limit=500"
# # headers = {
# #     f"Bot {configs.token}"
# # }

# # r = requests.get(url, headers=headers)
# # res = (eval(r.__dict__["_content"].decode(
# #     "utf-8").replace("null", "None").replace("false", "False").replace("true", "True")))
# # print(res)

# # for user in res:
# #     res = user["user"]
# #     # print(res)
# #     conn.upsertVertex("User", res["id"], attributes={"id": res["id"], "username": res["username"], "discriminator": res["discriminator"]})
# # #     if channel["type"] == 4:
# # #         conn.upsertVertex("Category", channel["id"], attributes={
# # #                           "category": channel["id"]})
# # #     elif channel["type"] == 0:
# # #         conn.upsertVertex("Channel", channel["id"], attributes={
# # #                           "channel": channel["id"]})
# # #         conn.upsertEdge(
# # #             "Channel", channel["id"], "CHANNEL_CATEGORY", "Category", channel["parent_id"])

# Get the member channels and the messages
url = f"https://discord.com/api/v8/guilds/{guild}/channels"
headers = {
    "Authorization": f"Bot {configs.token}"
}

r = requests.get(url, headers=headers)
res = (eval(r.__dict__["_content"].decode(
    "utf-8").replace("null", "None").replace("false", "False").replace("true", "True")))
# print(res)

for channel in res:
    if channel["type"] == 4:
        conn.upsertVertex("Category", channel["id"], attributes={
                          "category_id": channel["id"]})
    elif channel["type"] == 0:
        conn.upsertVertex("Channel", channel["id"], attributes={
                          "channel_id": channel["id"]})
        conn.upsertEdge(
            "Channel", channel["id"], "CHANNEL_CATEGORY", "Category", channel["parent_id"])
        
        url = f"https://discord.com/api/v8/channels/{channel['id']}/messages?limit=100"
        headers = {
            "Authorization": f"Bot {configs.token}"
        }
        r = requests.get(url, headers=headers)
        res = (eval(r.__dict__["_content"].decode(
            "utf-8").replace("null", "None").replace("false", "False").replace("true", "True")))
        # print(res)
        last_message_id = 0

        for message in res:
            # print(message["content"], message)
            conn.upsertVertex("Message", message["id"], attributes={
                "message_id": message["id"], "message_content": message["content"]})
            conn.upsertEdge("Message", message["id"], "SENDER", "User", message["author"]["id"])
            conn.upsertEdge(
                "Message", message["id"], "MESSAGE_CHANNEL", "Channel", channel['id'])
            conn.upsertVertex("Year", message["timestamp"][:4], attributes={
                "year": message["timestamp"][:4]
            })
            conn.upsertEdge(
                "Message", message["id"], "MESSAGE_YEAR", "Year", message["timestamp"][:4])
            conn.upsertVertex("Month", message["timestamp"][8:10], attributes={
                "month": message["timestamp"][8:10]
            })
            conn.upsertEdge("Year", message["timestamp"][:4], "YEAR_MONTH",
                            "Month", message["timestamp"][8:10])
            conn.upsertEdge(
                "Message", message["id"], "MESSAGE_MONTH", "Month", message["timestamp"][8:10])
            conn.upsertVertex("Day", message["timestamp"][5:7], attributes={
                "day": message["timestamp"][5:7]
            })
            conn.upsertEdge("Month", message["timestamp"][8:10], "MONTH_DAY",
                            "Day", message["timestamp"][5:7])
            conn.upsertEdge(
                "Message", message["id"], "MESSAGE_DAY", "Day", message["timestamp"][5:7])
            last_message_id = message["id"]
            # if len(message["mentions"]) > 0:
            #     for mentionned in message["mentions"]:
            #         conn.upsertEdge(
            #             "Message", message["id"], "MENTIONS", "User", mentionned["id"])
        
        for i in range(10):
            url = f"https://discord.com/api/v8/channels/{channel['id']}/messages?limit=100&before={last_message_id}"
            headers = {
                "Authorization": f"Bot {configs.token}"
            }
            r = requests.get(url, headers=headers)
            res = (eval(r.__dict__["_content"].decode(
                "utf-8").replace("null", "None").replace("false", "False").replace("true", "True")))
            # print(res)

            for message in res:
                # print(message)
                try:
                    conn.upsertVertex("Message", message["id"], attributes={
                        "message_id": message["id"], "message_content": message["content"]})
                    conn.upsertEdge(
                        "Message", message["id"], "SENDER", "User", message["author"]["id"])
                    conn.upsertEdge(
                        "Message", message["id"], "MESSAGE_CHANNEL", "Channel", channel['id'])
                    conn.upsertVertex("Year", message["timestamp"][:4], attributes={
                        "year": message["timestamp"][:4]
                    })
                    conn.upsertEdge(
                        "Message", message["id"], "MESSAGE_YEAR", "Year", message["timestamp"][:4])
                    conn.upsertVertex("Month", message["timestamp"][8:10], attributes={
                        "month": message["timestamp"][8:10]
                    })
                    conn.upsertEdge("Year", message["timestamp"][:4], "YEAR_MONTH",
                                    "Month", message["timestamp"][8:10])
                    conn.upsertEdge(
                        "Message", message["id"], "MESSAGE_MONTH", "Month", message["timestamp"][8:10])
                    conn.upsertVertex("Day", message["timestamp"][5:7], attributes={
                        "day": message["timestamp"][5:7]
                    })
                    conn.upsertEdge("Month", message["timestamp"][8:10], "MONTH_DAY",
                                    "Day", message["timestamp"][5:7])
                    conn.upsertEdge(
                        "Message", message["id"], "MESSAGE_DAY", "Day", message["timestamp"][5:7])
                    if last_message_id == message["id"]: break
                    else: last_message_id = message["id"]
                    # if len(message["mentions"]) > 0:
                    #     for mentionned in message["mentions"]:
                    #         conn.upsertEdge(
                    #             "Message", message["id"], "MENTIONS", "User", mentionned["id"])
                except:
                    print(message)






# # # Get the Messages
# # url = "https://discord.com/api/v8/channels/819148893044211752/messages"

# # headers = {
# #     "Authorization": f"Bot {configs.token}"
# # }

# # r = requests.get(url, headers=headers)
# # res = eval(r.__dict__["_content"].decode(
# #     "utf-8").replace("null", "None").replace("false", "False").replace("true", "True"))[::-1]
# # print([i["content"] for i in res])
# # print(len(res))
# # # print(r.__dict__)
# # # It only results in the last 50 messages
