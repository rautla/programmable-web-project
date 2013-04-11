#import random
import database as db
import unittest

from archive.models import UserModel, TablatureModel, CommentModel

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        db.create_users_table()
        db.create_tablatures_table()
        db.create_comments_table()

    def test_add_user(self):
        user_info = {}
        db.database.add_user()
            
        
if __name__ == '__main__':
    unittest.main()
    