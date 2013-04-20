# -*- coding: utf-8 -*-

from django.utils import unittest
from django.test.client import Client
import json
import archive.database as db
from operator import attrgetter
from archive.models import UserModel, TablatureModel, CommentModel

class TestUser(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
                
        #Make sure that tables exist for each test
        db.create_users_table("debug.db")
        db.create_tablatures_table("debug.db")
        db.create_comments_table("debug.db")

    def test_put_add_user(self):
        '''
        Try to add user.
        '''
     
        data = '{"user_nickname":"jonne", "email":"jolli@live.fi", "picture":"es-purkki.png", "description":"opettajien kauhu"}'
        response = self.client.put('/tab_archive/users/jonne', data = data , content_type = 'application/json')

        self.assertEqual(response.status_code, 204)
        
    def test_get(self):
        '''
        Try to get user with no authorization.
        '''
        
        data = '{"user_nickname":"jonne", "email":"jolli@live.fi", "picture":"es-purkki.png", "description":"opettajien kauhu"}'
        response = self.client.put('/tab_archive/users/jonne', data = data , content_type = 'application/json')
        
        self.assertEqual(response.status_code, 204)
        
        response = self.client.get('/tab_archive/users/jonne', {"Accept":"application/json"})
        self.assertEqual(response.status_code, 200)
        
        content = json.loads(response.content)
        
        
        self.assertEqual(content["user"]['picture'], "es-purkki.png")
        self.assertEqual(content["user"]['description'], "opettajien kauhu")
        self.assertFalse(content.has_key('email'))

    def test_get_authorized(self):
        '''
        Try to get user with authorization.
        '''
        
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
        
        
        data = '{"user_nickname":"jonne", "email":"jolli@live.fi", "picture":"es-purkki.png", "description":"opettajien kauhu"}'
        response = self.client.put('/tab_archive/users/jonne', data = data , content_type = 'application/json')
        
        self.assertEqual(response.status_code, 204)
        
        
        # Issue a GET request.
        response = self.client.get('/tab_archive/users/jonne', {"Accept":"application/json"}, **extra)
        self.assertEqual(response.status_code, 200)
     
        content = json.loads(response.content)
        
        self.assertEqual(content["user"]['picture'], "es-purkki.png")
        self.assertEqual(content["user"]['description'], "opettajien kauhu")
        self.assertEqual(content["user"]['email'], "jolli@live.fi")
        
    def test_get_fail(self):
        '''
        Try to get user that does not exit.
        '''
        response = self.client.get('/tab_archive/users/puuhapete', content_type = "application/json")
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        response = self.client.post('/tab_archive/users/olli', {"Accept":"application/json", "Authorization":"erkki"}, content_type = "application/json")
     
        content = json.loads(response.content)
        
        self.assertEqual(response.status_code, 405)       
        
    def test_delete_unauthorized(self):
        '''
        Try to delete user without authorization.
        '''
        
        data = '{"user_nickname":"jonne", "email":"jolli@live.fi", "picture":"es-purkki.png", "description":"opettajien kauhu"}'
        response = self.client.put('/tab_archive/users/jonne', data = data , content_type = 'application/json')
        
        response = self.client.delete('/tab_archive/users/jonne', {"Accept":"application/json"}, content_type = "application/json")
        
        self.assertEqual(response.status_code, 401)
        
        
    def test_delete_authorized(self):
        '''
        Delete user.
        '''
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        data = '{"user_nickname":"erkki", "email":"erkki@pertti.fi", "picture":"kissakuva.png", "description":"maan viljeljia"}'
        response = self.client.put('/tab_archive/users/erkki', data = data , content_type = 'application/json')
        
        
        response = self.client.delete('/tab_archive/users/erkki', {"Accept":"application/json"}, content_type = "application/json", **extra)
        
        self.assertEqual(response.status_code, 204)
        
    def tearDown(self):
        #Make sure that no data is retained between tests
        db.drop_tables()
        
        
class TestUsers(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        
        #Make sure that tables exist for each test
        db.create_users_table("debug.db")
        db.create_tablatures_table("debug.db")
        db.create_comments_table("debug.db")
        
    def test_get(self):
        data = '{"user_nickname":"jonne", "email":"jolli@live.fi", "picture":"es-purkki.png", "description":"opettajien kauhu"}'
        response = self.client.put('/tab_archive/users/jonne', data = data , content_type = 'application/json')
    
        response = self.client.get('/tab_archive/users', {"Accept":"application/json"}, content_type = "application/json")
        
        content = json.loads(response.content)
        
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content[0]["user_nickname"], "jonne")
        self.assertEqual(len(content), 1)
        
    def test_post(self):
        response = self.client.post('/tab_archive/users', {"Accept":"application/json"}, content_type = "application/json")
        self.assertEqual(response.status_code, 405)
        
    def tearDown(self):
        #Make sure that no data is retained between tests
        db.drop_tables()
        

class TestArtist(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        
        #Make sure that tables exist for each test
        db.create_users_table("debug.db")
        db.create_tablatures_table("debug.db")
        db.create_comments_table("debug.db")
        
    def test_get(self):
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
    
        data = '{"user_nickname":"jonne", "email":"jolli@live.fi", "picture":"es-purkki.png", "description":"opettajien kauhu"}'
        response = self.client.put('/tab_archive/users/jonne', data = data , content_type = 'application/json')
    
        data = '{"body":"10110101", "artist_id":"paula koivuniemi", "song_id":"kuka pelkaa paulaa", "user_nickname":"jonne"}'
        response = self.client.post('/tab_archive/artists/paula koivuniemi/kuka pelkaa paulaa', data = data , content_type = 'application/json', **extra)
    
        #Here we try to get artist
        response = self.client.get('/tab_archive/artists/paula koivuniemi', {"Accept":"application/json"}, content_type = "application/json")
        
        content = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content["songs"][0]["song_id"], "kuka pelkaa paulaa")
        
    def tearDown(self):
        #Make sure that no data is retained between tests
        db.drop_tables()
        
    
class TestSong(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        
        #Make sure that tables exist for each test
        db.create_users_table("debug.db")
        db.create_tablatures_table("debug.db")
        db.create_comments_table("debug.db")
    
    def test_post(self):
        '''
        Try to add a tablature.
        '''
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
        
        data = '{"user_nickname":"jonne", "email":"jolli@live.fi", "picture":"es-purkki.png", "description":"opettajien kauhu"}'
        response = self.client.put('/tab_archive/users/jonne', data = data , content_type = 'application/json')
    
        data = '{"body":"10110101",  "song_id":"kuka pelkaa paulaa", "user_nickname":"jonne"}'
        
        #Here we try to post tablature
        response = self.client.post('/tab_archive/artists/paula koivuniemi/kuka pelkaa paulaa', data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 201)
        
        location = response["Location"]
                
        self.assertEqual(location, '/tab_archive/paula_koivuniemi/kuka_pelkaa_paulaa/1')
        
    def test_get(self):
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
    
        data = '{"user_nickname":"jonne", "email":"jolli@live.fi", "picture":"es-purkki.png", "description":"opettajien kauhu"}'
        response = self.client.put('/tab_archive/users/jonne', data = data , content_type = 'application/json')
    
        data = '{"body":"10110101", "artist_id":"paula koivuniemi", "song_id":"kuka pelkaa paulaa", "user_nickname":"jonne"}'
        response = self.client.post('/tab_archive/artists/paula koivuniemi/kuka pelkaa paulaa', data = data , content_type = 'application/json', **extra)
        location = response["Location"]
    
        #Here we try to get tablatures to song
        response = self.client.get('/tab_archive/paula koivuniemi/kuka pelkaa paulaa', {"Accept":"application/json"}, content_type = "application/json")
        
        content = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content["tablatures"]), 1)
        self.assertEqual(content["artist_id"], "paula koivuniemi")
        self.assertEqual(content["song_id"], "kuka pelkaa paulaa")
        self.assertEqual(content["tablatures"][0]["tablature"], "10110101")
        
    def tearDown(self):
        #Make sure that no data is retained between tests
        db.drop_tables()
        

