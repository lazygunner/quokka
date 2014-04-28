#!/usr/bin/env python
# -*- coding: utf-8 -*-

from quokka.core.db import db
from flask.ext.security import UserMixin, RoleMixin
from flask.ext.security.utils import encrypt_password
from quokka.core.admin.utils import _l

# Auth
class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True, verbose_name=_l('Name'))
    description = db.StringField(max_length=255,
                                 verbose_name=_l('Description'))

    @classmethod
    def createrole(cls, name, description=None):
        return cls.objects.create(
            name=name,
            description=description
        )

    def __unicode__(self):
        return u"{0} ({1})".format(self.name, self.description or 'Role')


class User(db.DynamicDocument, UserMixin):
    name = db.StringField(max_length=255, verbose_name=_l('Name'))
    email = db.EmailField(max_length=255, unique=True,
                          verbose_name=_l('Email'))
    password = db.StringField(max_length=255, verbose_name=_l('Password'))
    active = db.BooleanField(default=True, verbose_name=_l('Active'))
    confirmed_at = db.DateTimeField(verbose_name=_l('Confirmed At'))
    roles = db.ListField(
        db.ReferenceField(Role, reverse_delete_rule=db.DENY), default=[],
        verbose_name=_l('Roles')
    )

    last_login_at = db.DateTimeField(verbose_name=_l('Last Login At'))
    current_login_at = db.DateTimeField(verbose_name=_l('Current Login At'))
    last_login_ip = db.StringField(max_length=255,
                                   verbose_name=_l('Last Login IP'))
    current_login_ip = db.StringField(max_length=255,
                                      verbose_name=_l('Current Login IP'))
    login_count = db.IntField(verbose_name=_l('Login Count'))

    username = db.StringField(max_length=50, required=False, unique=True,
                              verbose_name=_l('Username'))

    remember_token = db.StringField(max_length=255,
                                    verbose_name=_l('Remember Token'))
    authentication_token = db.StringField(max_length=255,
                                    verbose_name=_l('Authentication Tokern'))

    def clean(self, *args, **kwargs):
        if not self.username:
            self.username = User.generate_username(self.email)

        try:
            super(User, self).clean(*args, **kwargs)
        except:
            pass

    @classmethod
    def generate_username(cls, email):
        username = email.lower()
        for item in ['@', '.', '-', '+']:
            username = username.replace(item, '_')
        return username

    def set_password(self, password, save=False):
        self.password = encrypt_password(password)
        if save:
            self.save()

    @classmethod
    def createuser(cls, name, email, password,
                   active=True, roles=None, username=None):

        username = username or cls.generate_username(email)
        return cls.objects.create(
            name=name,
            email=email,
            password=encrypt_password(password),
            active=active,
            roles=roles,
            username=username
        )

    @property
    def display_name(self):
        return self.name or self.email

    def __unicode__(self):
        return u"{0} <{1}>".format(self.name or '', self.email)

    @property
    def connections(self):
        return Connection.objects(user_id=str(self.id))


class Connection(db.Document):
    user_id = db.ObjectIdField(verbose_name=_l('Connection'))
    provider_id = db.StringField(max_length=255,
                                 verbose_name=_l('Provider ID'))
    provider_user_id = db.StringField(max_length=255,
                                      verbose_name=_l('Provider User ID'))
    access_token = db.StringField(max_length=255, 
                                  verbose_name=_l('Access Token'))
    secret = db.StringField(max_length=255, verbose_name=_l('Secret'))
    display_name = db.StringField(max_length=255,
                                  verbose_name=_l('Display Name'))
    full_name = db.StringField(max_length=255, verbose_name=_l('Full Name'))
    profile_url = db.StringField(max_length=512,
                                 verbose_name=_l('Profile URL'))
    image_url = db.StringField(max_length=512, verbose_name=_l('Image URL'))
    rank = db.IntField(default=1, verbose_name=_l('Rank'))

    @property
    def user(self):
        return User.objects(id=self.user_id).first()
