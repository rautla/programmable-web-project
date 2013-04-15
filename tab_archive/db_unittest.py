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
        user1 = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user1)
        user2 = UserModel.create({"user_nickname":"erkki" , "email":"erkki@sposti.org", "description":"Hodor", "picture":"hodor.png"})
        name = self.handle.add_user(user2)
        
        self.assertEqual(name, None)
        
    def test_get_user(self):
        '''
        Try to get user.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
    
        ret_val = self.handle.get_user("erkki")
        
        self.assertTrue(isinstance(ret_val, UserModel))
        
        self.assertEqual(ret_val.name, erkki)
        
    def test_get_user_fail(self):
        '''
        Try to get user that does not exist.
        '''
        user = self.handle.get_user("erkki")
        
        self.assertEqual(user, None)        
        
    def test_edit_user(self):
        '''
        Try to edit user.
        '''
        
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        name = self.handle.add_user(user)
        
        user_changes = UserModel.create({"user_nickname":"erkki", "email":"jorma@ekspertti.info", "description":"heeno mees", "picture":"tukiainen.png"})
        name = self.handle.edit_user(user_changes)
        
        self.assertEqual(name, "erkki")
        
        changed_user = self.handle.get_user("erkki")
        self.assertEqual(changed_user.email, "jorma@ekspertti.info")
        self.assertEqual(changed_user.description, "heeno mees")
        self.assertEqual(changed_user.picture, "tukiainen.png")
        
    def test_edit_user_fail‎(self):
        '''
        Try to edit user that does not exist.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        
        name = self.handle.edit_user(user)
        
        self.assertEqual(name, None)
        
    def test_delete_user(self):
        '''
        Try to delete user.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
        name = self.handle.delete_user()
        
        self.assertEqual(name, None)
        
    def test_delete_user_fail(self):
        '''
        Try to delete user that does not exist.
        '''
        
        name = self.handle.delete_user()
        
        self.assertEqual(name, None)
        
    def test_get_users(self):
        '''
        Try to get all users.
        '''
        
        user1 = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user1)
        user2 = UserModel.create({"user_nickname":"jorkki" , "email":"erkki@sposti.org", "description":"Hodor", "picture":"hodor.png"})
        name = self.handle.add_user(user2)
        
        users = self.handle.get_users()
        
        self.assertEqual(type(name), type([]))
        
        self.assertEqual(user1, users[0])
        self.assertEqual(user2, users[1])
    
    def tearDown(self):
        db.drop_tables()
        
        
if __name__ == '__main__':
    
    unittest.main()
    