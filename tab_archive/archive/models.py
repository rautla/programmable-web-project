# -*- coding: utf-8 -*-

from datetime import datetime, date
import re

# Create your models here.
class UserModel(object):
    
    
    def __init__(self, user_nickname, raw_data = None):
    
        self.user_nickname = user_nickname
        self.email = raw_data.get('email', None) if raw_data else None
        self.picture = raw_data.get('picture', None) if raw_data else None
        self.description = raw_data.get('description', None) if raw_data else None
        
        super(UserModel, self).__init__()
        
    @classmethod 
    def create(cls, row):
        user = UserModel(row['user_nickname'])
        user.email = row['email']
        user.description = row['description']
        user.picture = row['picture']
        return user
        
    def serialize(self):
    
        return {'user_nickname':self.user_nickname, 'email':self.email, 'description':self.description, 'picture':self.picture }
        
class CommentModel(object):
    
    
    def  __init__(self, comment_id, reply_to=None, raw_data=None, tablature_id=None):
        
        self.comment_id = comment_id
        self.reply_to = reply_to
        self.body = None
        self.tablature_id = tablature_id
        self.user_nickname = None #Nickname of sender
        
        if raw_data is not None:
            self.body = raw_data.get('body', None)
            self.user_nickname = raw_data.get('user_nickname', None)
        
        super(CommentModel, self).__init__()
        
    @classmethod
    def create(cls, row):
    
        reply_to = row['reply_to'] if row['reply_to'] is not None else ""
        tablature_id = row['tablature_id'] if row['tablature_id'] is not None else ""
		
        comment = CommentModel(row["comment_id"], reply_to=reply_to, tablature_id=tablature_id)
        comment.user_nickname = row['user_nickname']
        comment.body = row['body']
        return comment
        
    def serialize(self):
        _entity = {}
        _entity['body'] = self.body
        _entity['user_nickname'] = self.user_nickname
        _entity['tablature_id'] = self.tablature_id
        if self.reply_to is not None:
            _entity['reply_to'] = self.reply_to
        return _entity
        
class TablatureModel(object):

    def __init__(self, tablature_id, raw_data = None):
        self.tablature_id = tablature_id
        self.body = None
        self.rating = None
        self.artist_id = None
        self.song_id = None
        self.user_nickname = None
        self.rating_count = None
        if raw_data is not None:
            self.body = raw_data.get('body', None) 
            self.rating = raw_data.get('rating', None) 
            self.artist_id = raw_data.get('artist_id', None) 
            self.song_id = raw_data.get('song_id', None)
            self.user_nickname = raw_data.get('user_nickname', None)
            self.rating_count = raw_data.get('rating_count', None)
            
        super(TablatureModel, self).__init__()
            
    @classmethod
    def create(cls, row):
    
        tablature = TablatureModel(row['tablature_id'])
        tablature.body = row['body']
        tablature.rating = row['rating']
        tablature.artist_id = row['artist_id']
        tablature.song_id = row['song_id']
        tablature.user_nickname = row['user_nickname']
        tablature.rating_count = row['rating_count']
        return tablature
        
    def serialize(self):
        _entity = {}
        _entity['body'] = self.body
        _entity['tablature_id'] = self.tablature_id
        _entity['rating'] = self.rating
        _entity['artist_id'] = self.artist_id
        _entity['song_id'] = self.song_id
        _entity['user_nickname'] = self.user_nickname
        _entity['rating_count'] = self.rating_count
        return _entity
        
        
class ErrorModel(object):
    def __init__(self, errormessage):
        self.errormessage = errormessage
    def serialize(self):
        _entity = {}
        _entity['error'] = self.errormessage
        return _entity