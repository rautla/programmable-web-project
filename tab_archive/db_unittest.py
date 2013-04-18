# Fix problem with assertEqual
#import random
import archive.database as db
from operator import attrgetter
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
        
        self.assertIsNone(name)
        
    def test_get_user(self):
        '''
        Try to get user.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
    
        ret_val = self.handle.get_user("erkki")
        
        self.assertTrue(isinstance(ret_val, UserModel))
        
        self.assertEqual(ret_val.user_nickname, "erkki")
        
    def test_get_user_fail(self):
        '''
        Try to get user that does not exist.
        '''
        user = self.handle.get_user("erkki")
        
        self.assertIsNone(user)        
        
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
        
    def test_edit_user_fail(self):
        '''
        Try to edit user that does not exist.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        
        name = self.handle.edit_user(user)
        
        self.assertIsNone(name)
        
    def test_delete_user(self):
        '''
        Try to delete user.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
        name = self.handle.delete_user("erkki")
        
        self.assertEqual(name, "erkki")
        
    def test_delete_user_fail(self):
        '''
        Try to delete user that does not exist.
        '''
        
        name = self.handle.delete_user("erkki")
        
        self.assertIsNone(name)
        
    def test_get_users(self):
        '''
        Try to get all users.
        '''
        
        user1 = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user1)
        user2 = UserModel.create({"user_nickname":"jorkki" , "email":"erkki@sposti.org", "description":"Hodor", "picture":"hodor.png"})
        name = self.handle.add_user(user2)
        
        userlist = [user1, user2]
        userlist.sort(key=attrgetter("user_nickname"))
        
        users = self.handle.get_users()
        users.sort(key=attrgetter("user_nickname"))
        
        self.assertEqual(type(users), type([]))
        
        self.assertEqual(userlist[0].user_nickname, users[0].user_nickname)
        self.assertEqual(userlist[1].user_nickname, users[1].user_nickname)
        
    def test_get_users_fail(self):
        '''
        Try to get empty userlist.
        '''        
        
        ret_val = self.handle.get_users()
        self.assertIsNone(ret_val)
        
    def test_add_tablature(self):
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
    
        tab = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        tab_id = self.handle.add_tablature(tab)
        
        self.assertEqual(tab_id, 1)
        
    def test_get_songs(self):
        '''
        Try to get songs.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
        
        tab1 = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        tab_id1 = self.handle.add_tablature(tab1)
        
        tab2 = TablatureModel.create({'tablature_id':"Null", 'body':"1011111", "rating":0, "artist_id":"paula koivuniemi", "song_id":"kuka pelkaa paulaa", "user_nickname":"erkki", "rating_count":0})
        tab_id2 = self.handle.add_tablature(tab2)
        
        tab3 = TablatureModel.create({'tablature_id':"Null", 'body':"1010011", "rating":0, "artist_id":"tuttiritari", "song_id":"toinen tutti", "user_nickname":"erkki", "rating_count":0})
        tab_id3 = self.handle.add_tablature(tab3)
        
        tab4 = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        tab_id4 = self.handle.add_tablature(tab4)
        
        songs =self.handle.get_songs("tuttiritari");
        print songs
    
    def tearDown(self):
        db.drop_tables()
        
        
if __name__ == '__main__':
    
    unittest.main()
    