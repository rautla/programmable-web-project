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
        
    #COMMENT
    def get_comment(self, comment_id):
    
        raise NotImplementedError("")
        
    def modify_comment(self, comment_id):
        
        raise NotImplementedError("")
        
    def delete_comment(self, comment_id):
    
        raise NotImplementedError("")
        
    def add_comment