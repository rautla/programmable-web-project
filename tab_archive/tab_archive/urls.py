# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from archive.resources import Users, User, Artists, Artist, Song, Songs, Comment, Rating, Tablature, Tablatures, UserComments, UserTablatures, TablatureComments, Login
import re
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^tab_archive/users$',Users.as_view(), name="users"),
    
    url(r'^tab_archive/users/(?P<user_nickname>[\w\s]+)$', User.as_view(), name="user"),
    url(r'^tab_archive/users/(?P<user_nickname>[\w\s]+)/comments$', UserComments.as_view(), name="user_comments"),
    url(r'^tab_archive/users/(?P<user_nickname>[\w\s]+)/tablatures$', UserTablatures.as_view(), name="user_tablatures"),
    url(r'^tab_archive/artists$',Artists.as_view(), name="artists"),
    url(r'^tab_archive/artists/(?P<artist_id>[\w\s]+)$', Artist.as_view(),name="artist"),
    url(r'^tab_archive/songs$',Songs.as_view(), name="songs"),
    url(r'^tab_archive/artists/(?P<artist_id>[\w\s]+)/(?P<song_id>[\w\s]+)$', Song.as_view(),name="song"),
    url(r'^tab_archive/tablatures$',Tablatures.as_view(), name="tablatures"),
    url(r'^tab_archive/tablatures/(?P<tablature_id>\d+)$', Tablature.as_view(),name="tablature"),
    url(r'^tab_archive/tablatures/(?P<tablature_id>\d+)/rating$', Rating.as_view(),name="rating"),
    url(r'^tab_archive/tablatures/(?P<tablature_id>\d+)/comments$', TablatureComments.as_view(),name="tablaturecomments"),
    url(r'^tab_archive/tablatures/(?P<tablature_id>\d+)/(?P<comment_id>\d+)$', Comment.as_view(),name="comment"),
    url(r'^tab_archive/login$',Login.as_view(), name="login"), 
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

# Default login/logout views
urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)