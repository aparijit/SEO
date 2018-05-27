# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#import gauto

# Create your views here.
import os
__path__=[os.path.dirname(os.path.abspath(__file__))]
from . import gauto


def index(request):
    return render(request, 'query/home.html')

def list(request):
    search_query = str(request.POST.get('inputquery', False));
    reslist = gauto.show_list(search_query, 1)
    reslist.append(search_query)
    reslist2 = gauto.generate_urls(search_query, 1)
    reslist3 =  gauto.show_list(search_query, 2)
    reslist4 = gauto.show_list(search_query, 3)
    #reslist = gauto.generate_urls(search_query, 1)
    return render(request, 'query/list.html', {'result': reslist, 'urls': reslist2, 'key_word_count' : reslist3,
                                             'key_word_website_count' : reslist4    })
