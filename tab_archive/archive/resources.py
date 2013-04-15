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
        usermodel = database.get_user(user_id)
        #If the database returns None return 404 not Found
        if usermodel is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #Get the url of the users resource
        uritousers = reverse("users", request=request)
        #Get the url of this user history resource
        uritohistory = reverse("history", (user_id,), request=request)
        
        #Create the response body output. The output is a dictionary with the 
        #format provided in the method description
        output = {}
        #Create the dictionaries for publicProfile, history and users. To avoid
        #problems transform the registrationdata and description in string using the str() function
        publicprofile = {'nickname':usermodel.nickname,
                       'registrationdate':str(usermodel.reg_date),
                       'description':str(usermodel.description)}
        history = {'rel':'self', 'href':uritohistory}
        users = {'rel':'self', 'href':uritousers}
        #Append to the output
        output['publicprofile'] = publicprofile
        output['history'] = history
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
        
    def _deleteauthorized(self, request, user_id):
        if database.delete_user(user_id) is not None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            error = ErrorModel("The message "+ user_id+
                               " is not in the forum").serialize()
            return Response(error, status=status.HTTP_404_NOT_FOUND)
    
    def _updateuser(self, request, user_id):
        usermodel = UserModel(user_id)
        if usermodel is None:
            return Response(status = status.HTTP_404_NOT_FOUND)
        #request.DATA contains a dictionary with the entity body input.
        #Deserialize the data and modify the model
        try:
            #EXTRACT THE PRIVATE DATA
            firstname = request.DATA['firstname']
            lastname = request.DATA['lastname']
            age = request.DATA['age']
            gender = request.DATA['gender']
            residence = request.DATA['residence']
            email = request.DATA['email']
            website = request.DATA['website']
            description = request.DATA.get("description","")
            #SET VALUES TO USER
            usermodel.nickname = user_id
            usermodel.description = description
            usermodel.firstname = firstname
            usermodel.lastname = lastname
            usermodel.age = int(age)
            usermodel.gender = gender
            usermodel.residence = residence
            usermodel.email = email
            usermodel.website = website
        except Exception as e:
            print "Could not add the data "+ str(e)
            traceback.print_exc()
            return Response(status = 400)
        #Update the model to the database
        database.modify_user(usermodel)
        url = reverse("user", (user_id,), request=request)
        return Response(status=status.HTTP_204_NO_CONTENT,
                        headers={"Location":url})
    
    def _createuser(self, request, user_id):
        if database.contains_user(user_id):
            return Response(status=status.HTTP_409_CONFLICT)
        usermodel = None
        try:
            usermodel = UserModel(user_id, raw_data=request.DATA)
        except Exception as e:
            print "Could not add the data "+ str(e)
            traceback.print_exc()
            return Response(status = 400)
        database.append_user(usermodel)
        url = reverse("user", (user_id,), request=request)
        return Response(status=status.HTTP_204_NO_CONTENT,
                        headers={"Location":url})
    
    def _isauthorized(self, user_id, authorization): 
        if authorization is not None and (authorization.lower() == "admin" or 
                                          authorization.lower() == user_id.lower()):
            return True
        return False
    

class Users(APIView):
    def get (self, request):

        #Get in an array the models of all the messages
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
    def get():
    

class Artists(APIView):
    def get():
    

class Song(APIView):
    def get():
    
    def post():
    

class Songs(APIView):
    def get():
    

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
        #If replyto exists, include the url of the reply message
        replytocomment_url = None
        if 'reply_to' in comment:
            replytocomment_url = "http://localhost:8000/tab_archive/tablatures/%i/%i" %(comment[tablature_id],comment[comment_id])
            replytomessage_url = reverse("comment", (comment['reply_to'],), 
                                         request=request)
            comment['reply_to'] = replytocomment_url
        return Response(comment, status=status.HTTP_200_OK)    
    
    def delete():
    
    def put():
    
    def post():
    

class Rating(APIView):
    def get():
    
    def put():
    

class Tablature(APIView):
    def get():
    
    def delete():
    
    def put():
    
    def post():
    

class Tablatures(APIView):
    def get():
    def post():

