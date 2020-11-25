import os
import tinydb
from datetime import datetime

class dbquery:
    def __init__(self):
        self.state = "statefarm"

    def DBCheck(self, server_name):
        newpath = r'./database/' + server_name
        if not os.path.exists(newpath):
            os.makedirs(newpath)

    def warnUser(self, server_name, user_id, reason, warner):
        self.DBCheck(server_name)
        db = tinydb.TinyDB("./database/" + server_name + "/warnings.json")
        now = datetime.now()
        nowstrft = now.strftime("%m/%d/%Y, %H:%M:%S")
        db.insert({"username": str(user_id), "reason": str(reason), "warner": str(warner), "time": nowstrft})

    def getWarnings(self, server_name, user_id):
        Query = tinydb.Query()
        self.DBCheck(server_name)
        db = tinydb.TinyDB("./database/" + server_name + "/warnings.json")
        warnings = str(db.search(Query.username == str(user_id)))
        numWarnings = len(warnings)
        return numWarnings, warnings

    def clearwarns(self, server_name, user_id, num):
        self.DBCheck(server_name)
        db = tinydb.TinyDB("./database/" + server_name + "/warnings.json")
        Query = tinydb.Query()
        i = 0
        if num is None or num == "all":
            db.remove(Query.username == str(user_id))
        else:
            instances = db.search(Query.username == str(user_id))
            while i < int(num):
                i +=1
                lastwarn = instances.pop()
                print(lastwarn)
                time_lastwarned = lastwarn.get("time")
                db.remove(Query.username == user_id and Query.time == time_lastwarned)
