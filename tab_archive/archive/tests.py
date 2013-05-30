# -*- coding: utf-8 -*-

from django.utils import unittest
from django.test.client import Client
import json
import archive.database as db
from operator import attrgetter
from archive.models import UserModel, TablatureModel, CommentModel


def precond_user(client):
    '''
    Add user to database.
    '''

    data = '{"user_nickname":"jonne", "email":"jolli@live.fi", "picture":"es-purkki.png", "description":"opettajien kauhu"}'
    response = client.put('/tab_archive/users/jonne', data = data , content_type = 'application/json')

    return response
        
def precond_user2(client):
    '''
    Add user to database.
    '''
    data = '{"user_nickname":"erkki", "email":"erkki@pertti.fi", "picture":"kissakuva.png", "description":"maan viljeljia"}'
    response = client.put('/tab_archive/users/erkki', data = data , content_type = 'application/json')
    
    return response
    
def precond_user_tablature(client):
    '''
    Add user and tablature to database.
    '''
    extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }

    precond_user(client)
    
    data = '{"body":"10110101", "user_nickname":"jonne"}'
    response = client.post('/tab_archive/artists/paula koivuniemi/kuka pelkaa paulaa', data = data , content_type = 'application/json', **extra)
    
    return response
    
def precond_user_tablature2(client):
    '''
    Add user and 3 tablatures.
    '''
    precond_user_tablature(client)
    
    extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
    
    
    data = '{"body":"10110101", "user_nickname":"jonne"}'
    response = client.post('/tab_archive/artists/paula koivuniemi/kuuntelen tomppaa', data = data , content_type = 'application/json', **extra)
    
    data = '{"body":"10110101", "user_nickname":"jonne"}'
    response = client.post('/tab_archive/artists/Metallica/kuuntelen tomppaa', data = data , content_type = 'application/json', **extra)
    
    return response
    
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
     
        #Here we try to put user
        response = precond_user(self.client)

        self.assertEqual(response.status_code, 204)
        
    def test_put_add_user_fail(self):
        '''
        Try to add user with invalid data.
        Try to add user that already exists.
        '''
        
        data = '{"herpderp"}'
        response = self.client.put('/tab_archive/users/jonne', data = data , content_type = 'application/json')
        
        self.assertEqual(response.status_code, 400)
        
        response = precond_user(self.client)
        
        data = '{"user_nickname":"jonne", "email":"molli@live.fi", "picture":"redbull-tolkki.png", "description":"opettajien mielikki"}'
        response = self.client.put('/tab_archive/users/jonne', data = data , content_type = 'application/json')
        
        self.assertEqual(response.status_code, 409)
        
    def test_put_modify_user(self):
        '''
        Modify existing user.
        '''
        response = precond_user(self.client)
        
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
        
        data = '{"user_nickname":"jonne", "email":"molli@live.fi", "picture":"redbull-tolkki.png", "description":"opettajien mielikki"}'
        response = self.client.put('/tab_archive/users/jonne', data = data , content_type = 'application/json', **extra)
        
        self.assertEqual(response.status_code, 204)
        
    def test_get(self):
        '''
        Try to get user with no authorization.
        '''
        
        response = precond_user(self.client)
        
        response = self.client.get('/tab_archive/users/jonne', {"Accept":"application/json"})
        #expected = {'users':'{'href': 'http://testserver/tab_archive/users', 'rel': 'self'}', 'comments':'http://testserver/tab_archive/users/jonne/comments', 'tablatures':'http://testserver/tab_archive/users/jonne/tablatures', user:{"user_nickname":"jonne", "email":"jolli@live.fi", "picture":"es-purkki.png", "description":"opettajien kauhu"}}
        self.assertEqual(response.status_code, 200)
        
        content = json.loads(response.content)
        expected = {u'tablatures': {u'href': u'http://testserver/tab_archive/users/jonne/tablatures', 
        u'rel': u'self'}, 
        u'user': {u'picture': u'es-purkki.png', 
        u'description': u'opettajien kauhu', u'user_nickname': u'jonne'}, 
        u'comments': {u'href': u'http://testserver/tab_archive/users/jonne/comments', u'rel': u'self'}, 
        u'users': {u'href': u'http://testserver/tab_archive/users', u'rel': u'self'}}
        
        self.assertEqual(content, expected)

    def test_get_authorized(self):
        '''
        Try to get user with authorization.
        '''
        
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
        
        
        response = precond_user(self.client)
        
        self.assertEqual(response.status_code, 204)
        
        
        # Issue a GET request.
        response = self.client.get('/tab_archive/users/jonne', {"Accept":"application/json"}, **extra)
        self.assertEqual(response.status_code, 200)
     
        content = json.loads(response.content)
        
        expected = {u'tablatures': {u'href': u'http://testserver/tab_archive/users/jonne/tablatures', 
        u'rel': u'self'}, 
        u'user': {u'picture': u'es-purkki.png', u'email': u'jolli@live.fi', 
        u'description': u'opettajien kauhu', u'user_nickname': u'jonne'}, 
        u'comments': {u'href': u'http://testserver/tab_archive/users/jonne/comments', u'rel': u'self'}, 
        u'users': {u'href': u'http://testserver/tab_archive/users', u'rel': u'self'}}
        self.assertEqual(expected, content)
        
    def test_get_fail(self):
        '''
        Try to get user that does not exit.
        '''
        response = self.client.get('/tab_archive/users/puuhapete', content_type = "application/json")
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        '''
        Post is not allowed because it is not implemented.
        '''
        response = self.client.post('/tab_archive/users/olli', {"Accept":"application/json", "Authorization":"erkki"}, content_type = "application/json")
     
        content = json.loads(response.content)
        
        self.assertEqual(response.status_code, 405)       
        
    def test_delete_unauthorized(self):
        '''
        Try to delete user without authorization.
        '''
        
        response = precond_user(self.client)
        
        response = self.client.delete('/tab_archive/users/jonne', {"Accept":"application/json"}, content_type = "application/json")
        self.assertEqual(response.status_code, 401)
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        
        response = self.client.delete('/tab_archive/users/jonne', {"Accept":"application/json"}, content_type = "application/json", **extra)
      
        self.assertEqual(response.status_code, 401)
        
        
    def test_delete_authorized(self):
        '''
        Delete user.
        '''
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        response = precond_user2(self.client)    
        
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
        '''
        Get list of users.
        '''
        response = precond_user(self.client)
        response = precond_user2(self.client)
        #Here we try to get users
        response = self.client.get('/tab_archive/users', {"Accept":"application/json"}, content_type = "application/json")
        
        expected = [
        {u'link': {u'href': u'http://testserver/tab_archive/users/jonne', u'rel': u'self'}, 
        u'user_nickname': u'jonne'}, 
        {u'link': {u'href': u'http://testserver/tab_archive/users/erkki', u'rel': u'self'}, 
        u'user_nickname': u'erkki'}]
        
        content = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, expected)        
        
    def test_post(self):
        '''
        Post is not allowed because it is not implemented.
        '''
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
        '''
        Try to get songs by artist.
        '''
        response = precond_user_tablature2(self.client)
    
        #Here we try to get artist
        response = self.client.get('/tab_archive/artists/paula koivuniemi', {"Accept":"application/json"}, content_type = "application/json")
        
        
        self.assertEqual(response.status_code, 200)
        
        content = json.loads(response.content)
        expected = [{u'song_id': u'kuka pelkaa paulaa', u'link': 
        {u'href': u'http://testserver/tab_archive/artists/paula%20koivuniemi/kuka%20pelkaa%20paulaa', u'rel': u'self'}}, 
        {u'song_id': u'kuuntelen tomppaa', u'link': 
        {u'href': u'http://testserver/tab_archive/artists/paula%20koivuniemi/kuuntelen%20tomppaa', u'rel': u'self'}}
        ]
        
        
        self.assertEqual(content, expected)
        
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
        
        response = precond_user(self.client)
    
        data = '{"body":"10110101", "user_nickname":"jonne"}'
        
        #Here we try to post tablature
        response = self.client.post('/tab_archive/artists/paula koivuniemi/kuka pelkaa paulaa', data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 201)
        
        location = response["Location"]
                
        self.assertEqual(location, 'http://testserver/tab_archive/tablatures/1')
        
    def test_post_fail(self):
        '''
        Try to add tablature without authorization.
        Try to add tablature with mismatching authorization.
        Try to add tablature with user that doesn't exit
        Try to add malformed data.
        '''
        data = '{"body":"10110101", "user_nickname":"jonne"}'
        response = self.client.post('/tab_archive/artists/paula koivuniemi/kuka pelkaa paulaa', data = data , content_type = 'application/json')
        self.assertEqual(response.status_code, 401)
        
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        
        response = precond_user(self.client)
       
        response = self.client.post('/tab_archive/artists/paula koivuniemi/kuka pelkaa paulaa', data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 401)
        
        data = '{"body":"10110101", "user_nickname":"erkki"}'
        response = self.client.post('/tab_archive/artists/paula koivuniemi/kuka pelkaa paulaa', data = data , content_type = 'application/json')
        self.assertEqual(response.status_code, 401)
        
        data = '{"herp derp"}'
        response = self.client.post('/tab_archive/artists/paula koivuniemi/kuka pelkaa paulaa', data = data , content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
       
    def test_get(self):
        response = precond_user_tablature(self.client)
        
        location = response["Location"]
    
        #Here we try to get tablatures to song
        response = self.client.get('/tab_archive/artists/paula koivuniemi/kuka pelkaa paulaa', {"Accept":"application/json"}, content_type = "application/json")
        
        content = json.loads(response.content)
        
        expected = {u'artist_id': u'paula koivuniemi', 
        u'tablatures': 
        [{u'rating': 0, u'tablature_id': 1, u'link': 
        {u'href': u'http://testserver/tab_archive/tablatures/1', u'rel': u'self'}}], 
        u'song_id': u'kuka pelkaa paulaa'}
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, expected)
        
    def tearDown(self):
        #Make sure that no data is retained between tests
        db.drop_tables()
        

