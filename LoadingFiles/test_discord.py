import requests
import json
import configs

guild = 640707678297128980

message = 738757670172885092 # 752343815792230490

user = 494006444799295490

channel = 580945580554059796 # 640707678297128982

uid = 473148717814382593

url = f"https://discord.com/api/v8/channels/{channel}/messages?limit=100"
headers = {
    "Authorization": f"Bot {configs.token}"
}
r = requests.get(url, headers=headers)
res = (eval(r.__dict__["_content"].decode(
    "utf-8").replace("null", "None").replace("false", "False").replace("true", "True")))
# print(res)
last_message_id = 0

for message in res:
    print(message["timestamp"])
            # conn.upsertVertex("Message", message["id"], attributes={
            #     "message_id": message["id"], "message_content": message["content"]})
            # conn.upsertEdge(
            #     "Message", message["id"], "SENDER", "User", message["author"]["id"])
            # conn.upsertEdge(
            #     "Message", message["id"], "MESSAGE_CHANNEL", "Channel", channel['id'])
            # last_message_id = message["id"]

# # Get all members
# url = f"https://discord.com/api/v8/guilds/{guild}/members?limit=1000"

# headers = {
#     "Authorization": f"Bot {configs.token}"
# }

# r = requests.get(url, headers=headers)
# res = eval(r.__dict__["_content"].decode(
#     "utf-8").replace("null", "None").replace("false", "False").replace("true", "True"))
# print((res[1]['joined_at'][:4]), res[1]['joined_at'][5:7], res[1]['joined_at'][8:10])

# for i in res:
#     print(i["joined_at"])

# url = f"https://discord.com/api/v8/users/{uid}"
# headers = {
#     "Authorization": f"Bot {configs.token}"
# }

# r = requests.get(url, headers=headers)
# res = eval(r.__dict__["_content"].decode(
#     "utf-8").replace("null", "None").replace("false", "False").replace("true", "True"))
# print((res))

# Get the Messages
# url = "https://discord.com/api/v8/channels/667378024060026890/messages?limit=100"

# headers = {
#     "Authorization": f"Bot {configs.token}"
# }

# r = requests.get(url, headers=headers)
# print(r)
# res = eval(r.__dict__["_content"].decode(
#     "utf-8").replace("null", "None").replace("false", "False").replace("true", "True"))[::-1]
# print([i["content"] for i in res])
# print(len(res))
# print(r.__dict__)
# It only results in the last 50 messages

# def transform(message):
#     return message.content


# @bot.command()
# async def history(ctx, channel: discord.TextChannel):
#     messages_in_channel = await channel.history(limit=10).map(transform).flatten()

#     print(messages_in_channel)

