# Discord Dashboard

To run:

```
git clone https://github.com/TigerGraph-OSS/C360-DiscordDash.git
cd C360-DiscordDash/DiscordDashboard
touch configs.py
```

In configs.py, add:

```
secret = "INSERT_SECRET_FOR_GRAPH"
token = "INSERT_DISCORD_BOT_TOKEN"
```

Finally, run:

```
flask run
```
