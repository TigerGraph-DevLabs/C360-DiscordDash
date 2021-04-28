# Discord Dashboard

To run:

```
git clone https://github.com/TigerGraph-OSS/C360-DiscordDash.git
cd C360-DiscordDash/
touch DiscordDash/configs.py
touch LoadingFiles/configs.py
```

In both of the files called configs.py, add:

```
secret = "INSERT_SECRET_FOR_GRAPH"
token = "INSERT_DISCORD_BOT_TOKEN"
```

To create the graph, run:

```
python3 LoadingFiles/create_graph.py
```

Finally, to run the dashboard, use:

```
cd DiscordDash/
flask run
```
