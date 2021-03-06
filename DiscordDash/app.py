from flask import Flask
from flask import render_template
from flask import request, send_from_directory
from flask.json import jsonify
import pyTigerGraphBeta as tg 
import configs
import requests 
import json

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'Api-Key' : '',
    'Api-Username': 'Zrouga'
}

config = {
    "server": "https://rasa.i.tgcloud.io",
    "user": "tigergraph",
    "password": "tigergraph",
    "version": "3.1.0",
    "graph": "c360",
    "secret": configs.secret
}


app = Flask(__name__, static_url_path='/static')

conn = tg.TigerGraphConnection(host="https://discord.i.tgcloud.io",
                               password="tigergraph", useCert=True)

conn.graphname = "DiscordGraph"
conn.apiToken = conn.getToken(config["secret"])


# config = {
#     "server" : "https://rasa.i.tgcloud.io",
#     "user" : "tigergraph",
#     "password" : "tigergraph",
#     "version" : "3.1.0",
#     "graph" : "c360",
#     "secret" : "49j0bikopko1kv6lm0a79rk202m7slnk",
# }


app = Flask(__name__, static_url_path='/static')

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

# conn = tg.TigerGraphConnection(host=config["server"], graphname=config["graph"], username=config["user"], password=config["password"])

# conn.apiToken = conn.getToken(config["secret"])


# Get Most Starred Repos ?

# GetMostStarred = conn.runInstalledQuery("GetMostStarred")[0]["Result"]
# resSorted = sorted(GetMostStarred, key = lambda i: i['StarCount'],reverse=True)
RepoStarsList = [] # resSorted[:40]

# Get the Most Active Users 

# GetMostActiveUsers = conn.runInstalledQuery("getMostActiveUsers")[0]["Result"]
# usrSorted = sorted(GetMostActiveUsers, key = lambda i: i['valueStars'],reverse=True)
UserStarsList = [] #usrSorted[:20]

# repo Count 
repoCount =  0 #conn.runInstalledQuery("getTotalProjects")[0]["RepoCount"]
repoUsers = 0 #conn.runInstalledQuery("getTotalUsers")[0]["UsersCount"]
repoStars = 0 #conn.runInstalledQuery("GetStarsCount")[0]["StarsCount"]  
repoOwners = 0 #conn.runInstalledQuery("OwnersCount")[0]["OwnersCount"]  

@app.route('/')
def index():
    Github = {
        "repoCount" : repoCount,
        "repoUsers" : repoUsers,
        "repoStars" : repoStars,
        "repoOwners" : repoOwners,
        }
    
    
    return render_template('index.html',Github=Github,RepoStarsList=RepoStarsList,UserStarsList=UserStarsList)



@app.route('/chart')
def testChartAnt():
    import json 
    varList = [
      { 'time': '16 Q1', 'type': 'Test', "value": 0 },
      { 'time': '16 Q1', 'type': 'TEST2', "value": 17.8 },
      { 'time': '16 Q2', 'type': 'TEST2', "value": 69.4 },
      { 'time': '16 Q1', 'type': 'TEST2', "value": 12.8 },
      { 'time': '16 Q3', 'type': 'TEST2', "value": 0 },
      { 'time': '16 Q2', 'type': 'TEST2', "value": 18.1 },

    ]
    print(varList)
    return render_template('chart.html',ListValues=varList)


@app.route('/pie')
def testPieAnt():
   
    return render_template('/G2/CalendarHeatmap.html')

@app.route('/intents')
def intents():
    # try:
    #     res = conn.runInstalledQuery("getUnkownVertex")[0]["ss"]
    # except Exception as e:
    #     print(e)
    res = []
    return render_template('table.html',res=res)

