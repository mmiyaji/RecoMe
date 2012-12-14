#!/usr/bin/env python
# encoding: utf-8
"""
content.py

Ccreated by mmiyaji on 2012-10-29.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
from views import *
from recommend import *
from rakuten.models import *
if settings.MONGODB_USE:
    import pymongo
def home(request, genre_id = None, content_id = None, name = 'content'):
    """
    Case of GET REQUEST '/content/'
    画像の一覧を表示するページ
    """
    temp_values = Context()
    page=1
    span = 8
    pspan = 10
    order = "-created_at"
    conten = {}
    genre = '101266'
    genre_name = None
    count = 0
    user = None
    recommend = False
    if name == "recommend":
        recommend = True
        # print "content id",content_id
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
            if name == "recommend" and content_id and request.user.is_authenticated():
                recommend = True
                recom = Recom(memkey="nobel_word_network_limit100")
                ids = get_individuals(request, user, content_id, span, pspan, recom)
                contents = get_contens(ids, usedb, genre)
                count = 0
                genre_name = db.ichiba_genre.find({'id':genre})[0]["name"]
                # echoes(request, ids, contents)
            else:
                # print content_id
                if content_id:
                    ids = []
                    c = get_by_id_from_mongo(content_id)
                    if c:
                        tfidfs = c['tfidfs']
                        t = sorted(tfidfs.items(), key=lambda x: x[1]["tfidf"], reverse=True)
                        for i in range(0,span):
                            ppp = []
                            for p in range(0,pspan):
                                if len(t) > p:
                                    ts = t[p]
                                    w = ts[0]
                                    ppp.append({'word':w})
                                else:
                                    break
                            ids.append(ppp)
                        contents = get_contens(ids, usedb, genre, estimate=False)
                    else:
                        netdb = usedb.find({'genre_tree':genre,
                                            # 'isimage':{'$exists':True},
                                            # 'image_code':200,
                                            'im':True,
                                            # 'words':{'$ne':'中古'},
                                            }).sort('review_count', pymongo.DESCENDING)
                        net = netdb.skip(start).limit(limit)
                        count = netdb.count()
                        contents = net
                else:
                    netdb = usedb.find({'genre_tree':genre,
                                        # 'isimage':{'$exists':True},
                                        # 'image_code':200,
                                        'im':True,
                                        # 'words':{'$ne':'中古'},
                                        }).sort('review_count', pymongo.DESCENDING)
                    net = netdb.skip(start).limit(limit)
                    count = netdb.count()
                    contents = net
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
        # MONGODB_PATH = "127.0.0.1"
        MONGODB_PATH = settings.MONGODB_PATH
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
def get_by_id_from_mongo(id):
    conn = pymongo.Connection(settings.MONGODB_PATH, settings.MONGODB_PORT)
    db = conn.rakuten
    usedb = db.booktree
    return usedb.find_one({'id':id})
def rouletteChoice(itemList, getWeight = None, getItem = None):
    if getWeight == None:
        def _getWeight(item):
            return item
        getWeight = _getWeight
    totalWeight = 0
    for item in itemList:
        totalWeight += getWeight(item)
    r = random.random() * totalWeight
    for i in xrange(len(itemList)):
        w = getWeight(itemList[i])
        if r < w:
            if getItem:
                return getItem(itemList[i])
            else:
                return i
        else:
            r -= w
def norm(array):
    a = numpy.array([array])
    n = a / numpy.linalg.norm(a)
    return list(n[0])


def get_individuals(request, user, content_id, span, pspan, recom):
    c = get_by_id_from_mongo(content_id)
    if c:
        tfidfs = c['tfidfs']
        user = request.user
        inds = None
        try:
            now_history = History.get_by_user(user)[0]
        except:
            now_history = None
        history = History()
        history.user = user
        history.content_id = content_id
        history.save()
        if now_history:
            inds = now_history.individual.all()
        t = sorted(tfidfs.items(), key=lambda x: x[1]["tfidf"], reverse=True)
        ids = []
        for i in range(0,span):
            print "######",i
            try:
                ind = inds[i].clone()
            except:
                ind = Individual()
                ind.user = user
            ind.recent_history = history
            ind.save()
            ppp = []
            paras = ind.sorted_param()
            sorted(tfidfs.items(), key=lambda x: x[1]["tfidf"], reverse=True)
            for p in range(0,pspan):
                path_str = ""
                deleted = False
                if len(t) > p:
                    ts = t[p]
                    w = ts[0]
                else:
                    continue
                if len(paras) > p:
                    para = paras[p]
                    length = 0
                    # try:
                    if True:
                        if para.word == w:
                            length = 0
                            path = [w]
                            # print 'same word',
                        else:
                            length,path = recom.get_path(para.word, w)
                        if length != 0 and len(path) == 2:
                            deleted = recom.delete_path(para.word, w)
                            length,path = recom.get_path(para.word, w)
                            if deleted:
                                # print 'connected 1 length, then remove edge.',
                                recom.repair_path()
                    # except:
                    else:
                        # print 'not connected',
                        # print para.word, 'has',
                        # if recom.is_node(para.word):
                        #     print len(recom.get_neighbors(para.word)),
                        # else:
                        #     print 'no',
                        # print 'edges, ',
                        # print w, 'has',
                        # if recom.is_node(w):
                        #     print len(recom.get_neighbors(w)),
                        # else:
                        #     print 'no',
                        # print 'edges.',
                        path = [para.word, w]
                    hop = len(path)
                    sp = ts[1]["tfidf"]
                    ep = para.score
                    path_value = [sp]
                    if hop == 1:
                        path.append(path[0])
                        path.append(path[0])
                        hop = len(path)
                    if hop > 2:
                        step = (ep - sp) / (hop - 1)
                        for pp in range(1,hop-1):
                            path_value.append(sp+(pp*step))
                    path_value.append(ep)
                    rl = rouletteChoice(path_value)
                    for w1,w2 in zip(path, path_value):
                        # print w1,w2,"->",
                        path_str += "%s(%s)," % (w1,w2)
                    # print "selected", rl,path[rl], path_value[rl]
                    para.word = path[rl]
                    para.score = path_value[rl]
                else:
                    para = Parameter()
                    para.rank = p
                    para.word = w
                    para.score = ts[1]["tfidf"]
                para.path = path_str
                para.isdeleted_path = deleted
                ppp.append(para.score)
                para.save()
                ind.parameter.add(para)
            ind.save()
            ids.append(ind)
            np = norm(ppp)
            # if settings.DEBUG:
            #     print np, ppp
            for pp1,p2 in zip(ind.parameter.all(),np):
                pp1.score = p2
                pp1.save()
        history.individual = ids
        history.save()
        return ids
def get_contens(ids, usedb, genre, estimate=True):
    contents = []
    for ii in ids:
        ind_count = 0
        c = None
        is_find = False
        if estimate:
            iipara = ii.parameter.all()
            iiw = [iipara[0].word]
        else:
            # print ii
            iipara = ii
            iiw = [iipara[0]["word"]]
        # for ip in iipara:
        #     iiw.append(ip.word)
        for il in range(0,len(iipara)-1):
            # if settings.DEBUG:
            #     print 'search by ',
            #     for q in iiw:
            #         print q,
            #     print
            iiii = '_'.join(iiw)
            iikey = genre+"_"+iiii
            if iikey in cache:
                c2 = cache.get(iikey)
            else:
                c2 = usedb.find({'genre_tree':genre,
                                 'im':True,
                                 'words': {'$in':iiw},
                                 })
                try:
                    cache.set(iikey, c2, 0)
                    # if settings.DEBUG:
                    #     print 'set',iikey
                except:
                    pass
            # print '## ', c2.count(),iiw
            if c2.count() > 0:
                # print iiw
                for c in c2:
                    if c not in contents:
                        is_find = True
                        break
                    # ind_count += 1
                    # if ind_count > span * 3:
                    #     print 'not found...'
                    #     break
            if is_find:
                break
            if estimate:
                iiw.append(iipara[il+1].word)
            else:
                iiw.append(iipara[il+1]['word'])
        contents.append(c)
    return contents
def main():
    pass
# 指定したディレクトリにログ書きだし
def echoes(request, inds, contents):
    if True:
        user = request.user
        nowdate = datetime.datetime.now()
        now = nowdate.strftime("%a, %d %b %Y %H:%M:%S +0900")
        dir_date = nowdate.strftime("%Y")
        commands.getoutput("mkdir -p "+settings.TMP_DIR+'/'+user.username+'/access/'+dir_date)
        dirs = settings.TMP_DIR+'/'+user.username+'/access/'+dir_date+'/'+nowdate.strftime("%m")+'.json'
        f=open(dirs,'a')
        tmp = {
            "date":now,
            "user":user.username,
            "individuals":inds,
            "contents":contents,
            }
        f.write(serializers.serialize('json', tmp))
        # print tmp
        f.close()
    # except:
    #     pass

if __name__ == '__main__':
    main()
