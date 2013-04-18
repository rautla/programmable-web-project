import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse

from archive.database import database
from archive.models import UserModel, TablatureModel, CommentModel, ErrorModel



class User(APIView):
    def get (self, request, user_nickname): 
        authorization = ''  
        try:
            authorization = request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            pass
        if self._isauthorized(user_nickname, authorization):
            return self._readauthorized(request, user_nickname) 
        else:
            return self._readunathorized(request, user_nickname) 
    
    def delete(self, request, user_nickname):
        authorization = ''
        try:
            authorization = request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            pass
        if self._isauthorized(user_nickname, authorization):
            return self._deleteauthorized(request, user_nickname) 
        else:
            return Response(status = 401) 
    
    def put(self, request, user_nickname):
        authorization = ''
        try:
            authorization = request.META["HTTP_AUTHORIZATION"]
        except KeyError:
            pass
        if self._isauthorized(user_nickname, authorization):
            return self._updateuser(request, user_nickname) 
        else:
            return self._createuser(request, user_nickname)
    
        #Use the database to extract a user information. Use the method 
        #database.getUser(user_id) to obtain a UserModel
        usermodel = database.get_user(user_nickname)
        #If the database returns None return 404 not Found
        if usermodel is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #Get the url of the users resource
        uritousers = reverse("users", request=request)
        
        #Create the response body output. The output is a dictionary with the 
        #format provided in the method description
        output = {}
        #Create the dictionaries for publicProfile, history and users. To avoid
        #problems transform the registrationdata and description in string using the str() function
        publicprofile = {'user_nickname':usermodel.user_nickname,
                       'picture':usermodel.picture,
                       'description':str(usermodel.description)}
        users = {'rel':'self', 'href':uritousers}
        #Append to the output
        output['publicprofile'] = publicprofile
        output['users'] = users
        return Response(output, status=status.HTTP_200_OK)
    
    def _readauthorized(self, request, user_nickname):
        usermodel = database.get_user(user_nickname)
        if usermodel is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #Get the url of the users resource
        uritousers = reverse("users", request=request)
        #Get the url of this user history resource
        #Create the response body output. The output is a dictionary with the 
        #format provided in the method description
        output = {}
        #Create the dictionaries for userProfile, history and users
        users = {'rel':'self', 'href':uritousers}
        output['userprofile'] = usermodel.serialize()
        output['users'] = users
        return Response(output, status=status.HTTP_200_OK)
        
    def _deleteauthorized(self, request, user_nickname):
        if database.delete_user(user_nickname) is not None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            error = ErrorModel("The user "+ user_nickname+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
    
    def _updateuser(self, request, user_nickname):
        usermodel = UserModel(user_nickname)
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
    
    def _createuser(self, request, user_id):
        if database.contains_user(user_nickname):
            return Response(status=status.HTTP_409_CONFLICT)
        usermodel = None
        try:
            usermodel = UserModel(user_nickname, raw_data=request.DATA)
        except Exception as e:
            print "Could not add the data "+ str(e)
            traceback.print_exc()
            return Response(status = 400)
        database.add_user(usermodel)
        url = reverse("user", (user_nickname,), request=request)
        return Response(status=status.HTTP_204_NO_CONTENT,
                        headers={"Location":url})
    
    def _isauthorized(self, user_nickname, authorization): 
        if authorization is not None and (authorization.lower() == "admin" or 
                                          authorization.lower() == user_nickname.lower()):
            return True
        return False
    
class Users(APIView):
    def get (self, request):
        #Get in an array the models of all the users
        usermodels = database.get_users()
        #Users output looks: 
        #[{'nickname':user_nickname, 'link':{'rel':'self','href'=:'http://tab_archive/users/user_nickname'}},
        #{{'nickname':user_nickname, 'link':{'rel':'self','href'=:'http://tab_archive/users/user_nickname'}}]
        users = []
        for usermodel in usermodels:
            _usernickname = usermodel.user_nickname
            _userurl = "http://localhost:8000/tab_archive/users/"+_usernickname
            _userurl = reverse("user", (_usernickname,), request=request)
            user = {}
            user['user_nickname'] = _usernickname
            user['link'] = {'rel':'self', 'href':_userurl}
            users.append(user)
        
        response = Response(users, status=status.HTTP_200_OK)
        return response
    
class Artist(APIView):
    '''HUOM HOX MITES TÄMÄ (get_tablatures ilman song_id:tä???) TÄTÄ EI LÖYDY MUUALTA KUIN DOKKARISTA'''
    def get (self, request, artist_id):
        #Get in an array the models of all the tablatures from songs of artist
        tablaturemodels = database.get_tablatures(artist_id,'')

        #Serialize each one of the tablatures. An array of tablatures looks like:
        #[{'title':'message_title, 'link':{'rel':'self','href'=:'http://tab_archive/tablatures/tablature_id'}},
        #{'title':'message_title, 'link':{'rel':'self','href'=:'http://tab_archive/tablatures/tablature_id'}}]
        tablatures = []
        for tablaturemodel in tablaturemodels: 
            _tablatureid = tablaturemodel.tablature_id
            _tablatureurl = "http://localhost:8000/tab_archive/tablatures/"+_tablatureid
            _tablatureurl = reverse("tablature", (_tablatureid,), request=request)
            tablature = {}
            tablature['link'] = {'rel':'self', 'href':_tablatureurl}
            tablatures.append(tablature)
        '''HUOM HOX RATING, COMMENTS JA UPLOADER???(kts. dokkari)'''
        return Response(tablatures, status=status.HTTP_200_OK)

class Artists(APIView):
    def get (self, request):
        #Get an array of all the artists
        artistsmodels = database.get_artists()
        #Artists output looks: 
        #[{'artist':artist_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id'}},
        #{{'artist':artist_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id'}}]
        artists = []
        for tablaturemodel in artistmodels:'''HUOM HOX MITES TÄMÄ'''
            _artistid = tablaturemodel.artist_id
            _artisturl = "http://localhost:8000/tab_archive/artists/"+_artist_id
            _artisturl = reverse("artist", (_artistid,), request=request)
            artist = {}
            artist['artist_id'] = _artistid
            artist['link'] = {'rel':'self', 'href':_artisturl}
            artists.append(artist)
        
        response = Response(artists, status=status.HTTP_200_OK)
        return response
    
class Song(APIView):
    def get(self, request, song_id):
        #Get in an array the models of all the tablatures
        tablaturemodels = database.get_tablatures('', song_id)

        #Serialize each one of the tablatures. An array of tablatures looks like:
        #[{'song':'song_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id/song_id'}},
        #{'song':'song_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id/song_id'}}]
        tablatures = []
        for tablaturemodel in tablaturemodels: 
            _tablatureid = tablaturemodel.tablature_id
            _tablatureurl = "http://localhost:8000/tab_archive/tablatures/"+_tablatureid
            _tablatureurl = reverse("tablature", (_tablatureid,), request=request)
            tablature = {}
            tablature['link'] = {'rel':'self', 'href':_tablatureurl}
            tablatures.append(tablature)
        '''HUOM HOX RATING, COMMENTS JA UPLOADER???(kts. dokkari)'''
        return Response(tablatures, status=status.HTTP_200_OK)    
    
    def post(self, request, tablature_id):
    '''HUOM HOX MITES TÄMÄ (tablatures->post??? add_tablature???)'''
        #request.DATA contains the request body already deserialized in
        #a python dictionary
        if not request.DATA:
            error = ErrorModel('The artist_id, song_id and the body of the tablature\
                               cannot be empty').serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        if not database.contains_tablature(tablature_id):
            error = ErrorModel("The tablature "+tablature_id+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        '''HUOM HOX MITES TUON tablature_id:n KANSSA'''
        if database.contains_tablature(tablature_id):
            return Response(status=status.HTTP_409_CONFLICT)
        tablaturemodel = None
        try:
            tablaturemodel = TablatureModel(tablature_id, raw_data=request.DATA)
        except Exception as e:
            print "Could not add the data "+ str(e)
            traceback.print_exc()
            return Response(status = 400)
        database.add_tablature(tablaturemodel)
        url = reverse("tablature", (tablature_id,), request=request)
        return Response(status=status.HTTP_204_NO_CONTENT,
                        headers={"Location":url})    

class Songs(APIView):
    def get (self, request):
        #Get in an array the models of all the songs
        songmodels = database.get_songs()
        #Users output looks: 
        #[{'song':song_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id/song_id'}},
        #{{'song':song_id, 'link':{'rel':'self','href'=:'http://tab_archive/artists/artist_id/song_id'}}]
        songs = []
        for tablaturemodel in songmodels:'''HUOM HOX MITES TÄMÄ VARMAAN EI MEE NÄIN'''
            _artistid = tablaturemodel.artist_id
            _songid = tablaturemodel.song_id
            _songurl = "http://localhost:8000/tab_archive/artists/%s/%s" %(_artistid ,_song_id)
            _songurl = reverse("user", (_songid,), request=request)
            song = {}
            song['song_id'] = _songid
            song['link'] = {'rel':'self', 'href':_songurl}
            songs.append(song)
        
        response = Response(songs, status=status.HTTP_200_OK)
        return response
    
class Comment(APIView):
    #GET return the comment which comment id is comment_id
    def get (self, request, comment_id):
        #Get the model
        commentmodel = database.get_comment(comment_id)
        if commentmodel is None:
            error = ErrorModel("The comment "+ comment_id+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        #Serialize and modify the result so the sender is linked to its url
        comment = commentmodel.serialize()
        print comment
        #Modify the sender so it includes the URL of the sender:
        #From sender:"Axel" => I create sender:{'nickname':'Axel','link':{'rel':'self','href'=:'http://tab_archive/users/Axel'}}
        #senderurl = "http://localhost:8000/tab_archive/users/"+comment['sender']
        if comment['user_nickname'] is not None:
            senderurl = reverse("user",(comment['user_nickname'],), request=request)
            comment['user_nickname'] = {'user_nickname':comment['user_nickname'], 
                                 'link':{'rel':'self','href':senderurl}}
        else:
            comment['user_nickname'] = "Anonymous"                                                     
        #If replyto exists, include the url of the reply comment
        replytocomment_url = None
        if 'reply_to' in comment:
            replytocomment_url = "http://localhost:8000/tab_archive/tablatures/" + comment[tablature_id] + "/" + comment[comment_id])
            replytocomment_url = reverse("comment", (comment['reply_to'],), 
                                         request=request)
            comment['reply_to'] = replytocomment_url
        return Response(comment, status=status.HTTP_200_OK)    
    
    def delete(self, request, comment_id):
       try:
            if database.delete_comment(comment_id):
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                error = ErrorModel("The comment "+comment_id+
                                   " is not in the archive").serialize()
                return Response(error, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            error = ErrorModel("The comment "+comment_id+
                                   " is not in the archive").serialize()
            return Response(error, status=status.HTTP_400_BAD_REQUEST)    
    
    def put(self, request, comment_id):
       #request.DATA contains the request body already deserialized in a
        #python dictionary
        if not request.DATA:
            error = ErrorModel('The the body of the comment\
                               cannot be empty').serialize()
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if not database.contains_comment(comment_id):
            error = ErrorModel("The comment "+ comment_id+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        #Deserialize and modify the data in the comment.
        try:
            body = request.DATA['body']
            database.modify_comment(comment_id, body)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)     
    
    def post(self, request, comment_id):
        #request.DATA contains the request body already deserialized in
        #a python dictionary
        if not request.DATA:
            error = ErrorModel('The body of the comment\
                               cannot be empty').serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        if not database.contains_comment(comment_id):
            error = ErrorModel("The comment "+comment_id+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        '''TÄMÄ EI OLE VALMIS'''
        commentmodel = None
        if database.contains_comment(comment_id):
            return Response(status=status.HTTP_409_CONFLICT)        
        try:
            commentmodel = CommentModel(comment_id, raw_data=request.DATA)
        except Exception as e:
            print "Could not add the data "+ str(e)
            traceback.print_exc()
            return Response(status = 400)
        usermodel.reply_to = '''KOMMENTTI JOHON VASTATAAN'''
        database.add_comment(commentmodel)
        url = reverse("comment", (comment_id,), request=request)
        return Response(status=status.HTTP_204_NO_CONTENT,
                        headers={"Location":url})
    

class Rating(APIView):
    '''HUOM HOX MITES TÄMÄ'''
    def get(self, request):
        ratingmodel = database.get_rating()
        if ratingmodel is None:
            return Response(status=status.HTTP_404_NOT_FOUND)        
        #Rating output looks: 
        #[{'rating':rating, 'link':{'rel':'self','href'=:'http://tab_archive/tablatures/tablature_id/rating'}}]
        rating[]
        _rating = tablaturemodel.rating
        _ratingurl = "http://localhost:8000/tab_archive/tablatures/" + tablature[tablature_id] + "/" + tablature[rating]
        _ratingurl = reverse("rating", (_rating,), request=request)
        rating = {}
        rating['rating'] = _rating
        rating['link'] = {'rel':'self', 'href':_ratingurl}
        
        response = Response(rating, status=status.HTTP_200_OK)
        return response    
    
    def put(self, request, tablature_id):
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
            '''TÄTÄ PITÄÄ EHKÄ MUOKATA mallina kts. ex2->message->put()'''
            tablature_id = tablature_id '''MITES TÄÄ'''
            rating = request.DATA['rating']
            ratingcount = rating_count '''MITES TÄÄ'''
            database.add_rating(tablature_id, rating, rating_count)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    

class Tablature(APIView):
    def get (self, request, tablature_id):
    '''HUOM HOX TÄTÄ EI LÖYDY MUUALTA KUIN DOKKARISTA'''
    #GET return the tablature which tablature id is tablature_id
        #Get the model
        tablaturemodel = database.get_tablature(tablature_id)
        if tablaturemodel is None:
            error = ErrorModel("The tablature "+ tablature_id+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        #Serialize and modify the result so the sender is linked to its url
        tablature = tablaturemodel.serialize()
        print tablature
        #Modify the sender so it includes the URL of the sender:
        #From sender:"Axel" => I create sender:{'user_nickname':'Axel','link':{'rel':'self','href'=:'http://tab_archive/users/Axel'}}
        #senderurl = "http://localhost:8000/tab_archive/users/"+tablature['user_nickname']
        if tablature['user_nickname'] is not None:
            senderurl = reverse("user_nickname",(talbature['user_nickname'],), request=request)
            tablature['user_nickname'] = {'user_nickname':tablature['user_nickname'], 
                                 'link':{'rel':'self','href':senderurl}}
        else:
            tablature['user_nickname'] = "Anonymous"
        return Response(tablature, status=status.HTTP_200_OK)    
    
    def delete(self, request, tablature_id):
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
        
        tablaturemodel = TablatureModel(tablature_id)
        if tablaturemodel is None:
            return Response(status = status.HTTP_404_NOT_FOUND)
        #request.DATA contains a dictionary with the entity body input.
        #Deserialize the data and modify the model
        try:
            #EXTRACT THE PRIVATE DATA
            body = request.DATA['body']
            artist_id = request.DATA['artist_id']
            song_id = request.DATA['song_id']
            #SET VALUES TO USER
            tablaturemodel.tablature_id = tablature_id
            tablaturemodel.body = body
            tablaturemodel.artist_id = artist_id
            tablaturemodel.song_id = song_id
        except Exception as e:
            print "Could not add the data "+ str(e)
            traceback.print_exc()
            return Response(status = 400)
        #Update the model to the database
        database.edit_tablature(tablaturemodel)
        url = reverse("tablature", (tablature_id,), request=request)
        return Response(status=status.HTTP_204_NO_CONTENT,
                        headers={"Location":url})    
    
    def post(self, request, comment_id):
        '''HUOM HOX MITES TÄMÄ'''
        if database.contains_comment(comment_id):
            return Response(status=status.HTTP_409_CONFLICT)
        commentmodel = None
        try:
            commentmodel = CommentModel(comment_id, raw_data=request.DATA)
        except Exception as e:
            print "Could not add the data "+ str(e)
            traceback.print_exc()
            return Response(status = 400)
        database.add_comment(commentmodel)
        url = reverse("comment", (comment_id,), request=request)
        return Response(status=status.HTTP_204_NO_CONTENT,
                        headers={"Location":url})      

class Tablatures(APIView):
    def get (self, request):
        #Get in an array the models of all the tablatures
        tablaturemodels = database.get_tablatures()

        #Serialize each one of the tablatures. An array of tablatures looks like:
        #[{'title':'message_title, 'link':{'rel':'self','href'=:'http://tab_archive/tablatures/tablature_id'}},
        #{'title':'message_title, 'link':{'rel':'self','href'=:'http://tab_archive/tablatures/tablature_id'}}]
        tablatures = []
        for tablaturemodel in tablaturemodels: 
            _tablatureid = tablaturemodel.tablature_id
            _tablatureurl = "http://localhost:8000/tab_archive/tablatures/"+_tablatureid
            _tablatureurl = reverse("tablature", (_tablatureid,), request=request)
            tablature = {}
            tablature['link'] = {'rel':'self', 'href':_tablatureurl}
            tablatures.append(tablature)
        '''HUOM HOX RATING, COMMENTS JA UPLOADER???(kts. dokkari)'''
        return Response(tablatures, status=status.HTTP_200_OK)
    
    def post(self, request, tablature_id):
    '''HUOM HOX TÄTÄ EI LÖYDY MUUALTA KUIN DOKKARISTA(sama kuin song post)'''
        #request.DATA contains the request body already deserialized in
        #a python dictionary
        if not request.DATA:
            error = ErrorModel('The artist_id, song_id and the body of the message\
                               cannot be empty').serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        if not database.contains_tablature(tablature_id):
            error = ErrorModel("The tablature "+tablature_id+
                               " is not in the archive").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
        
        '''HUOM HOX MITES TUON tablature_id:n KANSSA'''
        if database.contains_tablature(tablature_id):
            return Response(status=status.HTTP_409_CONFLICT)
        tablaturemodel = None
        try:
            tablaturemodel = TablatureModel(tablature_id, raw_data=request.DATA)
        except Exception as e:
            print "Could not add the data "+ str(e)
            traceback.print_exc()
            return Response(status = 400)
        database.add_tablature(tablaturemodel)
        url = reverse("tablature", (tablature_id,), request=request)
        return Response(status=status.HTTP_204_NO_CONTENT,
                        headers={"Location":url})