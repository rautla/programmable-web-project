from exceptions import NotImplementedError
import re
from datetime import datetime
import time

import sqlite3
import sys


from archive.models import UserModel, TablatureModel, CommentModel

class ArchiveDatabaseInterface(object):
    '''
    The methods of this class work with archive models...
    '''
    
    def __init__(self):
        super(ArchiveDatabaseInterface, self).__init__()
        
    #TABLATURES
    def get_songs(self, artist):
        '''
        Return list of songs by artist.
        If artist parameter is left empty return all songs.
        Return "not found" error if artist or songs not found.
        '''
        
        raise NotImplementedError("")
        
    def get_artists():
        '''
        Return list of unique artists.
        '''
        
        raise NotImplementedError("")
        
    def get_tablatures(self, artist, song):
        '''
        Return list of tablatures to specified song.
        If parameters are left empty return all tablatures.
        If song parameter is left empty return all tablatures by artist.
        Return "not found error if song, artist or tablatures are not found.
        '''
        
        raise NotImplementedError("")
        
    def edit_tablature(self, tablature_id):
        '''
        Return tablature.
        '''
        
        raise NotImplementedError("")
        
    def delete_tablature(self, tablature_id):
        '''
        Delete tablature.
        '''
    
        raise NotImplementedError("")
        
    def add_tablature(self, artist, song, tablature):
        '''
        Add tablature to database.
        '''
        
        raise NotImplementedError("")
        
    def get_rating(self, tablature_id):
        '''
        Returns current rating fir the tablature.
        '''
        
        raise NotImplementedError("")
        
    def add_rating(self, tablature_id, rating):
        '''
        Calculate new rating.
        Returns "not found" error if tablature doesn't exist.
        '''
            
        raise NotImplementedError("")
        
   
    #COMMENT
    def get_comment(self, comment_id):
        '''
        Returns the comment.
        If comment doesn't exist return "not found" error.
        '''
        
        raise NotImplementedError("")
        
    def modify_comment(self, comment_id):
        '''
        Changes the comment in database to modified version.
        If comment doesn't exist return "not found" error.
        If user is not the original poster, return "unauthorized" error.
        '''
        
        raise NotImplementedError("")
        
    def delete_comment(self, comment_id):
        '''
        Deletes comment.
        If comment doesn't exist return "not found" error.
        If user is not the original poster, return "unauthorized" error.
        '''
        
        raise NotImplementedError("")
        
    def add_comment(self, comment):
        '''
        Adds comment to table.
        Return "unauthorized" if user is not logged in.
        '''
        
        raise NotImplementedError("")
        
    #USERS
    def get_user(self, user_id):
        '''
        returns user.
        Return "not found" error if user not found.
        '''
        
        raise NotImplementedError("")
        
    def edit_user(self, user_id, changes):
        '''
        Edit user information.
        Return "not found" error if user not found
        '''
        
        raise NotImplementedError("")
        
    def delete_user(self, user_id):
        '''
        Deletes user.
        Return "not found" error if user not found.
        '''
        
        raise NotImplementedError("")
        
    def get_users(self):
        '''
        Get list of users.
        '''
        
        raise NotImplementedError("")
        
class ArchiveDatabase(ArchiveDatabaseInterface):
    #TABLATURE
    def get_songs(self, artist):
        '''
        Return list of songs by artist.
        If artist parameter is left empty return all songs.
        Return "not found" error if artist or songs not found.
        '''
        
        return
        
    def get_artists():
        '''
        Return list of unique artists.
        '''
        
        raise NotImplementedError("")
        
    def get_tablatures(self, artist, song):
        '''
        Return list of tablatures to specified song.
        If parameters are left empty return all tablatures.
        If song parameter is left empty return all tablatures by artist.
        Return "not found error if song, artist or tablatures are not found.
        '''
        
        raise NotImplementedError("")
        
    def edit_tablature(self, tablature_id):
        '''
        Return tablature.
        '''
        
        raise NotImplementedError("")
        
    def delete_tablature(self, tablature_id):
        '''
        Delete tablature.
        '''
    
        raise NotImplementedError("")
        
    def add_tablature(self, artist, song, tablature):
        '''
        Add tablature to database.
        '''
        
        raise NotImplementedError("")
        
    def get_rating(self, tablature_id):
        '''
        Returns current rating fir the tablature.
        '''
        
        raise NotImplementedError("")
        
    def add_rating(self, tablature_id, rating):
        '''
        Calculate new rating.
        Returns "not found" error if tablature doesn't exist.
        '''
            
        raise NotImplementedError("")
        
   
    #COMMENT
    def get_comment(self, comment_id):
        '''
        Returns the comment.
        If comment doesn't exist return "not found" error.
        '''
        
        raise NotImplementedError("")
        
    def modify_comment(self, comment_id):
        '''
        Changes the comment in database to modified version.
        If comment doesn't exist return "not found" error.
        If user is not the original poster, return "unauthorized" error.
        '''
        
        raise NotImplementedError("")
        
    def delete_comment(self, comment_id):
        '''
        Deletes comment.
        If comment doesn't exist return "not found" error.
        If user is not the original poster, return "unauthorized" error.
        '''
        
        raise NotImplementedError("")
        
    def add_comment(self, comment):
        '''
        Adds comment to table.
        Return "unauthorized" if user is not logged in.
        '''
        
        raise NotImplementedError("")
        
    #USERS
    def get_user(self, user_id):
        '''
        returns user.
        Return "not found" error if user not found.
        '''
        
        raise NotImplementedError("")
        
    def edit_user(self, user_id, changes):
        '''
        Edit user information.
        Return "not found" error if user not found
        '''
        
        raise NotImplementedError("")
        
    def delete_user(self, user_id):
        '''
        Deletes user.
        Return "not found" error if user not found.
        '''
        
        raise NotImplementedError("")
        
    def get_users(self):
        '''
        Get list of users.
        '''
        
        raise NotImplementedError("")