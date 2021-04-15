# -*- coding: utf-8 -*-

from urllib import parse
from django import template
from django.shortcuts import resolve_url

register = template.Library()


@register.simple_tag
def get_return_link(request):
    top_page = resolve_url('share_calendar:calendar')
    referer = request.environ.get('HTTP_REFERER')  #前ページのURL

    # URL直接入力やお気に入りアクセスのときはリファラがないので、トップぺージに戻す
    if referer:

        # リファラがある場合、前回ページが自分のサイト内であれば、そこに戻す。
        parse_result = parse.urlparse(referer)
        if request.get_host() == parse_result.netloc:
            return referer
        if request.method == "POST":
            return top_page

    return top_page
