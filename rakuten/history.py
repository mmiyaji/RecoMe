#!/usr/bin/env python
# encoding: utf-8
"""
history.py

Created by mmiyaji on 2012-12-14.
Copyright (c) 2012  ruhenheim.org. All rights reserved.
"""
from views import *

def home(request):
    """
    Case of GET REQUEST '/'
    home page
    """
    temp_values = Context()
    temp_values = {
        "subscroll":True,
        }
    return render_to_response('general/index.html',temp_values,
                              context_instance=RequestContext(request))
def user(request, user_name = ""):
    temp_values = Context()
    user = None
    # get user
    # try:
    if user_name:
        user = User.objects.get(username = user_name)
    else:
        user = request.user
    # except User.DoesNotExist:
    #     pass
    temp_values = {
        "target":"history",
        "user":user
        }
    return render_to_response('history/user.html',temp_values,
                              context_instance=RequestContext(request))

def main():
    pass
if __name__ == '__main__':
    main()
