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
        
    #USERS
    def add_user(self, user_nickname, info):
        '''
        returns user.
        Return "not found" error if user not found.
        '''
        
        raise NotImplementedError("")
    
    def get_user(self, user_nickname):
        '''
        returns user.
        Return "not found" error if user not found.
        '''
        
        raise NotImplementedError("")
        
    def edit_user(self, user_nickname, changes):
        '''
        Edit user information.
        Return "not found" error if user not found
        '''
        
        raise NotImplementedError("")
        
    def delete_user(self, user_nickname):
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
    
    #TABLATURES
    def get_songs(self, artist):
        '''
        Return list of songs by artist.
        If artist parameter is left empty return all songs.
        Return "not found" error if artist or songs not found.
        '''
        
        raise NotImplementedError("")
        
    def get_artists(self):
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
        

        
class ArchiveDatabase(ArchiveDatabaseInterface, database_name = 'archive.db'):
    
    def __init__(self, database_name = 'archive.db'):
        super(ArchiveDatabaseInterface, self).__init__()
        self.database_name = database_name

    #USERS
    def add_user(self, user):
        '''
        Adds new user.
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        #Get the user_nickname of a user given the Nickname
        query = 'SELECT * FROM users WHERE user_nickname = ?'
        pvalue = (user.user_nickname,)
        
        #user_nickname = None
        
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(query, pvalue)
            #just one result possible
            row = cur.fetchone()
            if row is None:
                stmnt = 'INSERT INTO users(user_nickname,email,picture,description) VALUES(?,?,?,?)'
                pvalue = (user.user_nickname,user.email,user.picture,user.description)
                cur.execute(stmnt, pvalue)
                return user.user_nickname
            else:
                return None
        
    def get_user(self, user_nickname):
        '''
        returns user.
        Return "not found" error if user not found.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        #Get the user_nickname of a user given the Nickname
        query = 'SELECT * FROM users WHERE user_nickname = ?'
        pvalue = (user_nickname,)
        
        #user_nickname = None
        
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(query, pvalue)
            #just one result possible
            row = cur.fetchone()
            if row is None:
                return None
            else:    
                print row.keys()
                
                return UserModel.create(row)        
    
    def edit_user(self, user_nickname, changes):
        '''
        Edit user information.
        Return "not found" error if user not found
        '''
       
        keys_on = 'PRAGMA foreign_keys = ON'
        #Get the user_nickname of a user given the Nickname
        query = 'SELECT * FROM users WHERE user_nickname = ?'
        pvalue = (user.user_nickname,)
        
        #user_nickname = None
        
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(query, pvalue)
            #just one result possible
            row = cur.fetchone()
            if row is None:
                return None
            else:
                stmnt = 'UPDATE users SET description = ?, picture= ?,email= ? WHERE user_nickname = ?'
                pvalue = (user.description or row["description"],user.picture or row["picture"],user.email or row["email"])
                cur.execute(stmnt,pvalue)
                
                return user.user_nickname
 
        
    def delete_user(self, user_nickname):
        '''
        Deletes user.
        Return "not found" error if user not found.
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        #Get the user_nickname of a user given the Nickname
        query = 'SELECT * FROM users WHERE user_nickname = ?'
        pvalue = (user.user_nickname,)
        
        #user_nickname = None
        
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(query, pvalue)
            #just one result possible
            row = cur.fetchone()
            if row is None:
                return None
            else:
                stmnt = 'DELETE FROM users WHERE user_id = ?'
                pvalue = (user_id,)
                #execute the statement
                cur.execute(stmnt, pvalue)
                
                return user_nickname
        
    def get_users(self):
        '''
        Get list of users.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        #Get the user_nickname of a user given the Nickname
        query = 'SELECT * FROM users'
        pvalue = (user.user_nickname,)
        
        #user_nickname = None
        
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(query, pvalue)
            #get results
            rows = cur.fetchall()
            if rows is None:
                return None
                
            users = []
            for row in rows:
                users.append(UserModel.create(row))
            return users
    
    #TABLATURE
    def get_songs(self, artist):
        '''
        Return list of songs by artist.
        If artist parameter is left empty return all songs.
        Return "not found" error if artist or songs not found.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        if artist == '':
            query = 'SELECT * FROM tablatures'
        else:
            query = 'SELECT * FROM tablatures WHERE artist_id = ?'
            pvalue = (artist,)
        
        #song_id = None
        
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            if artist == '':
                cur.execute(query)
            else:
                cur.execute(query, pvalue)
            #get results
            rows = cur.fetchall()
            if rows is None:
                return None
                
            songs = []
            for row in rows:
                songs.append(row)
            return songs

        
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
        

        
def check_foreign_keys_status(database_name = 'archive.db'):
    '''
    Checks the status of foreign keys
    '''
    con = None
    try:
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(database_name)
        #get the cursor object. It allows to execute SQL code and traverse the result set
        cur = con.cursor()    
        #execute the pragma command
        cur.execute('PRAGMA foreign_keys = ON')
        #we know we retrieve just one record: use ftchone()
        data = cur.fetchone()
        
        print "Foreign Keys status: %s" % data                
        
    except sqlite3.Error, e:
        
        print "Error: %s" % e.args[0]
        sys.exit(1)
        
    finally:
        
        if con:
            con.close()
    return data
def set_and_check_foreign_keys_status(database_name = 'archive.db'):
    '''
    Sets and checks the status of foreign keys
    '''
    keys_on = 'PRAGMA foreign_keys = ON'
    con = None
    try:
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(database_name)
        #get the cursor object. It allows to execute SQL code and traverse the result set
        cur = con.cursor()
        #execute the pragma command, ON 
        cur.execute(keys_on)
        #execute the pragma check command
        cur.execute('PRAGMA foreign_keys = ON')
        #we know we retrieve just one record: use ftchone()
        data = cur.fetchone()
        
        print "Foreign Keys status: %s" % data                
        
    except sqlite3.Error, e:
        print "Error: %s" % e.args[0]
        sys.exit(1)
        
    finally:
        if con:
            con.close()
    return data
    
def create_users_table(database_name = 'archive.db'):
    keys_on = 'PRAGMA foreign_keys = ON'

    stmnt = 'CREATE TABLE "users" ("user_nickname" TEXT PRIMARY KEY  NOT NULL  UNIQUE , "email" TEXT, "picture" TEXT, "description" TEXT)'

    #connects (and creates if necessary) to the database. gets a connection object
    con = sqlite3.connect(database_name)
    with con:
        #get the cursor object. It allows to execute SQL code and traverse the result set
        cur = con.cursor() 
        try:
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(stmnt)
        except sqlite3.Error,e:
            print "Error: %s" % e.args[0]
    return None

def create_tablatures_table(database_name = 'archive.db'):
    keys_on = 'PRAGMA foreign_keys = ON'

    stmnt = 'CREATE TABLE "tablatures" ("body" TEXT, "tablature_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "rating" INTEGER, "artist_id" TEXT, "song_id" TEXT, "user_nickname" TEXT, "rating_count" INTEGER, FOREIGN KEY(user_nickname) REFERENCES users(user_nickname) ON DELETE CASCADE )'

    #connects (and creates if necessary) to the database. gets a connection object
    con = sqlite3.connect(database_name)
    with con:
        #get the cursor object. It allows to execute SQL code and traverse the result set
        cur = con.cursor() 
        try:
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(stmnt)
        except sqlite3.Error,e:
            print "Error: %s" % e.args[0]
    return None

def create_comments_table(database_name = 'archive.db'):

    keys_on = 'PRAGMA foreign_keys = ON'

    stmnt = 'CREATE TABLE "comments" ("comment_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "body" TEXT, "tablature_id" INTEGER REFERENCES tablatures, "user_nickname" TEXT REFERENCES users, "reply_to" INTEGER REFERENCES comments)'
    
    #connects (and creates if necessary) to the database. gets a connection object
    con = sqlite3.connect(database_name)
    with con:
        #get the cursor object. It allows to execute SQL code and traverse the result set
        cur = con.cursor() 
        try:
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(stmnt)
        except sqlite3.Error,e:
            print "Error: %s" % e.args[0]
    return None

def get_database(database_name = 'archive.db'):    
    return ArchiveDatabase(database_name)
    
