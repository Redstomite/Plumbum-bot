import unittest
from database_queries import dbquery
import tinydb


class testDB(unittest.TestCase):
    def test_warn(self):
        server_name = "testey"
        user = ["fffffffffffffffffffffffffffffffffffffffffffffffffffff"]
        reason = "multi-line reason"
        h = dbquery()
        h.warnUser(server_name, user, reason)

        db = tinydb.TinyDB("./db/" + server_name + "/warnings.json")
        Query = tinydb.Query()
        warnings = db.search(Query.username == user)
        numWarnings = len(warnings)
        self.assertEqual(numWarnings, 1, "should be 1")
        #passed
if __name__ == '__main__':
    unittest.main()
