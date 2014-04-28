#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quokka.core.db import db
from quokka.core.models import Content
from quokka.core.admin.utils import _l

class Post(Content):
    # URL_NAMESPACE = 'posts.detail'
    body = db.StringField(required=True, verbose_name=_l('Body'))
