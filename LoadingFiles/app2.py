from flask import Flask
from flask import render_template
from flask import request, send_from_directory
import pyTigerGraphBeta as tg
import configs

configs = {
    "server": "https://rasa.i.tgcloud.io",
    "user": "tigergraph",
    "password": "tigergraph",
    "version": "3.1.0",
    "graph": "c360",
    "secret": configs.secret
}


app = Flask(__name__, static_url_path='/static')

# conn = tg.TigerGraphConnection(host="https://discord.i.tgcloud.io",
#                                password="tigergraph", useCert=True)

# conn.graphname = "DiscordGraph"
# conn.apiToken = conn.getToken(configs["secret"])


@app.route('/')
def main():
    return render_template("index2.html")


if __name__ == '__main__':
    app.run(debug=True)
