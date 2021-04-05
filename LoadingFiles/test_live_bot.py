'''
Live Bot Tests
'''

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
    print(message.author)


client.run(configs.token)
