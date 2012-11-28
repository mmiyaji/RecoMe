#!/usr/bin/env python
# encoding: utf-8
"""
content.py

Ccreated by mmiyaji on 2012-10-29.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
/"""
from views import *
from recommend import *
import re
from django.contrib.sessions.backends.db import SessionStore
if settings.MONGODB_USE:
    import pymongo
def home(request, genre_id = None, name = 'content'):
    """
    Case of GET REQUEST '/content/'
    画像の一覧を表示するページ
    """
    temp_values = Context()
    page=1
    span = 8
    order = "-created_at"
    conten = {}
    genre = '101266'
    genre_name = None
    count = 0
    user = None
    recommend = False
    if name == "recommend":
        recommend = True
    # セッションに初回アクセスを保存
    session = request.session
    if 'date' not in session:
        session['date'] = datetime.datetime.now()
        session.save()
    if request.GET.has_key('genre'):
        genre = request.GET['genre']
    if genre_id:
        genre = genre_id
    if settings.MONGODB_USE:
        start = 0
        genre_name = ""
        conn = pymongo.Connection(settings.MONGODB_PATH, settings.MONGODB_PORT)
        db = conn.rakuten
        usedb = db.booktree
        if request.GET.has_key('page'):
            page = int(request.GET['page'])
        if request.GET.has_key('span'):
            span = int(request.GET['span'])
        limit = span
        start = page * span
        # net = usedb.find(u'genre_tree',u'101266').sort('review_average', pymongo.DESCENDING).skip(start).limit(limit) .sort('review_average', pymongo.DESCENDING)
        if genre:
#            net = usedb.find({'rc':{'$exists':True} ,'genre_tree':genre, 'isimage':{'$ne':False}}).sort('rc', pymongo.DESCENDING).skip(start).limit(limit)
            if name == "recommend":
                recommend = True
                recom = Recom()
            netdb = usedb.find({'genre_tree':genre,
                              # 'isimage':{'$exists':True},
                              # 'image_code':200,
                              'im':True,
                              # 'words':{'$ne':'中古'},
                              }).sort('review_count', pymongo.DESCENDING)
            net = netdb.skip(start).limit(limit)
            count = netdb.count()
            genre_name = db.ichiba_genre.find({'id':genre})[0]["name"]
        else:
            net = usedb.find().sort('review_count', pymongo.ASCENDING).sort('review_average', pymongo.DESCENDING).skip(start).limit(limit)
        contents = net
    else:
        content = {
            "image_url":"/static/img/screenshot/miu.jpg",
            "name":"name",
            "id":"id",
            "price":"price",
            "description":"description",
            "ext_description":"ext_description",
            "url":"url",
            "review_count":"review_count",
            "review_average":"review_average",
            "shop_code":"shop_code",
            "genre_code":"genre_code",
            "registed_at":"registed_at",
            }
        contents = [content for i in range(0,span)]
    temp_values = {
        "target":name,
        "title":u"コンテンツ一覧ページ",
        "contents":contents,
        "genre_name":genre_name,
        "rakuten":True,
        "count":count,
        "session":session,
        }
    return render_to_response('content/index.html',temp_values,
                              context_instance=RequestContext(request))
def genre(request, genre_id = None):
    """
    Case of GET REQUEST '/content/genre/'
    ジャンルの一覧を表示するページ
    """
    temp_values = Context()
    page=1
    span = 8
    order = "-created_at"
    conten = {}
    parent_genre = '101266'
    genre_name = None
    count = 0
    user = None
    session = request.session
    if 'date' not in session:
        session['date'] = datetime.datetime.now()
        session.save()
    if genre_id:
        parent_genre = genre_id
    if settings.MONGODB_USE:
        start = 0
        genre_name = ""
        MONGODB_PATH = "127.0.0.1"
        # MONGODB_PATH = settings.MONGODB_PATH
        conn = pymongo.Connection(MONGODB_PATH, settings.MONGODB_PORT)
        db = conn.rakuten
        usedb = db.ichiba_genre
        netdb = usedb.find({'parent_id':parent_genre,
                            })#.sort('id', pymongo.DESCENDING)
        genre_name = usedb.find_one({'id':parent_genre})["name"]
        contents = []
        for c in netdb:
            try:
                content = db.booktree.find({'genre_tree':c['id'],
                                            'im':True
                                            }).sort('ra', pymongo.DESCENDING)[0]
            except:
                content = None
            contents.append({
                    'parent_id':c['parent_id'],
                    'id':c['id'],
                    'name':c['name'],
                    'content':content,
                    })
    else:
        content = {
            "name":"name",
            "id":"id",
            "parent_id":"parent_id",
            "content":{"image_url":""},
            }
        contents = [content for i in range(0,span)]
    temp_values = {
        "target":"content",
        "title":u"ジャンル一覧ページ",
        "contents":contents,
        "genre_name":genre_name,
        "rakuten":True,
        "session":session,
        }
    return render_to_response('content/genre.html',temp_values,
                              context_instance=RequestContext(request))

def main():
    pass

if __name__ == '__main__':
    main()