class TestSongs(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        
        #Make sure that tables exist for each test
        db.create_users_table("debug.db")
        db.create_tablatures_table("debug.db")
        db.create_comments_table("debug.db")  

    def test_get(self):
        '''
        Try to get list of songs added to the database.
        '''
    
        response = precond_user_tablature2(self.client)
        
        #Here we try to get songs
        response = self.client.get('/tab_archive/songs', {"Accept":"application/json"}, content_type = "application/json")
        self.assertEqual(response.status_code, 200)
        
        expected = [{u'song': {u'song_id': u'kuuntelen tomppaa', u'link': {u'href': u'http://testserver/tab_archive/artists/Metallica/kuuntelen%20tomppaa', u'rel': u'self'}}, u'artist': {u'artist_id': u'Metallica', u'link': {u'href': u'http://testserver/tab_archive/artists/Metallica', u'rel': u'self'}}},
        {u'song': {u'song_id': u'kuka pelkaa paulaa', u'link': {u'href': u'http://testserver/tab_archive/artists/paula%20koivuniemi/kuka%20pelkaa%20paulaa', u'rel': u'self'}}, u'artist': {u'artist_id': u'paula koivuniemi', u'link': {u'href': u'http://testserver/tab_archive/artists/paula%20koivuniemi', u'rel': u'self'}}},
        {u'song': {u'song_id': u'kuuntelen tomppaa', u'link': {u'href': u'http://testserver/tab_archive/artists/paula%20koivuniemi/kuuntelen%20tomppaa', u'rel': u'self'}}, u'artist': {u'artist_id': u'paula koivuniemi', u'link':{u'href': u'http://testserver/tab_archive/artists/paula%20koivuniemi', u'rel': u'self'}}}]
        
        content = json.loads(response.content)
        self.assertEqual(content, expected)
        
        
    def tearDown(self):
        #Make sure that no data is retained between tests
        db.drop_tables()
        

class TestTablature(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        
        #Make sure that tables exist for each test
        db.create_users_table("debug.db")
        db.create_tablatures_table("debug.db")
        db.create_comments_table("debug.db")  
        
    def test_get(self):
        '''
        Try to get tablature.
        '''
    
        response = precond_user_tablature(self.client)
        
        location = response["Location"]
        tablature_id = location[location.rfind("/") + 1 :]
        #Here we try to get tablature
        
        response = self.client.get('/tab_archive/tablatures/' + tablature_id, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        
        content = json.loads(response.content)
        expected = {u'body': u'10110101', u'rating': 0, u'song_id': u'kuka pelkaa paulaa', 
        u'tablature_id': 1, u'rating_count': 0, u'artist_id': u'paula koivuniemi', 
        u'link': {u'href': u'http://testserver/tab_archive/users/jonne', u'rel':u'self'}, 
        u'user_nickname': u'jonne',
        u'comments': {u'href': u'http://testserver/tab_archive/tablatures/1/comments', u'rel':u'self'}
        }
        
        self.assertEqual(content, expected)
        
    def test_post(self):
        '''
        Try to post comment to tablature
        '''
        response = precond_user_tablature(self.client)
        
        location = response["Location"]
        tablature_id = location[location.rfind("/") + 1 :]
        
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        
        data = '{"user_nickname":"erkki", "email":"erkki@yahoo.fi", "picture":"minajarattori.jpg", "description":"paras"}'
        response = self.client.put('/tab_archive/users/erkki', data = data , content_type = 'application/json')
        
        #Here we try to post comment to a tablature
        data = '{"user_nickname":"erkki", "body":"onpa hyva, tykkaan!"}' 
        response = self.client.post('/tab_archive/tablatures/' + tablature_id, data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 201)
        
        location = response["Location"]
                
        self.assertEqual(location, 'http://testserver/tab_archive/tablatures/1/1')
        
    def test_post_fail(self):
        '''
        Try to post empty comment.
        Try to post without authorization.
        Try to post comment to tablature that doesn't exist.
        '''
        response = precond_user_tablature(self.client)
        
        location = response["Location"]
        tablature_id = location[location.rfind("/") + 1 :]
        
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        
        data = '{"user_nickname":"erkki", "email":"erkki@yahoo.fi", "picture":"minajarattori.jpg", "description":"paras"}'
        response = self.client.put('/tab_archive/users/erkki', data = data , content_type = 'application/json')
        
        data = '{}' 
        response = self.client.post('/tab_archive/tablatures/' + tablature_id, data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 400)
        
        data = '{"user_nickname":"erkki", "body":"onpa hyva, tykkaan!"}' 
        response = self.client.post('/tab_archive/tablatures/' + tablature_id, data = data , content_type = 'application/json', )
        self.assertEqual(response.status_code, 401)
        
        data = '{"user_nickname":"erkki", "body":"onpa hyva, tykkaan!"}'
        response = self.client.post('/tab_archive/tablatures/2' , data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 404)
        
    def test_put(self):
        '''
        Try to modify tablature.
        '''
        
        response = precond_user_tablature(self.client)
        
        location = response["Location"]
        tablature_id = location[location.rfind("/") + 1 :]
   
        #Here we try to put modified version of tablature
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
        data = '{"body":"11111111"}'
        response = self.client.put('/tab_archive/tablatures/' + tablature_id, data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 204)
    
    def test_put_fail(self):
        '''
        Try to put empty data to existing tablature.
        Try to edit without authorization.
        Try to edit tablature that doesn't exist.
        '''
        response = precond_user_tablature(self.client)
        
        location = response["Location"]
        tablature_id = location[location.rfind("/") + 1 :]
        
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
        data = '{}'
        response = self.client.put('/tab_archive/tablatures/' + tablature_id, data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 400)
        
        
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        data = '{"body":"11111111"}'
        response = self.client.put('/tab_archive/tablatures/' + tablature_id, data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 401)
        
        
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
        data = '{"body":"11111111"}'
        response = self.client.put('/tab_archive/tablatures/9', data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 404)
        
        
    def test_delete(self):
        '''
        Try to delete tablature.
        '''
        response = precond_user_tablature(self.client)

        location = response["Location"]
        tablature_id = location[location.rfind("/") + 1 :]
        
        #Here we try to delete tablature
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
        response = self.client.delete('/tab_archive/tablatures/' + tablature_id, content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 204)
        
    def test_delete_fail(self):
        '''
        Try to delete tablature that doesn't exist.
        Try to delete tablature without authorization.
        '''
        response = precond_user_tablature(self.client)

        location = response["Location"]
        tablature_id = location[location.rfind("/") + 1 :]
        
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
        response = self.client.delete('/tab_archive/tablatures/9', content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 404)
        
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        response = self.client.delete('/tab_archive/tablatures/1', content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 401)
        
    def tearDown(self):
        #Make sure that no data is retained between tests
        db.drop_tables()
        

class TestTablatures(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        
        #Make sure that tables exist for each test
        db.create_users_table("debug.db")
        db.create_tablatures_table("debug.db")
        db.create_comments_table("debug.db")
        
    def test_post(self):
        '''
        Post a new tablature.
        '''
        
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
    
        response = precond_user(self.client)
    
        #Here we try to post tablature
        data = '{"body":"10110101", "artist_id":"paula koivuniemi", "song_id":"kuka pelkaa paulaa", "user_nickname":"jonne"}'
        response = self.client.post('/tab_archive/tablatures', data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 201)
        location = response["Location"]
        self.assertEqual(location, 'http://testserver/tab_archive/tablatures/1')
        
    def test_post_fail(self):
        ''' 
        Try to post without authorization.
        Try to post empty data.
        '''
    
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
    
        response = precond_user(self.client)
    
        #Here we try to post tablature
        data = '{"body":"10110101", "artist_id":"paula koivuniemi", "song_id":"kuka pelkaa paulaa", "user_nickname":"jonne"}'
        response = self.client.post('/tab_archive/tablatures', data = data , content_type = 'application/json',)
        self.assertEqual(response.status_code, 401)
        
        response = self.client.post('/tab_archive/tablatures', data = {} , content_type = 'application/json',)
        self.assertEqual(response.status_code, 400)
        
    def test_get(self):
        '''
        Try to get list of tablatures.
        '''
        
        response = precond_user_tablature(self.client)
        
        #Here we try to get list of tablatures
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
        response = self.client.get('/tab_archive/tablatures', content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 200)
        
        content = json.loads(response.content)
        
        expected = [{u'tablature': {u'rating': 0, u'tablature_id': 1, u'rating_count': 0, u'link': {u'href': u'http://testserver/tab_archive/tablatures/1', u'rel': u'self'}, u'user': {u'link': {u'href':u'http://testserver/tab_archive/users/jonne', u'rel': u'self'}, u'user_nickname': u'jonne'}}, u'artist': {u'artist_id': u'paula koivuniemi', u'link': {u'href': u'http://testserver/tab_archive/artists/paula%20koivuniemi', u'rel': u'self'}}, u'song': {u'song_id': u'kuka pelkaa paulaa', u'link': {u'href': u'http://testserver/tab_archive/artists/paula%20koivuniemi/kuka%20pelkaa%20paulaa', u'rel': u'self'}}}]
        
        self.assertEqual(content, expected)
    
    def test_get_fail(self):
        '''
        Try to get from empty database.
        '''
        response = self.client.get('/tab_archive/tablatures', content_type = 'application/json')
        self.assertEqual(response.status_code, 404)
        
    def tearDown(self):
        #Make sure that no data is retained between tests
        db.drop_tables()
        
        
class TestComment(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        
        #Make sure that tables exist for each test
        db.create_users_table("debug.db")
        db.create_tablatures_table("debug.db")
        db.create_comments_table("debug.db")  
        
    def test_get(self):
        '''
        Try to get comment.
        '''
        
        response = precond_user_tablature(self.client)
        
        location = response["Location"]
        tablature_id = location[location.rfind("/") + 1 :]
        
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        
        data = '{"user_nickname":"erkki", "email":"erkki@yahoo.fi", "picture":"minajarattori.jpg", "description":"paras"}'
        response = self.client.put('/tab_archive/users/erkki', data = data , content_type = 'application/json')
       
        data = '{"user_nickname":"erkki", "body":"onpa hyva, tykkaan!"}' 
        response = self.client.post('/tab_archive/tablatures/' + tablature_id, data = data , content_type = 'application/json', **extra)
       
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
        data = '{"user_nickname":"jonne", "body":"niin munstaki!!"}' 
        response = self.client.post('/tab_archive/tablatures/1/1', data = data , content_type = 'application/json', **extra)
       
        #Here we try to get comment
        response = self.client.get('/tab_archive/tablatures/1/2', content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        
        content = json.loads(response.content)
        
        expected = {u'comment': {u'body': u'niin munstaki!!', u'reply_to': 1, u'tablature_id': 1, u'user_nickname': u'jonne'}, u'reply_to': 
        {u'href': u'http://testserver/tab_archive/tablatures/1/1', u'rel': u'self'}, u'user': 
        {u'link': {u'href': u'http://testserver/tab_archive/users/jonne', u'rel': u'self'}, u'user_nickname': u'jonne'}}
        self.assertEqual(content, expected)
        
    def test_get_fail(self):
        '''
        Try to get comment that doesn't exist
        '''
        response = precond_user_tablature(self.client)
        
        location = response["Location"]
        tablature_id = location[location.rfind("/") + 1 :]
        
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        
        data = '{"user_nickname":"erkki", "email":"erkki@yahoo.fi", "picture":"minajarattori.jpg", "description":"paras"}'
        response = self.client.put('/tab_archive/users/erkki', data = data , content_type = 'application/json')
       
        data = '{"user_nickname":"erkki", "body":"onpa hyva, tykkaan!"}' 
        response = self.client.post('/tab_archive/tablatures/' + tablature_id, data = data , content_type = 'application/json', **extra)
       
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
        data = '{"user_nickname":"jonne", "body":"niin munstaki!!"}' 
        response = self.client.post('/tab_archive/tablatures/1/1', data = data , content_type = 'application/json', **extra)
        
        response = self.client.get('/tab_archive/tablatures/1/3', content_type = 'application/json')
        self.assertEqual(response.status_code, 404)
       
    def test_post(self):
        '''
        Try to post reply to comment.
        '''
        
        response = precond_user_tablature(self.client)
       
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        
        data = '{"user_nickname":"erkki", "email":"erkki@yahoo.fi", "picture":"minajarattori.jpg", "description":"paras"}'
        response = self.client.put('/tab_archive/users/erkki', data = data , content_type = 'application/json')
       
        data = '{"user_nickname":"erkki", "body":"hieno tabu, hermanni!"}' 
        response = self.client.post('/tab_archive/tablatures/1', data = data , content_type = 'application/json', **extra)
       
        #Here we try to post reply to comment
        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
        data = '{"user_nickname":"jonne", "body":"niin munstaki!!"}' 
        response = self.client.post('/tab_archive/tablatures/1/1', data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 204)
        
        location = response["Location"]
                
        self.assertEqual(location, 'http://testserver/tab_archive/tablatures/1/2')
        
    def test_post_fail(self):
        '''
        Try to post unauthorized.
        Try to post empty data.
        Try to reply to comment that dosen't exist.
        '''
        response = precond_user_tablature(self.client)
       
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        
        data = '{"user_nickname":"erkki", "email":"erkki@yahoo.fi", "picture":"minajarattori.jpg", "description":"paras"}'
        response = self.client.put('/tab_archive/users/erkki', data = data , content_type = 'application/json')
       
        data = '{"user_nickname":"erkki", "body":"hieno tabu, hermanni!"}' 
        response = self.client.post('/tab_archive/tablatures/1', data = data , content_type = 'application/json', **extra)
       
        #Here we try to post reply to comment
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        data = '{"user_nickname":"jonne", "body":"niin munstaki!!"}' 
        response = self.client.post('/tab_archive/tablatures/1/1', data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 401)

        extra = {
            'HTTP_AUTHORIZATION': "jonne"
        }
        
        data = '{}' 
        response = self.client.post('/tab_archive/tablatures/1/1', data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 400)
        
        data = '{"user_nickname":"jonne", "body":"niin munstaki!!"}' 
        response = self.client.post('/tab_archive/tablatures/2/2', data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 404)
        
        
        
    def test_delete(self):
        '''
        Try to delete comment.
        '''
        response = precond_user_tablature(self.client)
       
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        
        data = '{"user_nickname":"erkki", "email":"erkki@yahoo.fi", "picture":"minajarattori.jpg", "description":"paras"}'
        response = self.client.put('/tab_archive/users/erkki', data = data , content_type = 'application/json')
       
        data = '{"user_nickname":"erkki", "body":"hieno tabu, hermanni!"}' 
        response = self.client.post('/tab_archive/tablatures/1', data = data , content_type = 'application/json', **extra)

        #Here we try to delete comment
        response = self.client.delete('/tab_archive/tablatures/1/1', content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 204)
        
    def test_put(self):
        '''
        Try to edit comment.
        '''
        
        response = precond_user_tablature(self.client)
       
        extra = {
            'HTTP_AUTHORIZATION': "erkki"
        }
        
        data = '{"user_nickname":"erkki", "email":"erkki@yahoo.fi", "picture":"minajarattori.jpg", "description":"paras"}'
        response = self.client.put('/tab_archive/users/erkki', data = data , content_type = 'application/json')
       
        data = '{"user_nickname":"erkki", "body":"hieno tabu, hermanni!"}' 
        response = self.client.post('/tab_archive/tablatures/1', data = data , content_type = 'application/json', **extra)
        
        #Here we try to put edited version of comment
        data = '{"body":"aika sux"}' 
        response = self.client.put('/tab_archive/tablatures/1/1', data = data , content_type = 'application/json', **extra)
        self.assertEqual(response.status_code, 204)
        
        
    def tearDown(self):
        #Make sure that no data is retained between tests
        db.drop_tables()


class TestRating(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        
        #Make sure that tables exist for each test
        db.create_users_table("debug.db")
        db.create_tablatures_table("debug.db")
        db.create_comments_table("debug.db")
        
        
    def test_post(self):
        '''
        Rate a tablutature.
        '''
        response = precond_user_tablature(self.client)
        
        #Here we try to post rating to tablature

        data = '{"rating":5}'
        response = self.client.post('/tab_archive/tablatures/1/rating', data = data , content_type = 'application/json', )
        self.assertEqual(response.status_code, 200)
        
    def test_get(self):
        '''
        Get rating of tablature.
        '''
        response = precond_user_tablature(self.client)

        data = '{"rating":5}'
        response = self.client.post('/tab_archive/tablatures/1/rating', data = data , content_type = 'application/json', )
        self.assertEqual(response.status_code, 200)
        
        #here we try to get tablature rating
        response = self.client.get('/tab_archive/tablatures/1/rating', content_type = 'application/json', )
        self.assertEqual(response.status_code, 200)
        
        content = json.loads(response.content)
        self.assertEqual(content["rating"], 5)
        self.assertEqual(content["rating_count"], 1)
        
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
        '''
        Get list of artists.
        '''
        response = precond_user_tablature(self.client)
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
        
        songs = self.handle.get_songs("tuttiritari", None)
        songs.sort()
        
        expected = [["tuttiritari", "tutti viimeinen"],["tuttiritari", "toinen tutti"]]
        expected.sort()

        self.assertEqual(expected,songs)

        songs = self.handle.get_songs("", None)
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
        
        

        songs = self.handle.get_songs("", None)
        songs.sort()

        expected = [["tuttiritari", "tutti viimeinen"], ["tuttiritari", "toinen tutti"], ["paula koivuniemi", "kuka pelkaa paulaa"]]
        expected.sort()

        self.assertEqual(expected,songs)
    
    def test_get_songs_fail(self):
        '''
        Try to get songs whene there is none.
        '''
        songs = self.handle.get_songs("paula koivuniemi", None)
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
        
        artists = self.handle.get_artists(None)
        artists.sort()
    
        expected = ["tuttiritari","paula koivuniemi"]
        expected.sort()

        self.assertEqual(artists, expected)

    def test_get_artists_fail(self):
        '''
        Try to get artists when no tablatures has been added.
        '''
        artists = self.handle.get_artists(None)
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
        
        tablatures = self.handle.get_tablatures('paula koivuniemi','kuka pelkaa paulaa')
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
        
        edit = TablatureModel.create({'tablature_id':tab_id, 'body':"1111111", "rating":0, "artist_id":None, "song_id":"tutti viimeinen", "user_nickname":"erkki", "rating_count":0})
        
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