class TestArtists(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        
        #Make sure that tables exist for each test
        db.create_users_table("debug.db")
        db.create_tablatures_table("debug.db")
        db.create_comments_table("debug.db")
        
    def test_get(self):
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
    
        data = '{"user_nickname":"jonne", "email":"jolli@live.fi", "picture":"es-purkki.png", "description":"opettajien kauhu"}'
        response = self.client.put('/tab_archive/users/jonne', data = data , content_type = 'application/json')
    
        data = '{"body":"10110101", "artist_id":"paula koivuniemi", "song_id":"kuka pelkaa paulaa", "user_nickname":"jonne"}'
        response = self.client.post('/tab_archive/artists/paula koivuniemi/kuka pelkaa paulaa', data = data , content_type = 'application/json', **extra)
        location = response["Location"]
        
        #Here we try to get list of artists
        response = self.client.get('/tab_archive/artists', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        
        content = json.loads(response.content)        
        
        self.assertEqual(content[0]['artist_id'], "paula koivuniemi")
        self.assertEqual(len(content), 1)
        
    def tearDown(self):
        #Make sure that no data is retained between tests
        db.drop_tables()
        
        
class TestDatabaseInterface(unittest.TestCase):

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
        
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user) 

        user = self.handle.get_user("oula")
        
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
        self.assertTrue(self.handle.contains_user("erkki"))
        name = self.handle.delete_user("erkki")
        
        self.assertEqual(name, "erkki")
        self.assertFalse(self.handle.contains_user("erkki"))
        
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
        
    def test_add_tablature_fail(self):
        '''
        Try to add tablature by user that does not exist.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
    
        tab = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"jorkki", "rating_count":0})
        tab_id = self.handle.add_tablature(tab)
        
        self.assertIsNone(tab_id)

        
    def test_get_songs_by_artist(self):
        '''
        Try to get songs by artist.
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
        
        songs = self.handle.get_songs("tuttiritari")
        songs.sort()
        
        expected = [["tuttiritari", "tutti viimeinen"],["tuttiritari", "toinen tutti"]]
        expected.sort()

        self.assertEqual(expected,songs)

        songs = self.handle.get_songs("")
        songs.sort()

        expected = [["tuttiritari", "tutti viimeinen"], ["tuttiritari", "toinen tutti"], ["paula koivuniemi", "kuka pelkaa paulaa"]]
        expected.sort()

        self.assertEqual(expected,songs)

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
        
        

        songs = self.handle.get_songs("")
        songs.sort()

        expected = [["tuttiritari", "tutti viimeinen"], ["tuttiritari", "toinen tutti"], ["paula koivuniemi", "kuka pelkaa paulaa"]]
        expected.sort()

        self.assertEqual(expected,songs)
    
    def test_get_songs_fail(self):
        '''
        Try to get songs whene there is none.
        '''
        songs = self.handle.get_songs("paula koivuniemi")
        self.assertIsNone(songs)

    def test_get_artists(self):
        '''
        Try to get artists.        
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
        
        artists = self.handle.get_artists()
        artists.sort()
    
        expected = ["tuttiritari","paula koivuniemi"]
        expected.sort()

        self.assertEqual(artists, expected)

    def test_get_artists_fail(self):
        '''
        Try to get artists when now tablatures has been added.
        '''
        artists = self.handle.get_artists()
        self.assertIsNone(artists)
        
    def test_get_tablatures_all(self):
        '''
        Try to get list of all tablatures.
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
        
        tablatures = self.handle.get_tablatures('','')

        self.assertTrue(isinstance(tablatures[0], TablatureModel))
        self.assertEqual(tablatures[0].tablature_id, tab_id1)
        self.assertEqual(tablatures[0].body, tab1.body)
        self.assertEqual(tablatures[0].rating, tab1.rating)
        self.assertEqual(tablatures[0].artist_id, tab1.artist_id)
        self.assertEqual(tablatures[0].song_id, tab1.song_id)
        self.assertEqual(tablatures[0].user_nickname, tab1.user_nickname)
        self.assertEqual(tablatures[0].rating_count, tab1.rating_count)
        self.assertEqual(len(tablatures), 4)
        
        
        
    def test_get_tablatures_by_artist(self):
        '''
        Try to get list of tablatures by artist.
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
        
        tablatures = self.handle.get_tablatures('paula koivuniemi','')

        self.assertTrue(isinstance(tablatures[0], TablatureModel))
        self.assertEqual(tablatures[0].tablature_id, tab_id2)
        self.assertEqual(tablatures[0].body, tab2.body)
        self.assertEqual(tablatures[0].rating, tab2.rating)
        self.assertEqual(tablatures[0].artist_id, tab2.artist_id)
        self.assertEqual(tablatures[0].song_id, tab2.song_id)
        self.assertEqual(tablatures[0].user_nickname, tab2.user_nickname)
        self.assertEqual(tablatures[0].rating_count, tab2.rating_count)
        self.assertEqual(len(tablatures), 1)
        
    def test_get_tablatures_by_song(self):
        '''
        Try to get list of tablatures by song.
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
        
        tablatures = self.handle.get_tablatures('','kuka pelkaa paulaa')

        self.assertTrue(isinstance(tablatures[0], TablatureModel))
        self.assertEqual(tablatures[0].tablature_id, tab_id2)
        self.assertEqual(tablatures[0].body, tab2.body)
        self.assertEqual(tablatures[0].rating, tab2.rating)
        self.assertEqual(tablatures[0].artist_id, tab2.artist_id)
        self.assertEqual(tablatures[0].song_id, tab2.song_id)
        self.assertEqual(tablatures[0].user_nickname, tab2.user_nickname)
        self.assertEqual(tablatures[0].rating_count, tab2.rating_count)
        self.assertEqual(len(tablatures), 1)
        
    def test_get_tablatures_fail(self):
        '''
        Try to get list of tablatures when there is none.
        '''
        
        tablatures = self.handle.get_tablatures('', '')
        self.assertIsNone(tablatures)
        
    def test_get_tablature(self):
        '''
        Try to get tablature by id.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
    
        tab = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        tab_id = self.handle.add_tablature(tab)
        
        got = self.handle.get_tablature(tab_id)
        self.assertTrue(isinstance(got, TablatureModel))
        self.assertEqual(got.tablature_id, 1)
        self.assertEqual(got.body, tab.body)
        self.assertEqual(got.rating, tab.rating)
        self.assertEqual(got.artist_id, tab.artist_id)
        self.assertEqual(got.song_id, tab.song_id)
        self.assertEqual(got.user_nickname, tab.user_nickname)
        self.assertEqual(got.rating_count, tab.rating_count)
        
    def test_get_tablature_fail(self):
        '''
        Try to get tablature that does not exist
        '''
        tab = self.handle.get_tablature(10)
        self.assertIsNone(tab)
        
    def test_edit_tablature(self):
        '''
        Try to edit tablature.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
    
        tab = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        tab_id = self.handle.add_tablature(tab)
        
        edit = TablatureModel.create({'tablature_id':tab_id, 'body':"1111111", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        
        edit_id = self.handle.edit_tablature(edit)
        edited = self.handle.get_tablature(edit_id)
        
        self.assertEqual(edit_id, tab_id)
        self.assertEqual(edited.body, edit.body)
        
    def test_edit_tablature_fail(self):
        '''
        Try to edit tablature that does not exist.
        '''
        edit = TablatureModel.create({'tablature_id':1, 'body':"1111111", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        edit_id = self.handle.edit_tablature(edit)

        self.assertIsNone(edit_id)
        
    def test_delete_tablature(self):
        '''
        Try to delete tablature.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
    
        tab = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        tab_id = self.handle.add_tablature(tab)
        
        delete_id = self.handle.delete_tablature(tab_id)
        self.assertEqual(tab_id, delete_id)
        
        deleted = self.handle.get_tablature(tab_id)
        self.assertIsNone(deleted)
        
    def test_delete_tablature_fail(self):
        '''
        Try to delete tablature that doesn't exist.
        '''
        deleted_id = self.handle.delete_tablature(3)
        self.assertIsNone(deleted_id)
        
    def test_get_rating(self):
        '''
        Try to get rating.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
    
        tab = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        tab_id = self.handle.add_tablature(tab)
            
        rating = self.handle.get_rating(tab_id)
        self.assertEqual(rating, (0,0))
    
    def test_get_rating_fail(self):
        '''
        Try to get rating that doesn't exist.
        '''
        rating = self.handle.get_rating(1)
        self.assertIsNone(rating)
        
    def test_add_rating(self):
        '''
        Try to add rating.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
    
        tab = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        tab_id = self.handle.add_tablature(tab)
        
        rating = self.handle.add_rating(tab_id, 5)
        self.assertEqual(rating, (5,1))
        rating = self.handle.add_rating(tab_id, 5)
        self.assertEqual(rating, (10,2))
        
    def test_add_rating_fail(self):
        '''
        Try to add rating to a tablature that does not exist.
        '''
        rating = self.handle.add_rating(1, 5)
        self.assertIsNone(rating)
        
    def test_contains_tablature(self):
        '''
        Try if table contains tablature.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
    
        tab = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        tab_id = self.handle.add_tablature(tab)
        
        contains = self.handle.contains_tablature(tab_id)
        self.assertTrue(contains)
        
    def test_contains_tablature_fail(self):
        '''
        Table doesn't contain tablature.
        '''
        contains = self.handle.contains_tablature(1)
        self.assertFalse(contains)
        
    def test_add_comment(self):
        '''
        Try to add comment.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
        
        tab = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        tab_id = self.handle.add_tablature(tab)
        
        comment = CommentModel.create({"comment_id":None, "reply_to":None, "user_nickname":"erkki", "tablature_id":tab_id, "body":"ihan huono, ei jatkoon"})
        comment_id = self.handle.add_comment(comment)
        
        self.assertEqual(comment_id, 1)
        
    def test_add_comment_fail(self):
        '''
        Try to add comment without existing user or tablature.
        '''
        comment = CommentModel.create({"comment_id":None, "reply_to":None, "user_nickname":"erkki", "tablature_id":1, "body":"ihan huono, ei jatkoon"})
        comment_id = self.handle.add_comment(comment)
                
        self.assertIsNone(comment_id)
        
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
        
        comment_id = self.handle.add_comment(comment)
        self.assertIsNone(comment_id)
        
    def test_get_comment(self):
        '''
        Try to get comment.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
        
        tab = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        tab_id = self.handle.add_tablature(tab)
        
        comment = CommentModel.create({"comment_id":None, "reply_to":None, "user_nickname":"erkki", "tablature_id":tab_id, "body":"ihan huono, ei jatkoon"})
        comment_id = self.handle.add_comment(comment)
        
        got = self.handle.get_comment(comment_id)

        self.assertTrue(isinstance(got, CommentModel))
        self.assertEqual(comment_id, got.comment_id)
        self.assertEqual(comment.user_nickname, got.user_nickname)
        self.assertEqual(comment.body, got.body)
    
    def test_get_comment_fail(self):
        '''
        Try to get comment that does not exist.
        '''
        
        got = self.handle.get_comment(1)
        
        self.assertIsNone(got)
        
    def test_modify_comment(self):
        '''
        Try to modify comment.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
        
        tab = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        tab_id = self.handle.add_tablature(tab)
        
        comment = CommentModel.create({"comment_id":None, "reply_to":None, "user_nickname":"erkki", "tablature_id":tab_id, "body":"ihan huono, ei jatkoon"})
        comment_id = self.handle.add_comment(comment)
        
        modify = CommentModel.create({"comment_id":comment_id, "reply_to":None, "tablature_id":tab_id, "user_nickname":"erkki", "body":"aivan super, mahtavaa"})
        modified_id = self.handle.modify_comment(modify)
        modified = self.handle.get_comment(modified_id)
        
        self.assertEqual(modified_id, comment_id)
        self.assertEqual(modified.body, modify.body)
        self.assertEqual(modified.user_nickname, comment.user_nickname)
    
    def test_modify_comment_fail(self):
        '''
        Try to modify comment that does not exist.
        '''
        modify = CommentModel.create({"comment_id":1, "reply_to":None, "user_nickname":"erkki", "tablature_id":1, "body":"aivan super, mahtavaa"})
        modified_id = self.handle.modify_comment(modify)
        self.assertIsNone(modified_id)
        
    def test_append_answer(self):
        '''
        Try to add reply to comment.
        '''
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
        
        tab = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        tab_id = self.handle.add_tablature(tab)
        
        comment = CommentModel.create({"comment_id":None, "reply_to":None, "user_nickname":"erkki", "tablature_id":tab_id, "body":"ihan huono, ei jatkoon"})
        comment_id = self.handle.add_comment(comment)
        
        response = CommentModel.create({"comment_id":None, "reply_to":comment_id, "user_nickname":"erkki", "tablature_id":tab_id, "body":"paraspas"})
        response_id = self.handle.append_answer(response)
            
        self.assertEqual(response_id, 2)
    
    def test_append_answer(self):
        '''
        Try to add reply to comment that doesn't exist.
        '''
    
        response = CommentModel.create({"comment_id":None, "reply_to":1, "user_nickname":"erkki", "tablature_id":1, "body":"paraspas"})
        response_id = self.handle.append_answer(response)
        self.assertIsNone(response_id)
    
    def test_contains_comment(self):
        '''
        Try if table contains comment with id.
        '''
        
        
        user = UserModel.create({"user_nickname":"erkki", "email":"erkki@ekspertti.info", "description":"", "picture":"lahna.png"})
        self.handle.add_user(user)
        
        tab = TablatureModel.create({'tablature_id':"Null", 'body':"1010010", "rating":0, "artist_id":"tuttiritari", "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        tab_id = self.handle.add_tablature(tab)
        
        comment = CommentModel.create({"comment_id":None, "reply_to":None, "user_nickname":"erkki", "tablature_id":tab_id, "body":"ihan huono, ei jatkoon"})
        comment_id = self.handle.add_comment(comment)
        
        contains = self.handle.contains_comment(comment_id)
        
        assertTrue(contains)
        
    def test_contains_comment(self):
        contains = self.handle.contains_comment(1)
        
        self.assertFalse(contains)
    
    def tearDown(self):
        db.drop_tables()