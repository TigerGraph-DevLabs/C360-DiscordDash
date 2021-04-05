import discord
import pyTigerGraph as tg
import configs 


client = discord.Client()

conn = tg.TigerGraphConnection(host="https://discord.i.tgcloud.io",
                               password="tigergraph", gsqlVersion="3.0.5", useCert=True)

conn.graphname = "DiscordGraph"
conn.apiToken = conn.getToken(conn.createSecret())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    print(message.channel)
    conn.upsertVertex("Message", message.id, attributes={
        "message_id": message.id, "message_content": message.content})
    conn.upsertEdge("Message", message.id,
                    "SENDER", "User", message.author)
    conn.upsertEdge(
        "Message", message["id"], "MESSAGE_CHANNEL", "Channel", message.channel)
    if len(message.mentions) > 0:
        for mentionned in message.mentions:
            conn.upsertEdge(
                "Message", message.id, "MENTIONS", "User", mentionned.id)


client.run(configs.token)
