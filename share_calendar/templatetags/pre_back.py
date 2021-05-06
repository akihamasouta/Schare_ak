# -*- coding: utf-8 -*-

from urllib import parse
from django import template
from django.shortcuts import resolve_url
import re

register = template.Library()


@register.simple_tag
def get_return_link(request):
    top_page = resolve_url('share_calendar:calendar')
    referer = request.environ.get('HTTP_REFERER')  #前ページのURL
    now_page_url = request.build_absolute_uri()
    
    
    memory_pic_url = resolve_url('share_calendar:memory_pic'+'/'+'0')
    num_list = re.findall(r'\d+', now_page_url)
    memory_pic_num = str(num_list[-1])
    memory_pic_url = "{0}://{1}/{2}/{3}/".format(request.scheme, request.get_host(),'share_calendar/memory_pic',memory_pic_num)
    
    num2_list = re.findall(r'\d+', str(referer)) 
    look_pic_url = False
    if len(num2_list) >=3:
        look_pic_num1 = str(num2_list[-1])
        look_pic_num2 = str(num2_list[-2])
        look_pic_num3 = str(num2_list[-3])
        look_pic_url = "{0}://{1}/{2}/{3}/{4}/{5}/".format(request.scheme, request.get_host(),'share_calendar/look_pic',look_pic_num3,look_pic_num2,look_pic_num1)

    

    # URL直接入力やお気に入りアクセスのときはリファラがないので、トップぺージに戻す
    if referer:

        # リファラがある場合、前回ページが自分のサイト内であれば、そこに戻す。
        parse_result = parse.urlparse(referer)
        if str(now_page_url) == str(referer):
            return top_page
        if str(now_page_url) == str(memory_pic_url) and str(look_pic_url) == str(referer):
            return top_page
                
        if request.get_host() == parse_result.netloc:
            return referer
        if request.method == "POST":
            return top_page

    return top_page
