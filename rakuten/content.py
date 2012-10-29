#!/usr/bin/env python
# encoding: utf-8
"""
content.py

Ccreated by mmiyaji on 2012-10-29.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
/"""
from views import *
import re
def home(request):
    """
    Case of GET REQUEST '/content/'
    画像の一覧を表示するページ
    """
    temp_values = Context()
    page=1
    span = 8
    order = "-created_at"
    content = {"url":"static/img/screenshot/miu.jpg", "caption":"hoge"}
    contents = [content for i in range(0,span)]
    temp_values = {
        "target":"content",
        "title":u"コンテンツ一覧ページ",
        "contents":contents,
        }
    return render_to_response('content/index.html',temp_values,
                              context_instance=RequestContext(request))

def main():
    pass

if __name__ == '__main__':
    main()
