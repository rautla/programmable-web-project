from django.utils import unittest
from django.test.client import Client
import json


class UserTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_get(self):
        # Issue a GET request.
        response = self.client.get('/tab_archive/users/erkki', {"Accept":"application/json"})
     
        content = json.loads(response.content)
        print content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['picture'], "erkki.png")
        self.assertEqual(content['description'], "hevosmies")
        self.assertFalse(content.has_key('email'))

    def test_get_authorized(self):
        # Issue a GET request.
        response = self.client.get('/tab_archive/users/erkki', {"Accept":"application/json", "Authorization":"erkki"})
     
        content = json.loads(response.content)
        print content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['picture'], "erkki.png")
        self.assertEqual(content['description'], "hevosmies")
        self.assertEqual(content['email'], "erkki@pertti.fi")
        
    def test_get_fail(self):
        response = self.client.get('/tab_archive/users/olli', {"Accept":"application/json"})
        
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        response = self.client.get('/tab_archive/users/erkki', {"Accept":"application/json"})
     
        content = json.loads(response.content)
        
        self.assertEqual(response.status_code, 200)
        
        