# -*- coding: utf-8 -*-

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
        Return "None" if user not found.
        '''
        
        raise NotImplementedError("")
    
    def get_user(self, user_nickname):
        '''
        returns user.
        Return "None" if user not found.
        '''
        
        raise NotImplementedError("")
        
    def edit_user(self, user):
        '''
        Edit user information.
        Return "None" if user not found
        '''
        
        raise NotImplementedError("")
        
    def delete_user(self, user_nickname):
        '''
        Deletes user.
        Return "None" if user not found.
        '''
        
        raise NotImplementedError("")
        
    def get_users(self):
        '''
        Get list of users.
        '''
        
        raise NotImplementedError("")

    def contains_user(self, user_nickname):
        '''
        Returns true if the user is in the database. False otherwise
        '''
        raise NotImplementedError("")
    
    #TABLATURES
    def get_songs(self, artist):
        '''
        Return list of songs by artist.
        If artist parameter is left empty return all songs.
        Return "None" if artist or songs not found.
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

    def get_tablature(self, tablature_id):
        '''
        Return tablature.
        Return "None" if tablature was not found
        '''
        
        raise NotImplementedError("")
        
    def edit_tablature(self, tablature):
        '''
        Return tablature.
        '''
        
        raise NotImplementedError("")
        
    def delete_tablature(self, tablature_id):
        '''
        Delete tablature.
        '''
    
        raise NotImplementedError("")
        
    def add_tablature(self, tablature):
        '''
        Add tablature to database.
        '''
        
        raise NotImplementedError("")
        
    def get_rating(self, tablature_id):
        '''
        Returns current rating for the tablature.
        '''
        
        raise NotImplementedError("")
        
    def add_rating(self, tablature_id, rating):
        '''
        Calculate new rating.
        Returns "None" if tablature doesn't exist.
        '''
            
        raise NotImplementedError("")
 
    def contains_tablature(self, tablature_id):
        '''
        Returns true if the tablature is in the database. False otherwise
        '''
        raise NotImplementedError("")       
   
    #COMMENT
    def get_comment(self, comment_id):
        '''
        Returns the comment.
        If comment doesn't exist return "None".
        '''
        
        raise NotImplementedError("")
        
    def modify_comment(self, comment):
        '''
        Changes the comment in database to modified version.
        If comment doesn't exist return "None".
        If user is not the original poster, return "unauthorized" error.
        '''
        
        raise NotImplementedError("")
        
    def delete_comment(self, comment_id):
        '''
        Deletes comment.
        If comment doesn't exist return "None".
        If user is not the original poster, return "unauthorized" error.
        '''
        
        raise NotImplementedError("")
        
    def add_comment(self, comment):
        '''
        Adds comment to table.
        Return "unauthorized" if user is not logged in.
        '''
        
        raise NotImplementedError("")
        
    def append_answer(self, comment_id, body, user_nickname):
        '''
        Writes an answer to the message with id=comment_id
        raises ForumDatabaseError if the DB could not be modified.
        raises ValueError if the message_id has a wrong format
        returns the id of the new message
        '''
        
        raise NotImplementedError("")
        
    def contains_comment(self, comment_id):
        '''
        Returns true if the message is in the database. False otherwise.
        '''
        raise NotImplementedError("")        
        