@app.route('/communityOverview')
def communityOverview():
    stats = [] # requests.get("https://community.tigergraph.com/about.json", headers=headers)
    # if (stats.status_code == 200):
    #     stats = stats.json()['about']['stats']
    url = f"https://discord.com/api/v8/guilds/640707678297128980/members?limit=1000"
    headers = {
        "Authorization": f"Bot {configs.token}"
    }
    r = requests.get(url, headers=headers)
    res = eval(r.__dict__["_content"].decode(
        "utf-8").replace("null", "None").replace("false", "False").replace("true", "True"))

    monthlyMessages = conn.runInstalledQuery("getMessagesByMonth",
                                    params={"year": "2021", "month": "03"})[0]["@@total"]
    activeUsers = len(res)
    totalMessages = conn.runInstalledQuery("getTotalMessages")[0]["@@total"]
    totalUsers = conn.runInstalledQuery("getTotalUsers")[0]["@@total"]

    icons = {
        "monthlyMessages": monthlyMessages,
        "activeUsers": activeUsers,
        "totalMessages": totalMessages,
        "totalUsers": totalUsers
    }

    messagesMonth = []
    for year in range(2019, 2022):
        for i in range(1, 10):
            monthlyMessages = conn.runInstalledQuery("getMessagesByMonth",
                                                    params={"year": f"{year}", "month": f"0{i}"})[0]["@@total"]
            messagesMonth.append({"x": f"{year}-0{i}", "y": monthlyMessages})
        for i in range(10, 13):
            monthlyMessages = conn.runInstalledQuery("getMessagesByMonth",
                                                    params={"year": f"{year}", "month": f"{i}"})[0]["@@total"]
            messagesMonth.append({"x": f"{year}-{i}", "y": monthlyMessages})
    usersMonth = []
    for year in range(2019, 2022):
        for i in range(1, 10):
            monthlyUsers = conn.runInstalledQuery("getUsersByMonth",
                                                     params={"year": f"{year}", "month": f"0{i}"})[0]["@@total"]
            usersMonth.append({"x": f"{year}-0{i}", "y": monthlyUsers})
        for i in range(10, 13):
            monthlyUsers = conn.runInstalledQuery("getUsersByMonth",
                                                     params={"year": f"{year}", "month": f"{i}"})[0]["@@total"]
            usersMonth.append({"x": f"{year}-{i}", "y": monthlyUsers})
    stats = {
        "posts": messagesMonth,
        "signups":  usersMonth
    }
    return render_template('communityOverview.html', icons=icons, stats=stats)

@app.route('/communityUsers')
def communityUsers():
    # users = requests.get("https://community.tigergraph.com/admin/users/list/active.json?order=posts_read", headers=headers)
    # if (users.status_code == 200):
    #     users = users.json()
    #     for user in users:
    #         user['avatar_template'] = user['avatar_template'].replace("{size}", "100")
    users = conn.runInstalledQuery("getMostActiveUsers")[0]["Res"]
    users = [i["attributes"] for i in users]
    for user in range(len(users)):
        users[user]["messages"] = users[user]["@messages"]
    
    return render_template('communityUsers.html', users=users)

@app.route('/community/fetch/', methods=['POST', 'GET'])
def fetchData():
    pageviews = []
    signups = []
    posts = []
    topics =[]
    likes = []
    if request.method == 'POST':
        dates = request.json['data']
        url = f"https://community.tigergraph.com/admin/reports/consolidated_page_views.json?{dates}"
        res = requests.get(url, headers=headers)
        if (res.status_code == 200):
            pageviews = res.json()['report']['data']
       
        url = f"https://community.tigergraph.com/admin/reports/signups.json?{dates}"
        res = requests.get(url, headers=headers)
        if (res.status_code == 200):
            signups = res.json()['report']['data']
        
        url = f"https://community.tigergraph.com/admin/reports/posts.json?{dates}"
        res = requests.get(url, headers=headers)
        if (res.status_code == 200):
            posts = res.json()['report']['data']
       
        url = f"https://community.tigergraph.com/admin/reports/topics.json?{dates}"
        res = requests.get(url, headers=headers)
        if (res.status_code == 200):
            topics = res.json()['report']['data']
        
        url = f"https://community.tigergraph.com/admin/reports/likes.json?{dates}"
        res = requests.get(url, headers=headers)
        if (res.status_code == 200):
            likes = res.json()['report']['data']
    
    return {"pageviews": pageviews, "signups": signups, "posts": posts, "topics": topics, "likes": likes}

@app.route('/add', methods=['POST'])
def intents_add():
    ids = "Value" #request.form['id']
    return render_template('add.html',ids=ids)



if __name__ == '__main__':
    app.run(debug=True)
