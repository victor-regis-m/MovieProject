from django.shortcuts import render, redirect, reverse
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Movie, List
import requests as re


def index(request):
    return render(request, 'htmls/index.html')


def userpage(request):
    user_lists = List.objects.filter(user=request.user)
    request.session['user_lists'] = list(map(lambda x: x.list_name, user_lists))
    return render(request, 'htmls/userpage.html')


@login_required
def createlist(request):
    if 'listname' in request.POST:
        listname = request.POST['listname']
        if listname in request.session['user_lists']:
            request.session['list_exists'] = True
            request.session['listname'] = listname
            return render(request, 'htmls/createlist.html')
        else:
            request.session['movielist'] = list()
            request.session['listname'] = listname
            return redirect('populatelist')
    return render(request, 'htmls/createlist.html')


@login_required
def populatelist(request):
    posted_info = request.POST
    if 'listname' in posted_info.keys():
        request.session['listname'] = posted_info['listname']
    moviename = posted_info['moviename'] if 'moviename' in posted_info.keys() else ''
    if len(moviename) > 0:
        # for now just using first page results, if needed can be expanded
        api_request = 'https://api.themoviedb.org/3/search/movie?api_key=' \
                      + settings.TMDB_API_KEY \
                      + '&language=en-US&query=' + moviename \
                      + '&page=1&include_adult=false '
        response = re.request('GET', api_request)
        request.session['query_list_response'] = response.json()['results']
    else:
        moviename = ''
        request.session['query_list_response'] = []
    request.session['moviename'] = moviename
    request.session['lastquery'] = request.session['moviename']
    request.session['lastresult'] = request.session['query_list_response']
    request.session['movielist'] = request.session['movielist']
    request.session['listname'] = request.session['listname']
    return render(request, 'htmls/populatelist.html')


@login_required
def addmovietolist(request):
    request.session['moviename'] = request.session['lastquery']
    request.session['query_list_response'] = request.session['lastresult']
    movielist = request.session['movielist']
    addedmovie = request.POST['addedmovie']
    if addedmovie not in movielist:
        movielist.append(addedmovie)
    request.session['movielist'] = movielist
    return redirect('populatelist')


@login_required
def removemoviefromlist(request):
    request.session['moviename'] = request.session['lastquery']
    request.session['query_list_response'] = request.session['lastresult']
    movielist = request.session['movielist']
    removedmovie = request.POST['removedmovie']
    if removedmovie in movielist:
        movielist.remove(removedmovie)
    request.session['movielist'] = movielist
    request.session['movielist'] = movielist
    return redirect('populatelist')


@login_required
def savelist(request):
    listname = request.session['listname']
    username = request.user
    new_list_entry = List(user=username, list_name=listname)
    new_list_entry.save()
    for movie in request.session['movielist']:
        new_movie_entry = Movie(user=username, movie_title=movie, list_name=listname)
        new_movie_entry.save()
    try:
        created_terms = \
            ['query_list_response', 'movielist', 'lastquery', 'listname',
             'lastresult', 'moviename', 'user_lists', 'movies']
        for name in created_terms:
            del request.session[name]
    except KeyError:
        pass
    return render(request, 'htmls/listsaved.html')


@login_required
def consultlist(request):
    listname = request.path.split("=")[1]
    request.session['movies'] = \
        list(map(lambda x: x.movie_title, Movie.objects.filter(user=request.user, list_name=listname)))
    request.session['listname'] = listname
    return render(request, 'htmls/listcontents.html')


@login_required
def deletelist(request):
    listname = request.POST['deletelist']
    Movie.objects.filter(user=request.user, list_name=listname).delete()
    List.objects.filter(user=request.user, list_name=listname).delete()
    return redirect('userpage')


@login_required
def logout(request):
    django_logout(request)
    domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    return_to = request.build_absolute_uri(reverse('index'))
    return redirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')
