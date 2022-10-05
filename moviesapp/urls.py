from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('userpage', views.userpage, name='userpage'),
    path('createlist', views.createlist, name='createlist'),
    path('populatelist', views.populatelist, name='populatelist'),
    path('addmovietolist', views.addmovietolist, name='addmovietolist'),
    path('removemoviefromlist', views.removemoviefromlist, name='removemoviefromlist'),
    re_path('movielist=', views.consultlist, name='consultlist'),
    path('listsaved', views.savelist, name='savelist'),
    path('deletelist', views.deletelist, name='deletelist'),
    path('logout/', views.logout, name='logout'),
]
