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
        db.insert({"username": user_id, "reason": reason, "warner": warner, "time": now.strftime("%m/%d/%Y, %H:%M:%S")})

    def getWarnings(self, server_name, user_id):
        Query = tinydb.Query()
        self.DBCheck(server_name)
        db = tinydb.TinyDB("./database/" + server_name + "/warnings.json")
        warnings = str(db.search(Query.username == user_id))
        numWarnings = len(warnings)
        return numWarnings, warnings

    def clearwarns(self, server_name, user_id):
        self.DBCheck(server_name)
        db = tinydb.TinyDB("./database/" + server_name + "/warnings.json")
        Query = tinydb.Query()
        db.remove(Query.username == user_id)
