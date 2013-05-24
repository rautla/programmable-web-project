# -*- coding: utf-8 -*-

import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from django.contrib.auth import authenticate, login, logout
from archive.database import database
from archive.models import UserModel, TablatureModel, CommentModel, ErrorModel
from django.contrib.auth.models import User as AuthUser

class User(APIView):
    '''
    User model.
    tab_archive/users/<user_nickname>
    '''
    
    def get (self, request, user_nickname):
        '''
        Get user information by user_nickname.
        Email address requires authorization.
        '''
        
        print request.user
        
        authorization = ''  
        try:
            authorization = request.user.username #request.META["HTTP_AUTHORIZATION"]
            
        except KeyError:
            pass
        if self._isauthorized(user_nickname, authorization):
            return self._readauthorized(request, user_nickname) 
        else:
            return self._readunauthorized(request, user_nickname) 
    
    def delete(self, request, user_nickname):
        '''
        Delete user by user_nickname.
        Requires authorization.
        Returns 401 on unauthorized.
        '''
        authorization = ''
        try:
            authorization = request.user.username #request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            pass
        if self._isauthorized(user_nickname, authorization):
            return self._deleteauthorized(request, user_nickname) 
        else:
            return Response(status = 401) 
    
    def put(self, request, user_nickname):
        '''
        Create or modify user.
        Modify requires authorization.
        '''
        print "     herpderp        "
        authorization = ''
        try:
            print " herp "   
            print "authorization = " + request.user.username
            authorization = request.user.username #request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            print " derp "
            print "keyerror"
            pass
        if self._isauthorized(user_nickname, authorization):
            return self._updateuser(request, user_nickname) 
        else:
            return self._createuser(request, user_nickname)
    
    def _readunauthorized(self, request, user_nickname):
        '''
        Unauthorized user can't see email address.
        Return 200 on success.
        Return 404 if user doesn't exist.
        '''
        #Use the database to extract a user information. Use the method 
        #database.get_user(user_nickname) to obtain a UserModel
        usermodel = database.get_user(user_nickname)
        #If the database returns None return 404 not Found
        if usermodel is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #Get the url of the users resource
        uritousers = reverse("users", request=request)
        
        #Create the response body output. 
        output = {}
        
        user = {'user_nickname':usermodel.user_nickname,
                       'picture':usermodel.picture,
                       'description':str(usermodel.description)}
        users = {'rel':'self', 'href':uritousers}
        output = {"users":users, "user":user}
        
        _commentsurl = reverse("user_comments", (user_nickname,), request=request)
        _tablaturesurl = reverse("user_tablatures", (user_nickname,), request=request)
        
        output['comments'] = {'rel':'self', 'href':_commentsurl}
        output['tablatures'] = {'rel':'self', 'href':_tablaturesurl}
        
        return Response(output, status=status.HTTP_200_OK)
    
    def _readauthorized(self, request, user_nickname):
        '''
        Authorized user or admin can see email.
        Return 200 on success.
        '''
        usermodel = database.get_user(user_nickname)
        
        if usermodel is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #Get the url of the users resource
        uritousers = reverse("users", request=request)
        #Get the url of this user history resource
        #Create the response body output. 
        output = {}

        users = {'rel':'self', 'href':uritousers}
        output['user'] = usermodel.serialize()
        output['users'] = users
        _commentsurl = reverse("user_comments", (user_nickname,), request=request)
        _tablaturesurl = reverse("user_tablatures", (user_nickname,), request=request)
        
        output['comments'] = {'rel':'self', 'href':_commentsurl}
        output['tablatures'] = {'rel':'self', 'href':_tablaturesurl}
       
            
        return Response(output, status=status.HTTP_200_OK)
        
    def _deleteauthorized(self, request, user_nickname):
        '''
        Authorized user can delete user if exists.
        Return 404 if user doesn't exist.
        Return 204 on success.
        '''
        if database.delete_user(user_nickname) is not None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            error = ErrorModel("The user "+ user_nickname+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
    
    def _updateuser(self, request, user_nickname):
        '''
        Edit user.
        Return 400 if request is invalid.
        Return 204 on success.
        '''
        try:
            usermodel = UserModel(user_nickname)
        except Exception as e:
            print "Could not add the data "+ str(e)
            traceback.print_exc()
            return Response(status = 400)
        if usermodel is None:
            return Response(status = status.HTTP_404_NOT_FOUND)
        #request.DATA contains a dictionary with the entity body input.
        #Deserialize the data and modify the model
        try:
            #EXTRACT THE PRIVATE DATA

            email = request.DATA['email']
            description = request.DATA.get("description","")
            #SET VALUES TO USER
            usermodel.nickname = user_nickname
            usermodel.description = description
            usermodel.email = email
        except Exception as e:
            print "Could not add the data "+ str(e)
            traceback.print_exc()
            return Response(status = 400)
        #Update the model to the database
        database.edit_user(usermodel)
        url = reverse("user", (user_nickname,), request=request)
        return Response(status=status.HTTP_204_NO_CONTENT,
                        headers={"Location":url})
    
    def _createuser(self, request, user_nickname):
        '''
        Create new user.
        Return 400 on bad request.
        Return 204 on success.
        '''
        if database.contains_user(user_nickname):
            return Response(status=status.HTTP_409_CONFLICT)
        usermodel = None
        try:
            usermodel = UserModel(user_nickname, raw_data=request.DATA)
        except Exception as e:
            print "Could not add the data "+ str(e)
            traceback.print_exc()
            return Response(status=status.HTTP_400_BAD_REQUEST)
        database.add_user(usermodel)
        user = AuthUser.objects.create_user(usermodel.user_nickname, usermodel.email, request.DATA.get('password', None))
        user.save()
        url = reverse("user", (user_nickname,), request=request)
        return Response(status=status.HTTP_204_NO_CONTENT,
                        headers={"Location":url})
    
    def _isauthorized(self, user_nickname, authorization): 
        '''
        Check if user is authorized.
        '''
        if authorization is not None and (authorization.lower() == "admin" or 
                                          authorization.lower() == user_nickname.lower()):
            return True
        return False
    
class Users(APIView):
    '''
    List of users.
    '''
    
    def get (self, request):
        '''
        Return list of users.
        Return 200.
        '''
        #Get in an array the models of all the users
        usermodels = database.get_users()
        if usermodels == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        #Users output looks: 
        #[{'nickname':user_nickname, 'link':{'rel':'self','href'=:'http://tab_archive/users/user_nickname'}},
        #{{'nickname':user_nickname, 'link':{'rel':'self','href'=:'http://tab_archive/users/user_nickname'}}]
        users = {}
        userlist = []
        for usermodel in usermodels:
            _usernickname = usermodel.user_nickname
            _userurl = "http://localhost:8000/tab_archive/users/"+_usernickname
            _userurl = reverse("user", (_usernickname,), request=request)
            user = {}
            user['user_nickname'] = _usernickname
            user['link'] = {'rel':'self', 'href':_userurl}
            userlist.append(user)
        
        response = Response(userlist, status=status.HTTP_200_OK)
        return response
    

class TablatureComments(APIView):
    '''
    NOT IMPLEMENTED YET!
    '''
    def get(self, request, tablature_id):
    
        pass
    
    
class UserComments(APIView):
    '''
    NOT IMPLEMENTED YET!
    '''
    def get(self, request, user_nickname):
    
        pass
     #commentsmodel = database.get_comments_by_user(user_nickname)
        #if commentsmodel != None:
        #    for comment in commentsmodel:
        #        comment_info = {"artist_id":comment.artist_id, "song_id":comment.song_id, "tablature_id":comment.tablature_id}
        #        
        #        commenturl = reverse("comment", (comment.comment_id,), request=request)
        #        
        #        comment_info['link'] = {'rel':'self', 'href':commenturl}
        #       
        #        comments.append(comment_info)
        #    output['comments'] = comments
    
    
    
class UserTablatures(APIView):
    '''
    NOT IMPLEMENTED YET!
    '''
    def get(self, request, user_nickname):
    
        pass
    
class Artist(APIView):
    '''
    One artist.
    '''

    def get (self, request, artist_id):
        '''
        Get songs by artist.
        '''
        #Get in an array the models of all the tablatures from songs of artist
        songmodels = database.get_songs(artist_id, None)
        if songmodels == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        #Serialize each one of the tablatures. An array of tablatures looks like:
        #[{'song_id':song_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id/song_id'}},
        #{'song_id':song_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id/song_id'}}]
        songs = []
        for songmodel in songmodels: 
            _artistid = songmodel[0]
            _songid = songmodel[1]
            _songurl = "http://localhost:8000/tab_archive/artists/"+_artistid + "/" +_songid
            _songurl = reverse("song", (_artistid,_songid), request=request)        
            song = {}
            song['song_id'] = _songid
            song['link'] = {'rel':'self', 'href':_songurl}
            songs.append(song)
        
        response = Response(songs, status=status.HTTP_200_OK)
        return response

class Artists(APIView):
    '''
    List of artists.
    '''

    def get(self, request):
        '''
        Get list of artists.
        Return 200.
        '''
    
        #Get an array of all artists
        artistmodels = database.get_artists(None)
        #Artists output looks: 
        #[{'artist':artist_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id'}},
        #{{'artist':artist_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id'}}]
        if artistmodels == None:        
            return Response(status=status.HTTP_404_NOT_FOUND)
        artists = []
        for artistmodel in artistmodels:
            _artistid = artistmodel
            _artisturl = "http://localhost:8000/tab_archive/artists/"+_artistid
            _artisturl = reverse("artist",(_artistid,), request=request)
            artist = {}
            artist['artist_id'] = _artistid
            artist['link'] = {'rel':'self', 'href':_artisturl}
            artists.append(artist)
            
        response = Response(artists, status=status.HTTP_200_OK)
        return response
        
    def post(self, request):
        '''
        Get list of artists containing keyword in the artist_id.
        Return 200.
        '''
    
        #Get an array of all artists
        artistmodels = database.get_artists(request.DATA["keyword"])
        #Artists output looks: 
        #[{'artist':artist_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id'}},
        #{{'artist':artist_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id'}}]
        if artistmodels == None:        
            return Response(status=status.HTTP_404_NOT_FOUND)
        artists = []
        for artistmodel in artistmodels:
            _artistid = artistmodel
            _artisturl = "http://localhost:8000/tab_archive/artists/"+_artistid
            _artisturl = reverse("artist",(_artistid,), request=request)
            artist = {}
            artist['artist_id'] = _artistid
            artist['link'] = {'rel':'self', 'href':_artisturl}
            artists.append(artist)
            
        response = Response(artists, status=status.HTTP_200_OK)
        return response
    
class Song(APIView):
    '''
    Song contains tablatures made to represent it.
    '''
    
    def get(self, request, artist_id, song_id):
        '''
        Get list of tablatures by artist and song ids.
        Returns 200.
        '''
        
        #Get in an array the models of all the tablatures
        tablaturemodels = database.get_tablatures(artist_id, song_id)
        if tablaturemodels == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        #Serialize each one of the tablatures. An array of tablatures looks like:
        #[{'song':'song_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id/song_id'}},
        #{'song':'song_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id/song_id'}}]
        song = {}
        song["artist_id"] = artist_id
        song["song_id"] = song_id
        tablatures = []
        for tablaturemodel in tablaturemodels: 
            _tablatureid = tablaturemodel.tablature_id
            _rating = tablaturemodel.rating
            _tablatureurl = "http://localhost:8000/tab_archive/tablatures/"+str(_tablatureid)
            _tablatureurl = reverse("tablature", (_tablatureid,), request=request)
            tablature = {}
            tablature['tablature_id'] = _tablatureid
            tablature['rating'] = _rating
            tablature['link'] = {'rel':'self', 'href':_tablatureurl}
            tablatures.append(tablature)
        song["tablatures"] = tablatures
        response = Response(song, status=status.HTTP_200_OK)  
        return response
        
    def post(self, request, artist_id, song_id):
        '''
        Add a new tablature.
        Returns 400 on bad request.
        Returns 401 on unauthorized user.
        Returns 201 on successful creation.
        '''
        if not request.DATA:
            error = ErrorModel('The artist_id, song_id and the body of the tablature\
                               cannot be empty').serialize()
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        tablaturemodel = None
        try:
            if not request.DATA.has_key("artist_id"):
                request.DATA["artist_id"] = artist_id
            if not request.DATA.has_key("song_id"):
                request.DATA["song_id"] = song_id
            tablaturemodel = TablatureModel(None, raw_data=request.DATA)
            user_nickname = tablaturemodel.user_nickname
        except Exception as e:
            print "Could not add the data " + str(e)
            traceback.print_exc()
            return Response(status = 400)
        
        authorization = ''
        try:
            authorization = request.user.username #request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            pass
        if self._isauthorized(user_nickname, authorization):
            return self._createtablature(tablaturemodel, request) 
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def _createtablature(self, tablaturemodel, request):
        '''
        Creates tablature.
        '''
        tablature_id = database.add_tablature(tablaturemodel)
        url = reverse("tablature", (tablature_id,), request=request)
        return Response(status=status.HTTP_201_CREATED,
                        headers={"Location":url})    
    
    def _isauthorized(self, user_nickname, authorization): 
        '''
        Check that user is authorized.
        '''
        if authorization is not None and (authorization.lower() == "admin" or 
                                          authorization.lower() == user_nickname.lower()):
            return True
        return False

class Songs(APIView):
    '''
    List of songs.
    Returns 200.
    '''
    def get (self, request):
        #Get in an array the models of all the songs
        songmodels = database.get_songs("", None)
        if songmodels == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        #Users output looks: 
        #[{'song':song_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id/song_id'}},
        #{{'song':song_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id/song_id'}}]
        songs = {}
        songlist = []
        for songmodel in songmodels:
            _artistid = songmodel[0]
            _songid = songmodel[1]
            _songurl = "http://localhost:8000/tab_archive/artists/%s/%s" %(_artistid ,_songid)
            _songurl = reverse("song", (_artistid, _songid,), request=request)
            song = {"song":{}, "artist":{}}
            song["song"]['song_id'] = _songid
            song["artist"]['artist_id'] = _artistid
            _artisturl = reverse("artist", (_artistid,), request=request)
            song["artist"]['link'] = {'rel':'self', 'href':_artisturl}
            song["song"]['link'] = {'rel':'self', 'href':_songurl}
            songlist.append(song)
        songs["songs"] = songlist
        response = Response(songlist, status=status.HTTP_200_OK)
        return response
        
        
    '''
    Find songs containing keyword in song_id.
    Returns 200.
    '''    
    def post (self, request):
        #Get in an array the models of all the songs
        songmodels = database.get_songs("", request.DATA["keyword"])
        if songmodels == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        
        #Users output looks: 
        #[{'song':song_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id/song_id'}},
        #{{'song':song_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id/song_id'}}]
        songs = {}
        songlist = []
        for songmodel in songmodels:
            _artistid = songmodel[0]
            _songid = songmodel[1]
            _songurl = "http://localhost:8000/tab_archive/artists/%s/%s" %(_artistid ,_songid)
            _songurl = reverse("song", (_artistid, _songid,), request=request)
            song = {"song":{}, "artist":{}}
            song["song"]['song_id'] = _songid
            song["artist"]['artist_id'] = _artistid
            _artisturl = reverse("artist", (_artistid,), request=request)
            song["artist"]['link'] = {'rel':'self', 'href':_artisturl}
            song["song"]['link'] = {'rel':'self', 'href':_songurl}
            songlist.append(song)
        songs["songs"] = songlist
        response = Response(songlist, status=status.HTTP_200_OK)
        return response
    
class Comment(APIView):
    '''
    Get, modify and reply to comments.
    '''
    #GET return the comment which comment id is comment_id
    def get (self, request, tablature_id, comment_id):
        '''
        Get comment.
        Return 404 if comment doesn't exist.
        Return 200 on success.
        '''
        #Get the model
        commentmodel = database.get_comment(comment_id)
        if commentmodel is None:
            error = ErrorModel("The comment "+ comment_id+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        #Serialize and modify the result so the sender is linked to its url
        comment = {}
        comment["comment"] = commentmodel.serialize()

        
        senderurl = reverse("user",(commentmodel.user_nickname,), request=request)
        comment['user'] = {'user_nickname':commentmodel.user_nickname, 'link':{'rel':'self','href':senderurl}}
                                                 
        #If replyto exists, include the url of the reply comment
        replytocomment_url = None

        if commentmodel.reply_to != "":

            replytocomment_url = reverse("comment", (commentmodel.tablature_id, commentmodel.reply_to), request=request)
            comment['reply_to'] = {'rel':'self','href':replytocomment_url }
        return Response(comment, status=status.HTTP_200_OK)    
    
    def delete(self, request, tablature_id, comment_id):
        '''
        Delete comment.
        Requires authorization.
        Returns 401 on authorized request.
        Returns 404 if comment doesn't exist.
        '''
        authorization = ''
        try:
            authorization = request.user.username #request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            pass
            
        if not database.contains_comment(comment_id):
            error = ErrorModel("The comment " + str(comment_id) + " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
            
        commentmodel = database.get_comment(comment_id)
        if self._modifyisauthorized(commentmodel, authorization):
            return self._deletecomment(commentmodel.comment_id, request) 
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def _deletecomment(self, comment_id, request):
        '''
        Performs deletion.
        Return 400 on bad request.
        Return 204 on success.
        '''
        
        try:
            if database.delete_comment(comment_id):
                return Response(None, status=status.HTTP_204_NO_CONTENT)
                
        except Exception:
            error = ErrorModel("The comment "+comment_id+
                                   " is not in the archive").serialize()
            return Response(error, status=status.HTTP_400_BAD_REQUEST)    
    
    def put(self, request, tablature_id, comment_id):
        '''
        Modify comment.
        Requires authorization.
        '''
        #request.DATA contains the request body already deserialized in a
        #python dictionary
        if not request.DATA:
            error = ErrorModel('The the body of the comment\
                               cannot be empty').serialize()
            print "HERP"
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if not database.contains_comment(comment_id):
            error = ErrorModel("The comment "+ comment_id+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        commentmodel = database.get_comment(comment_id)
        commentmodel.body = request.DATA["body"]
        authorization = ''
        try:
            authorization = request.user.username #request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            pass
        if self._modifyisauthorized(commentmodel, authorization):
            return self._modifycomment(commentmodel, request) 
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        
    def _modifycomment(self, comment, request):
        '''
        Performs actual modification.
        Called when authorization check is passed.
        Checks for bad request. (returns 400)
        '''
        #Deserialize and modify the data in the comment.
        try:
            database.modify_comment(comment)
        except Exception:
            print "derp"
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)     
    
    def post(self, request, tablature_id, comment_id):
        '''
        Post reply to an existing comment.
        '''
        #request.DATA contains the request body already deserialized in
        #a python dictionary
        if not request.DATA:
            error = ErrorModel('The body of the comment\
                               cannot be empty').serialize()
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if not database.contains_comment(comment_id):
            error = ErrorModel("The comment "+comment_id+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        commentmodel = None
        
        try:
            commentmodel = CommentModel('', raw_data=request.DATA)
        except Exception as e:
            print "Could not add the data "+ str(e)
            traceback.print_exc()
            return Response(status = 400)
        commentmodel.reply_to = comment_id 
        commentmodel.tablature_id = tablature_id
        
        authorization = ''
        try:
            authorization = request.user.username #request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            pass
        if self._isauthorized(commentmodel.user_nickname, authorization):
            return self._createreply(commentmodel, request) 
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def _createreply(self, commentmodel, request):
        '''
        Create reply comment.
        '''
        comment_id = database.add_comment(commentmodel)

        url = reverse("comment", (commentmodel.tablature_id, comment_id), request=request)
        return Response(status=status.HTTP_204_NO_CONTENT,
                        headers={"Location":url})
                        
    def _isauthorized(self, user_nickname, authorization):
        '''
        Check if user is allowed to post reply.
        '''
        if authorization is not None and (authorization.lower() == "admin" or 
                                          authorization.lower() == user_nickname.lower()):
            return True
        return False
        
    def _modifyisauthorized(self, comment, authorization): 
        '''
        Check if user is allowed to modify or delete comment.
        '''
        if authorization is not None and (authorization.lower() == "admin" or 
                                          authorization.lower() == comment.user_nickname.lower()):
            return True
        return False
    

class Rating(APIView):
    '''
    Get or modify rating.
    '''
    
    def get(self, request, tablature_id):
        '''
        Get rating of tablature.
        '''
        ratingmodel = database.get_rating(tablature_id)
        if ratingmodel is None:
            return Response(status=status.HTTP_404_NOT_FOUND)        
        
        
        
        rating = {}
        rating['rating'] = ratingmodel[0]
        rating['rating_count'] = ratingmodel[1]
        
        response = Response(rating, status=status.HTTP_200_OK)
        return response    
    
    def post(self, request, tablature_id):
        '''
        Give your own rating to a tablature.
        Rating is incremented by the value given and rating count is incremented by 1.
        '''
    
        #request.DATA contains the request body already deserialized in a
        #python dictionary
        if not request.DATA:
            error = ErrorModel('The artist_id, song_id and body of the tablature\
                               cannot be empty').serialize()
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if not database.contains_tablature(tablature_id):
            error = ErrorModel("The tablature "+ tablature_id+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        #Deserialize and modify the data in the tablature.
        try:
            tablature_id = tablature_id
            newrating = request.DATA['rating']
            rating = database.add_rating(tablature_id, newrating)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response((rating[0], rating[1]), status=status.HTTP_200_OK)
    

class Tablature(APIView):
    '''
    Post comment to tablature, get, modify or delete tablature.
    '''

    def get (self, request, tablature_id):
        '''
        Get tablature by id.
        Returns 404 if doesn't exist or 200 on success.
        '''
        #GET return the tablature which tablature id is tablature_id
        #Get the model
        tablaturemodel = database.get_tablature(tablature_id)
        if tablaturemodel is None:
            error = ErrorModel("The tablature "+ tablature_id+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        #Serialize and modify the result so the sender is linked to its url
        tablature = tablaturemodel.serialize()
        #print tablature
        #Modify the sender so it includes the URL of the sender:
        #From sender:"Axel" => I create sender:{'user_nickname':'Axel','link':{'rel':'self','href'=:'http://tab_archive/users/Axel'}}
        #senderurl = "http://localhost:8000/tab_archive/users/"+tablature['user_nickname']
        if tablature['user_nickname'] is not None:
            senderurl = reverse("user",(tablature['user_nickname'],), request=request)
            tablature['link'] = {'rel':'self','href':senderurl}
        commentsurl = reverse("tablaturecomments", (tablature_id,), request=request)
        tablature["comments"] = {'rel':'self','href':commentsurl}
        return Response(tablature, status=status.HTTP_200_OK)    
    
    def delete(self, request, tablature_id):
        '''
        Delete tablature.
        Requires authorization.
        If not authorized return 401.
        '''
        if not database.contains_tablature(tablature_id):
            
            error = ErrorModel("The tablature "+ tablature_id+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        authorization = ''
        try:
            authorization = request.user.username #request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            pass
        if self._modifyisauthorized(tablature_id, authorization):
            return self._deletetablature(tablature_id) 
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def _deletetablature(self, tablature_id):
        '''
        Perform deletion.
        Return 404 if tablature doesn't exist.
        Return 400 on bady request.
        On successful deletion return 204.
        '''
        try:
            if database.delete_tablature(tablature_id):
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                error = ErrorModel("The tablature "+tablature_id+
                                   " is not in the archive").serialize()
                return Response(error, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            error = ErrorModel("The tablature "+tablature_id+
                                   " is not in the archive").serialize()
            return Response(error, status=status.HTTP_400_BAD_REQUEST)    
    
    def put(self, request, tablature_id):
        '''
        Modify tablature.
        Requires authorization.
        '''
    
        #request.DATA contains the request body already deserialized in a
        #python dictionary

        if not request.DATA:
            
            error = ErrorModel('The artist_id, song_id and body of the tablature\
                               cannot be empty').serialize()
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if not database.contains_tablature(tablature_id):
            
            error = ErrorModel("The tablature "+ tablature_id+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        
        #request.DATA contains a dictionary with the entity body input.
        #Deserialize the data and modify the model
        tablaturemodel = TablatureModel(tablature_id)
        try:
            #EXTRACT THE PRIVATE DATA
            if request.DATA.has_key("body"):
                body = request.DATA['body']
            else:
                body = None
            if request.DATA.has_key("artist_id"):
                artist_id = request.DATA["artist_id"]
            else:
                artist_id = None
            if request.DATA.has_key("song_id"):
                song_id = request.DATA['song_id']
            else:
                song_id = None
            #SET VALUES TO USER
            tablaturemodel.tablature_id = tablature_id
            tablaturemodel.body = body
            tablaturemodel.artist_id = artist_id
            tablaturemodel.song_id = song_id
        except Exception as e:
            print "Could not add the data "+ str(e)
            traceback.print_exc()
            return Response(status = 400)
            
        authorization = ''
        try:
            authorization = request.user.username #request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            pass
        if self._modifyisauthorized(tablature_id, authorization):
            return self._modifytablature(tablaturemodel, request) 
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            
            
    def _modifytablature(self, tablaturemodel, request):
        '''
        Performs modification.
        '''
        
        #Update the model to the database
        database.edit_tablature(tablaturemodel)
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
    def post(self, request, tablature_id):
        '''
        Post a comment to tablature by id.
        Requires authorization.
        Returns 400 on bad request.
        '''
        if not request.DATA:
            error = ErrorModel('The artist_id, song_id and the body of the tablature\
                               cannot be empty').serialize()
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        
        if not database.contains_tablature(tablature_id):
            error = ErrorModel('Tablature was not found.').serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        commentmodel = None
        try:
            commentmodel = CommentModel(None, raw_data=request.DATA)
            user_nickname = commentmodel.user_nickname
            commentmodel.tablature_id = tablature_id
        except Exception as e:
            print "Could not add the data "+ str(e)
            traceback.print_exc()
            return Response(status = 400)
            
        authorization = ''
        try:
            authorization = request.user.username #request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            pass
        if self._isauthorized(user_nickname, authorization):
            return self._createcomment(commentmodel, request) 
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        
    def _createcomment(self, commentmodel, request):
        '''
        Performs creation.
        Returns 201.
        '''
        comment_id = database.add_comment(commentmodel)
        url = reverse("comment", (commentmodel.tablature_id,comment_id,), request=request)
        return Response(status=status.HTTP_201_CREATED,
                        headers={"Location":url})      
                        
    def _isauthorized(self, user_nickname, authorization): 
        '''
        Check that user is allowed to post comment.
        '''
        if authorization is not None and (authorization.lower() == "admin" or 
                                          authorization.lower() == user_nickname.lower()):
            return True
        return False
        
    def _modifyisauthorized(self, tablature_id, authorization): 
        '''
        Check that user is allowed to modify tablature.
        '''
        tablaturemodel = database.get_tablature(tablature_id)
        user_nickname = tablaturemodel.user_nickname
        if authorization is not None and (authorization.lower() == "admin" or 
                                          authorization.lower() == user_nickname.lower()):
            return True
        return False

class Tablatures(APIView):
    '''
    Get list of tablatures or post a new.
    '''
    
    def get (self, request):
        '''
        Get list of tablatures.
        Returns 200.
        '''
        #Get in an array the models of all the tablatures
        tablaturemodels = database.get_tablatures('', '')
        if tablaturemodels == None:
            error = ErrorModel('Tablatures were not found.').serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
            

        #Serialize each one of the tablatures. An array of tablatures looks like:
        #[{'title':'message_title, 'link':{'rel':'self','href'=:'http://tab_archive/tablatures/tablature_id'}},
        #{'title':'message_title, 'link':{'rel':'self','href'=:'http://tab_archive/tablatures/tablature_id'}}]
        songs = []
        for tablaturemodel in tablaturemodels: 
            song = {"artist":{}, "song":{}, "tablature":{}}
            _artisturl = reverse("artist", (tablaturemodel.artist_id,), request=request)
            _songurl = reverse("song", (tablaturemodel.artist_id, tablaturemodel.song_id,), request=request)
            song["artist"]["artist_id"] = tablaturemodel.artist_id
            song["artist"]["link"] = {'rel':'self', 'href':_artisturl}
            song["song"]["song_id"] = tablaturemodel.song_id
            song["song"]["link"] = {'rel':'self', 'href':_songurl}
            _tablatureid = tablaturemodel.tablature_id
            _tablatureurl = "http://localhost:8000/tab_archive/tablatures/"+str(_tablatureid)
            _tablatureurl = reverse("tablature", (_tablatureid,), request=request)
            tablature = {}
            tablature['tablature_id'] = _tablatureid
            tablature['rating'] = tablaturemodel.rating
            tablature['rating_count'] = tablaturemodel.rating_count
            tablature['link'] = {'rel':'self', 'href':_tablatureurl}
            tablature['user'] = {'user_nickname' : tablaturemodel.user_nickname}
            _userurl = reverse("user", (tablaturemodel.user_nickname,), request=request)
            tablature['user']['link'] = {'rel':'self', 'href':_userurl}
            song["tablature"] = tablature
            songs.append(song)
        return Response(songs, status=status.HTTP_200_OK)
    
    def post(self, request):
        '''
        Post a tablature.
        Requires authorized user.
        '''
        if not request.DATA:
            error = ErrorModel('The artist_id, song_id and the body of the tablature\
                               cannot be empty').serialize()
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        tablaturemodel = None
        try:
            tablaturemodel = TablatureModel(None, raw_data=request.DATA)
            user_nickname = tablaturemodel.user_nickname
        except Exception as e:
            print "Could not add the data " + str(e)
            traceback.print_exc()
            return Response(status = 400)
        
        authorization = ''
        try:
            authorization = request.user.username #request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            pass
        if self._isauthorized(user_nickname, authorization):
            return self._createtablature(tablaturemodel, request) 
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    def _createtablature(self, tablaturemodel, request):
        '''
        Performs creation.
        '''
        tablature_id = database.add_tablature(tablaturemodel)
        url = reverse("tablature", (tablature_id,), request=request)
        return Response(status=status.HTTP_201_CREATED,
                        headers={"Location":url})    
    
    def _isauthorized(self, user_nickname, authorization): 
        '''
        Checks that user is authorized.
        '''
        if authorization is not None and (authorization.lower() == "admin" or 
                                          authorization.lower() == user_nickname.lower()):
            return True
        return False
        
        
class Login(APIView):
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                print "Great success!"
                return Response(status = 204) 
            else:
                # Return a 'disabled account' error message
                print "This is an error message!"
                return Response(status = 403) 
        else:
            # Return an 'invalid login' error message.
            print "Invalid login!"
            return Response(status = 401) 
            
    def get(self, request):
        
        #return Response(status = 204)
        #print request["HTTP_USERNAME"]
        
        try:
            print request.META["HTTP_USERNAME"]
            print request.META["HTTP_PASSWORD"]
            username = request.META["HTTP_USERNAME"]
            password = request.META["HTTP_PASSWORD"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to a success page.
                    print "Great success!"
                    return Response(status = 204) 
                else:
                    # Return a 'disabled account' error message
                    print "This is an error message!"
                    return Response(status = 403) 
            else:
                # Return an 'invalid login' error message.
                print "Invalid login!"
                return Response(status = 401) 
        except KeyError:
            logout(request)
            return Response(status = 204)