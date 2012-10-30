#!/usr/bin/env python
# encoding: utf-8
"""
content.py

Ccreated by mmiyaji on 2012-10-29.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
/"""
from views import *
import re
if settings.MONGODB_USE:
    import pymongo
def home(request):
    """
    Case of GET REQUEST '/content/'
    画像の一覧を表示するページ
    """
    temp_values = Context()
    page=1
    span = 20
    order = "-created_at"
    conten = {}
    if settings.MONGODB_USE:
        start = 0
        limit = span
        conn = pymongo.Connection(settings.MONGODB_PATH, settings.MONGODB_PORT)
        db = conn.rakuten
        usedb = db.booktree
        net = usedb.find().sort('review_average', pymongo.DESCENDING).skip(start).limit(limit)
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
        "target":"content",
        "title":u"コンテンツ一覧ページ",
        "contents":contents,
        "rakuten":True,
        }
    return render_to_response('content/index.html',temp_values,
                              context_instance=RequestContext(request))

def main():
    pass

if __name__ == '__main__':
    main()
