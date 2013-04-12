# Fix problem with assertEqual
#import random
import database as db
import unittest

from archive.models import UserModel, TablatureModel, CommentModel

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        '''
        Makes sure that tables exist.
        '''
        db.create_users_table()
        db.create_tablatures_table()
        db.create_comments_table()

    def test_add_user(self):
        '''
        Try to create user.
        '''
        user = UserModel.create({"user_nickname":"erkki" , "email":"erkki@sposti.org", "description":"Hodor", "picture":"hodor.png"})
        name = db.database.add_user(user)
        self.assertEqual(name, "erkki")
        
    def test_add_user_fail(self):
        '''
        Try to create user with nickname that already exists.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
       
            
        
if __name__ == '__main__':
    unittest.main()
    