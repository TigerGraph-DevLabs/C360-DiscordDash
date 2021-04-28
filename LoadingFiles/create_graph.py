'''
Create Graph + Queries
'''

import pyTigerGraph as tg 

conn = tg.TigerGraphConnection(host="https://discord.i.tgcloud.io",
                               password="tigergraph", gsqlVersion="3.0.5", useCert=True)

# print(conn.gsql('''DROP ALL''', options=[]))

print(conn.gsql('''
CREATE VERTEX Message (PRIMARY_ID message_id STRING, message_content STRING) WITH primary_id_as_attribute="true"
CREATE VERTEX Channel (PRIMARY_ID channel_id STRING, channel_name STRING) WITH primary_id_as_attribute="true"
CREATE VERTEX Category (PRIMARY_ID category_id STRING, category_name STRING) WITH primary_id_as_attribute="true"
CREATE VERTEX User (PRIMARY_ID id STRING, username STRING, avatar STRING, discriminator STRING) WITH primary_id_as_attribute="true"

CREATE VERTEX Year (PRIMARY_ID year STRING) WITH primary_id_as_attribute="true"
CREATE VERTEX Month (PRIMARY_ID month STRING) WITH primary_id_as_attribute="true"
CREATE VERTEX Day (PRIMARY_ID day STRING) WITH primary_id_as_attribute="true"

CREATE UNDIRECTED EDGE CHANNEL_CATEGORY (FROM Channel, TO Category)
CREATE UNDIRECTED EDGE SENDER (FROM Message, TO User)
CREATE UNDIRECTED EDGE MENTIONS (FROM Message, TO User)
CREATE UNDIRECTED EDGE MESSAGE_CHANNEL (FROM Message, TO Channel)

CREATE UNDIRECTED EDGE MESSAGE_YEAR (FROM Message, TO Year)
CREATE UNDIRECTED EDGE MESSAGE_MONTH (FROM Message, TO Month)
CREATE UNDIRECTED EDGE MESSAGE_DAY (FROM Message, TO Day)
CREATE UNDIRECTED EDGE USER_YEAR (FROM User, TO Year)
CREATE UNDIRECTED EDGE USER_MONTH (FROM User, TO Month)
CREATE UNDIRECTED EDGE USER_DAY (FROM User, TO Day)
CREATE UNDIRECTED EDGE YEAR_MONTH (FROM Year, TO Month)
CREATE UNDIRECTED EDGE MONTH_DAY (FROM Month, TO Day)
''', options=[]))

print(conn.gsql('''CREATE GRAPH DiscordGraph(Message, Channel, Category, User, 
                    MESSAGE_CHANNEL, CHANNEL_CATEGORY, SENDER, MENTIONS,
                    Year, Month, Day, 
                    MESSAGE_YEAR, MESSAGE_MONTH, MESSAGE_DAY, 
                    YEAR_MONTH, MONTH_DAY,  
                    USER_YEAR, USER_MONTH, USER_DAY)''',
                options=[]))  # Create the Graph

conn.graphname = "DiscordGraph"
conn.apiToken = conn.getToken(conn.createSecret())

'''
CREATE QUERY getTotalUsers(/* Parameters here */) FOR GRAPH DiscordGraph { 
  /* Write query logic here */ 
    SumAccum<int> @@total = 0;
    Seed = {User.*};
    Res = SELECT s FROM Seed:s
          ACCUM @@total+=1;

    PRINT @@total;
    PRINT Seed;
}
'''

'''
CREATE QUERY getTotalProjects(STRING id) FOR GRAPH DiscordGraph { 
  /* Write query logic here */ 
  SumAccum<int> @@total = 0;
  Seed = {Category.*};
  Res = SELECT t FROM Seed:s- (CHANNEL_CATEGORY:e)-Channel:t
  WHERE s.category_id == id
  ACCUM @@total+=1;
  
  PRINT @@total;
}
'''

'''
CREATE QUERY getTotalMessages(/* Parameters here */) FOR GRAPH DiscordGraph { 
  /* Write query logic here */ 
  SumAccum<int> @@total = 0;
  Seed = {Message.*};
  Res = SELECT s FROM Seed:s
  ACCUM @@total+=1;
  
  PRINT @@total;
}
'''

'''
CREATE QUERY getTotalChannels(/* Parameters here */) FOR GRAPH DiscordGraph { 
  /* Write query logic here */ 
  SumAccum<int> @@total = 0;
  Seed = {Channel.*};
  Res = SELECT s FROM Seed:s
  ACCUM @@total+=1;
  
  PRINT @@total;
}
'''

'''
CREATE QUERY getTopUsers() FOR GRAPH DiscordGraph {  
  SumAccum<int> @totalMessages = 0;
  
  Seed = {Message.*};
  
  Res = SELECT t FROM Seed:s- (SENDER:e)-User:t 
        ACCUM t.@totalMessages+=1
        HAVING t.@totalMessages > 0
        ORDER BY t.@totalMessages DESC
        LIMIT 100;
  
  PRINT Res;
}
'''

'''
CREATE QUERY getMessagesByMonth(STRING month, STRING year) FOR GRAPH DiscordGraph { 
  SumAccum<int> @@total = 0;
  
  Seed = {Message.*};
  
  YearlyMessages = SELECT m FROM Seed:m -(MESSAGE_YEAR:e)-Year:y
                    WHERE y.year == year;
  messages = SELECT m FROM YearlyMessages:m -(MESSAGE_MONTH:e)-Month:y
                    WHERE y.month == month
                    ACCUM @@total+=1;
  
  PRINT @@total;
  PRINT messages;
}
'''

'''
CREATE QUERY getUsersByMonth(STRING month, STRING year) FOR GRAPH DiscordGraph { 
  SumAccum<int> @@total = 0;
  
  Seed = {User.*};
  
  YearlyUsers = SELECT m FROM Seed:m -(USER_YEAR:e)-Year:y
                    WHERE y.year == year;
  users = SELECT m FROM YearlyUsers:m -(USER_MONTH:e)-Month:y
                    WHERE y.month == month
                    ACCUM @@total+=1;
  
  PRINT @@total;
  PRINT users;
}
'''
