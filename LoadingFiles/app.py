from flask import Flask
from flask import render_template
from flask import request, send_from_directory
import pyTigerGraphBeta as tg 
import requests
import configs

configs = {
    "server" : "https://rasa.i.tgcloud.io",
    "user" : "tigergraph",
    "password" : "tigergraph",
    "version" : "3.1.0",
    "graph" : "c360",
    "secret": configs.secret
}


app = Flask(__name__, static_url_path='/static')

conn = tg.TigerGraphConnection(host="https://discord.i.tgcloud.io",
                               password="tigergraph", useCert=True)

conn.graphname = "DiscordGraph"
conn.apiToken = conn.getToken(configs["secret"])

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('static/images', path)


@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('static/fonts', path)

# conn = tg.TigerGraphConnection(host=configs["server"], graphname=configs["graph"], username=configs["user"], password=configs["password"])

# conn.apiToken = conn.getToken(configs["secret"])


# Get Most Starred Repos ?

# GetMostStarred = conn.runInstalledQuery("GetMostStarred")[0]["Result"]
# resSorted = sorted(GetMostStarred, key = lambda i: i['StarCount'],reverse=True)
RepoStarsList = [] # resSorted[:40]

# Get the Most Active Users 

GetMostActiveUsers = conn.runInstalledQuery("getMostActiveUsers")[0]["Res"]
# usrSorted = sorted(GetMostActiveUsers, key = lambda i: i['valueStars'],reverse=True)
UserStarsList = [i["attributes"] for i in GetMostActiveUsers]  # usrSorted[:20]
for i in range(len(UserStarsList)):
    UserStarsList[i]["messages"] = UserStarsList[i]["@messages"]
# repo Count 

url = f"https://discord.com/api/v8/guilds/640707678297128980/members?limit=1000"

headers = {
    "Authorization": f"Bot {configs.token}"
}

r = requests.get(url, headers=headers)
res = eval(r.__dict__["_content"].decode(
    "utf-8").replace("null", "None").replace("false", "False").replace("true", "True"))

repoCount =  conn.runInstalledQuery("getMessagesByMonth", 
                params={"year": "2021", "month": "03"})[0]["@@total"]
repoUsers = len(res)
repoStars = conn.runInstalledQuery("getTotalMessages")[0]["@@total"]
repoOwners = conn.runInstalledQuery("getTotalUsers")[0]["@@total"]

@app.route('/')
def index():
    Github = {
        "repoCount" : repoCount,
        "repoUsers" : repoUsers,
        "repoStars" : repoStars,
        "repoOwners" : repoOwners,
        }
    import json
    varList = [
        {'time': '2019', 'type': 'New Users',
            "value": conn.runInstalledQuery("getUsersByYear", params={"year": "2019"})[0]["@@total"]},
        {'time': '2019', 'type': 'Messages', "value": conn.runInstalledQuery(
            "getMessagesByYear", params={"year": "2019"})[0]["@@total"]},
        {'time': '2020', 'type': 'New Users', "value": conn.runInstalledQuery(
            "getUsersByYear", params={"year": "2020"})[0]["@@total"]},
        {'time': '2020', 'type': 'Messages', "value": conn.runInstalledQuery(
            "getMessagesByYear", params={"year": "2020"})[0]["@@total"]},
        {'time': '2021', 'type': 'Messages', "value": conn.runInstalledQuery(
            "getMessagesByYear", params={"year": "2021"})[0]["@@total"]},
        {'time': '2021', 'type': 'New Users', "value": conn.runInstalledQuery(
            "getUsersByYear", params={"year": "2021"})[0]["@@total"]},


    ]
    
    return render_template('index.html', ListValues=varList, Github=Github, RepoStarsList=RepoStarsList, UserStarsList=UserStarsList)



@app.route('/chart')
def testChartAnt():
    import json 
    varList = [
        {'time': '2019', 'type': 'New Users',
            "value": conn.runInstalledQuery("getUsersByYear", params={"year": "2019"})[0]["@@total"]},
        {'time': '2019', 'type': 'Messages', "value": conn.runInstalledQuery(
            "getMessagesByYear", params={"year": "2019"})[0]["@@total"]},
        {'time': '2020', 'type': 'New Users', "value": conn.runInstalledQuery(
            "getUsersByYear", params={"year": "2020"})[0]["@@total"]},
        {'time': '2020', 'type': 'Messages', "value": conn.runInstalledQuery(
            "getMessagesByYear", params={"year": "2020"})[0]["@@total"]},
        {'time': '2021', 'type': 'Messages', "value": conn.runInstalledQuery(
            "getMessagesByYear", params={"year": "2021"})[0]["@@total"]},
        {'time': '2021', 'type': 'New Users', "value": conn.runInstalledQuery(
            "getUsersByYear", params={"year": "2021"})[0]["@@total"]},
      

    ]
    print(varList)
    return render_template('chart.html',ListValues=varList)


@app.route('/pie')
def testPieAnt():
   
    return render_template('/G6/LargeGraph.html')

@app.route('/intents')
def intents():
    # try:
    #     res = conn.runInstalledQuery("getUnkownVertex")[0]["ss"]
    # except Exception as e:
    #     print(e)
    res = []
    return render_template('table.html',res=res)


@app.route('/add', methods=['POST'])
def intents_add():
    ids = "Value" #request.form['id']
    return render_template('add.html',ids=ids)


@app.route('/<string:name>')
def do_this(name):
    return render_template(name)

if __name__ == '__main__':
    app.run(debug=True)
