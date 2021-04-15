# -*- coding: utf-8 -*-

import os

#settings.pyからそのままコピー
SECRET_KEY='lnkfbav=4cvd!$do_47%73^_bw)z2$(f8em1_tur4!1gx58=7g'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



DEBUG = True