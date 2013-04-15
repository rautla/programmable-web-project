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
        Return "None" if user not found.
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
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
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(query)
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
        Return "None" if artist or songs not found.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        if artist == '':
            query = 'SELECT DISTINCT artist_id, song_id FROM tablatures'
        else:
            query = 'SELECT DISTINCT artist_id, song_id FROM tablatures WHERE artist_id = ?'
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
            if rows is None:
                return None
                
            artists = []
            for row in rows:
                artists.append(row)
            return artists
        
    def get_tablatures(self, artist, song):
        '''
        Return list of tablatures to specified song.
        If parameters are left empty return all tablatures.
        If song parameter is left empty return all tablatures by artist.
        Return "None" if song, artist or tablatures are not found.
        '''
        
        keys_on = 'PRAGMA foreign_keys = ON'
        
        if song_id == '' and artist_id == '':
            query = 'SELECT DISTINCT artist_id, song_id, tablature_id FROM tablatures'
        elif song_id == '':
            query = 'SELECT DISTINCT artist_id, song_id, tablature_id FROM tablatures WHERE artist_id = ?'
            pvalue = (artist,)
        elif artist_id == '':
            query = 'SELECT DISTINCT artist_id, song_id, tablature_id FROM tablatures WHERE song_id = ?'
            pvalue = (song,)
        else:
            query = 'SELECT DISTINCT artist_id, song_id, tablature_id FROM tablatures WHERE artist_id = ?, song_id = ?'
            pvalue = (artist,song,)
            
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
            if rows is None:
                return None
                
            tablatures = []
            for row in rows:
                tablatures.append(row)
            return tablatures
        
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
                pvalue = (tablature.body or row["body"],tablature.artist_id or row["artist_id"],tablature.song_id or row["song_id"])
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
        pvalue = (tablature.body,Null,0,tablature.artist_id,tablature.song_id,tablature.user_nickname,0)
        
        #tablature_id = None
        
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(query, pvalue)
            return tablature.tablature_id
        
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
            rows = cur.fetchall()
            if rows is None:
                return None           
            return rating,rating_count
        
    def add_rating(self, tablature_id, rating, rating_count):
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
                pvalue = (rating + row[rating],row[rating_count] + 1,)
                cur.execute(stmnt,pvalue)
                
                return rating, rating_count
        
   
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
                print row.keys()
                
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
                pvalue = (comment.body or row["body"])
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
        query = 'INSERT INTO comments(comment_id,body,tablature_id,user_nickname,reply_to) VALUES(?,?,?,?,?)'
        pvalue = (Null,comment.body,comment.tablature_id,comment.user_nickname,comment.reply_to)
        
        #connects (and creates if necessary) to the database. gets a connection object
        con = sqlite3.connect(self.database_name)
        with con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(keys_on)        
            #execute the statement
            cur.execute(query, pvalue)
            return comment.comment_id
        

        
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

    stmnt = 'CREATE TABLE "users" ("user_nickname" TEXT PRIMARY KEY  NOT NULL  UNIQUE , "email" TEXT, "picture" TEXT, "description" TEXT  ON DELETE CASCADE )'

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

    stmnt = 'CREATE TABLE "tablatures" ("body" TEXT, "tablature_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "rating" INTEGER, "artist_id" TEXT, "song_id" TEXT, "user_nickname" TEXT, "rating_count" INTEGER, FOREIGN KEY(user_nickname) REFERENCES users(user_nickname))'

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
    
def drop_tables(database_name = 'debug.db'):

    keys_on = 'PRAGMA foreign_keys = ON'
    
    #connects (and creates if necessary) to the database. gets a connection object
    con = sqlite3.connect(database_name)
    with con:
        cur = con.cursor() 
        cur.execute(keys_on)
        cur.execute('DROP TABLE users')
        cur.execute('DROP TABLE tablatures')
        cur.execute('DROP TABLE comments')
        
        

def get_database(database_name = 'archive.db'):    
    return ArchiveDatabase(database_name)
    
