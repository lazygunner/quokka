# coding: utf-8
import uuid
from quokka.core.db import db
from quokka.core.models import Publishable
from quokka.core.admin.utils import _l



class BaseComment(object):
    author_name = db.StringField(max_length=255, required=True,
                                 verbose_name=_l('Author Name'))
    author_email = db.StringField(max_length=255,
                                  verbose_name=_l('Author Email'))
    body = db.StringField(required=True, verbose_name=_l('Body'))
    spam = db.BooleanField(verbose_name=_l('Spam'))
    deleted = db.BooleanField(verbose_name=_l('Deleted'))
    content_format = db.StringField(
        choices=('markdown',),
        default="markdown",
        verbose_name=_l('Content Format')
    )

    @property
    def gravatar_email(self):
        if self.created_by:
            return self.created_by.email
        return self.author_email


class Reply(Publishable, BaseComment, db.EmbeddedDocument):
    uid = db.StringField(verbose_name=_l('UID'))
    parent = db.StringField(verbose_name=_l('Parent'))

    def clean(self):
        if not self.uid:
            self.uid = str(uuid.uuid4())


class Comment(Publishable, BaseComment, db.Document):
    path = db.StringField(max_length=255, required=True,
                          verbose_name=_l('Path'))
    replies = db.ListField(db.EmbeddedDocumentField(Reply),
                           verbose_name=_l('Replies'))

    def __unicode__(self):
        return u"{0} - {1}...".format(self.author_name, self.body[:15])

    meta = {
        "ordering": ['-created_at'],
        "indexes": ['-created_at', 'path']
    }
