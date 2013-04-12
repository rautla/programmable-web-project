# Fix problem with assertEqual
#import random
import archive.database as db
import unittest

from archive.models import UserModel, TablatureModel, CommentModel

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        '''
        Makes sure that tables exist.
        '''
        self.handle = db.get_database("debug.db")
        db.create_users_table("debug.db")
        db.create_tablatures_table("debug.db")
        db.create_comments_table("debug.db")

    def test_add_user(self):
        '''
        Try to create user.
        '''
        user = UserModel.create({"user_nickname":"erkki" , "email":"erkki@sposti.org", "description":"Hodor", "picture":"hodor.png"})
        name = self.handle.add_user(user)
        self.assertEqual(name, "erkki")
        
        self.assertRaises(AssertionError)
        #AssertionError: None != 'erkki'
        
    def test_add_user_fail(self):
        '''
        Try to create user with nickname that already exists.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
       
            
        
if __name__ == '__main__':
    unittest.main()
    