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
            self.user_nickname = raw.data.get('user_nickname', None)
        
        super(CommentModel, self).__init__()
        
    @classmethod
    def create(cls, row):
    
        reply_to = str(row['reply_to']) if row['reply_to'] is not None else ""
        
        comment = CommentModel(str(row["comment_id"]), reply_to=reply_to, tablature_id=tablature_id)
        comment.user_nickname = row ['user_nickname']
        comment.body = row ['body']
        return comment
        
    def serialize(self):
        _entity = {}
        _entity['body'] = self.body
        _entity['user_nickname'] = self.user_nickname
        if self.reply_to is not None:
            _entity['reply_to'] = self.reply_to
        return _entity
        
class TablatureModel(object):

    def __init__(self, tablature_id, raw_data = None):
        self.tablature_id = tablature_id
        self.body = None
        self.rating = None
        self.artist_id = None
        user_nickname = None
        if raw_data is not None:
            self.body = raw_data.get('body', None) 
            self.rating = raw_data.get('rating', None) 
            self.artist_id = raw_data.get('artist_id', None) 
            self.user_nickname = raw_data.get('user_nickname', None)
            
        super(TablatureModel, self).__init__()
            
    @classmethod
    def create(cls, row):
    
        tablature = TablatureModel(row['tablature_id'])
        tablature.body = row['body']
        tablature.rating = row['rating']
        tablature.artist_id = row['artist_id']
        tablature.user_nickname = row['user_nickname']
        return tablature
        
    def serialize(object):
        _entity = {}
        _entity['body'] = self.body
        _entity['tablature_id'] = self.tablature_id
        _entity['rating'] = self.rating_id
        _entity['artist_id'] = row['artist_id']
        _entity['user_nickname'] = row['user_nickname']
        return _entity
        
        
class ErrorModel(object):
    def __init__(self, errormessage):
        self.errormessage = errormessage
    def serialize(self):
        _entity = {}
        _entity['error'] = self.errormessage
        return _entity