class ArchiveDatabase(ArchiveDatabaseInterface):
    
    def __init__(self, database_name = 'archive.db'):
        super(ArchiveDatabaseInterface, self).__init__()
        self.database_name = database_name

    #USERS
    def add_user(self, user):
        '''
        Adds new user.
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM users WHERE user_nickname = ?'
        pvalue = (user.user_nickname,)
        
        #user_nickname = None
        
        #connects (and creates if necessary) to the database. gets a connection object
        #con = sqlite3.connect(self.database_name)
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
        Return "None" if user not found.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM users WHERE user_nickname = ?'
        pvalue = (user_nickname,)
        
        #user_nickname = None
        
        #connects (and creates if necessary) to the database. gets a connection object
        #con = sqlite3.connect(self.database_name)
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
                #print row.keys()
                
                return UserModel.create(row)        
    
    def edit_user(self, user):
        '''
        Edit user information.
        Return "None" if user not found
        '''
       
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM users WHERE user_nickname = ?'
        pvalue = (user.user_nickname,)
        
        #user_nickname = None
        
        #connects (and creates if necessary) to the database. gets a connection object
        #con = sqlite3.connect(self.database_name)
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
                pvalue = (user.description or row["description"],user.picture or row["picture"],user.email or row["email"],user.user_nickname)
                cur.execute(stmnt,pvalue)
                
                return user.user_nickname
 
        
    def delete_user(self, user_nickname):
        '''
        Deletes user.
        Return "None" if user not found.
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM users WHERE user_nickname = ?'
        pvalue = (user_nickname,)
        
        #user_nickname = None
        
        #connects (and creates if necessary) to the database. gets a connection object
        #con = sqlite3.connect(self.database_name)
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
                stmnt = 'DELETE FROM users WHERE user_nickname = ?'
                pvalue = (user_nickname,)
                #execute the statement
                cur.execute(stmnt, pvalue)
                
                return user_nickname
        
    def get_users(self):
        '''
        Get list of users.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM users'
        
        #user_nickname = None
        
        #connects (and creates if necessary) to the database. gets a connection object
        #con = sqlite3.connect(self.database_name)
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(query)
            #get results
            rows = cur.fetchall()
            if len(rows) == 0:
                return None
                
            users = []
            for row in rows:
                users.append(UserModel.create(row))
            return users
    
    def contains_user(self, user_nickname):
        '''
        Returns true if the user is in the database. False otherwise
        '''
        return self.get_user(user_nickname) is not None    
    
    #TABLATURE
    def get_songs(self, artist_id):
        '''
        Return list of songs by artist.
        If artist parameter is left empty return all songs.
        Return "None" if artist or songs not found.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        if artist_id == '':
            query = 'SELECT DISTINCT artist_id, song_id FROM tablatures'
        else:
            query = 'SELECT DISTINCT artist_id, song_id FROM tablatures WHERE artist_id = ?'
            pvalue = (artist_id,)
        
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            if artist_id == '':
                cur.execute(query)
            else:
                cur.execute(query, pvalue)
            #get results
            rows = cur.fetchall()
            if rows == []:
                return None
                
            songs = []
            for row in rows:
                songs.append([row[0],row[1]])
            return songs

        
    def get_artists(self):
        '''
        Return list of unique artists.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT DISTINCT artist_id FROM tablatures'
        
        #artist_id = None
        
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(query)
            #get results
            rows = cur.fetchall()
            if rows == []:
                return None
                
            artists = []
            for row in rows:
                artists.append(row[0])
            return artists
        
    def get_tablatures(self, artist_id, song_id):
        '''
        Return list of tablatures to specified song.
        If parameters are left empty return all tablatures.
        If song parameter is left empty return all tablatures by artist.
        Return "None" if song, artist or tablatures are not found.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        
        if song_id == '' and artist_id == '':
            query = 'SELECT * FROM tablatures'
        elif song_id == '':
            query = 'SELECT * FROM tablatures WHERE artist_id = ?'
            pvalue = (artist_id,)
        elif artist_id == '':
            query = 'SELECT * FROM tablatures WHERE song_id = ?'
            pvalue = (song_id,)
        else:
            query = 'SELECT * FROM tablatures WHERE artist_id = ? AND song_id = ?'
            pvalue = (artist_id, song_id,)
            
        #artist_id = None
        
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            if song_id == '' and artist_id == '':
                cur.execute(query)
            else:
                cur.execute(query, pvalue)
            #get results
            rows = cur.fetchall()
            if rows == []:
                return None
                
            tablatures = []
            for row in rows:
                tablatures.append(TablatureModel.create(row))
            return tablatures

    def get_tablature(self, tablature_id):
        '''
        Return a tablature.
        Return "None" if tablature was not found.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM tablatures WHERE tablature_id = ?'
        pvalue = (tablature_id,)
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
            return TablatureModel.create(row)
        
    def edit_tablature(self, tablature):
        '''
        Return tablature.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM tablatures WHERE tablature_id = ?'
        pvalue = (tablature.tablature_id,)
        
        #tablature_id = None
        
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
                stmnt = 'UPDATE tablatures SET body = ?, artist_id = ?, song_id = ? WHERE tablature_id = ?'
                pvalue = (tablature.body or row["body"],tablature.artist_id or row["artist_id"],tablature.song_id or row["song_id"], tablature.tablature_id)
                cur.execute(stmnt,pvalue)
                
                return tablature.tablature_id
        
    def delete_tablature(self, tablature_id):
        '''
        Delete tablature.
        '''
    
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM tablatures WHERE tablature_id = ?'
        pvalue = (tablature_id,)
        
        #tablature_id = None
        
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
                stmnt = 'DELETE FROM tablatures WHERE tablature_id = ?'
                pvalue = (tablature_id,)
                #execute the statement
                cur.execute(stmnt, pvalue)
                
                return tablature_id
        
    def add_tablature(self, tablature):
        '''
        Add tablature to database.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'INSERT INTO tablatures(body,tablature_id,rating,artist_id,song_id,user_nickname,rating_count) VALUES(?,?,?,?,?,?,?)'
        pvalue = (tablature.body,None,0,tablature.artist_id,tablature.song_id,tablature.user_nickname,0)
        
        #tablature_id = None
        if not self.contains_user(tablature.user_nickname):
            return None
        
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(query, pvalue)
            lrowid = cur.lastrowid
            return lrowid
        
    def get_rating(self, tablature_id):
        '''
        Returns current rating for the tablature.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT rating, rating_count FROM tablatures WHERE tablature_id = ?'
        pvalue = (tablature_id,)
        
        #tablature_id = None
        
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
            return row[0], row[1]
        
    def add_rating(self, tablature_id, rating):
        '''
        Calculate new rating.
        Returns "None" if tablature doesn't exist.
        '''
            
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT rating, rating_count FROM tablatures WHERE tablature_id = ?'
        pvalue = (tablature_id,)        
        
        #tablature_id = None
        
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
                stmnt = 'UPDATE tablatures SET rating = ?, rating_count = ? WHERE tablature_id = ?'
                pvalue = (rating + row[0], row[1] + 1, tablature_id)
                cur.execute(stmnt,pvalue)
                
                return rating + row[0], row[1] + 1
    
    def contains_tablature(self, tablature_id):
        '''
        Returns true if the tablature is in the database. False otherwise
        '''
        return self.get_tablature(tablature_id) is not None        
   
    #COMMENT
    def get_comment(self, comment_id):
        '''
        Returns the comment.
        If comment doesn't exist return "None".
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM comments WHERE comment_id = ?'
        pvalue = (comment_id,)
        
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
                #print row.keys()
                
                return CommentModel.create(row)
        
    def modify_comment(self, comment):
        '''
        Changes the comment in database to modified version.
        If comment doesn't exist return "None".
        If user is not the original poster, return "unauthorized" error.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM comments WHERE comment_id = ?'
        pvalue = (comment.comment_id,)
              
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
                stmnt = 'UPDATE comments SET body = ? WHERE comment_id = ?'
                pvalue = (comment.body or row["body"], comment.comment_id)
                cur.execute(stmnt,pvalue)
                
                return comment.comment_id
        
    def delete_comment(self, comment_id):
        '''
        Deletes comment.
        If comment doesn't exist return "None".
        If user is not the original poster, return "unauthorized" error.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM comments WHERE comment_id = ?'
        pvalue = (comment_id,)
        
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
                stmnt = 'DELETE FROM comments WHERE comment_id = ?'
                pvalue = (comment_id,)
                #execute the statement
                cur.execute(stmnt, pvalue)
                
                return comment_id
        
    def add_comment(self, comment):
        '''
        Adds comment to table.
        Return "unauthorized" if user is not logged in.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        if comment.reply_to != "":
            query = 'INSERT INTO comments(comment_id,body,tablature_id,user_nickname,reply_to) VALUES(?,?,?,?,?)'
            pvalue = (None,comment.body,comment.tablature_id,comment.user_nickname,comment.reply_to)
        else:
            query = 'INSERT INTO comments(comment_id,body,tablature_id,user_nickname,reply_to) VALUES(?,?,?,?,?)'
            pvalue = (None,comment.body,comment.tablature_id,comment.user_nickname,None)
        
        if not self.contains_user(comment.user_nickname):
            return None
        if not self.contains_tablature(comment.tablature_id):
            return None
        
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(query, pvalue)
            lid = cur.lastrowid
            return lid 
        
    def append_answer(self, comment):
        '''
        Writes an answer to the comment with id=comment_id
        returns the id of the new comment
        '''

        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT user_nickname from users WHERE user_nickname = ?'
        pvalue = (comment.user_nickname,)
        if not self.contains_comment(comment.reply_to):
            return None
        if not self.contains_user(comment.user_nickname):
            return None
        #user_id = None
        stmnt = 'INSERT INTO comments (body, user_nickname, reply_to) VALUES(?,?,?)'
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(query,pvalue)
            #just one result possible
            row = cur.fetchone()
            if row != None:
                comment.user_nickname = row["user_nickname"]
            pvalue = (comment.body,comment.user_nickname, comment.comment_id)
            #execute the statement
            cur.execute(stmnt,pvalue)
            lid = cur.lastrowid
            return lid if comment_id is not None else None    
    
    def contains_comment(self, comment_id):
        '''
        Returns true if the message is in the database. False otherwise.
        '''
        return self.get_comment(comment_id) is not None
        
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

    stmnt = 'CREATE TABLE "users" ("user_nickname" TEXT PRIMARY KEY  NOT NULL  UNIQUE , "email" TEXT, "picture" TEXT, "description" )'

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

    stmnt = 'CREATE TABLE "comments" ("comment_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "body" TEXT, "tablature_id" INTEGER REFERENCES tablatures ON DELETE CASCADE, "user_nickname" TEXT REFERENCES users ON DELETE CASCADE, "reply_to" INTEGER REFERENCES comments ON DELETE CASCADE )'
    
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
    
def drop_tables(database_name = 'debug.db'):

    keys_on = 'PRAGMA foreign_keys = ON'
    
    #connects (and creates if necessary) to the database. gets a connection object
    con = sqlite3.connect(database_name)
    with con:
        cur = con.cursor() 
        cur.execute(keys_on)
        
        cur.execute('DROP TABLE comments')
        cur.execute('DROP TABLE tablatures')
        cur.execute('DROP TABLE users')
        
        

def get_database(database_name = 'archive.db'):    
    return ArchiveDatabase(database_name)
    
database = ArchiveDatabase()
if (sys.argv[0] == "db_unittest.py"):
    database = ArchiveDatabase('debug.db')
elif (sys.argv[1] == "test"):
    database = ArchiveDatabase('debug.db')
else:
    database = ArchiveDatabase()
#print sys.argv
#print len(sys.argv)
#create_users_table("Test_archive.db")
#create_tablatures_table("Test_archive.db")
#create_comments_table("Test_archive.db")
#drop_tables("Test_archive.db")