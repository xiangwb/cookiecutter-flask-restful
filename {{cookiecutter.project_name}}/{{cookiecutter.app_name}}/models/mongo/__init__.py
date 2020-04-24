#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    __init__.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    mongodb的model定义文件
    
    :author: leo
    :copyright: (c) 2020, Tungee
    :date created: 2020-04-24 11:27
 
"""

from datetime import datetime

from bson import ObjectId
from mongoengine import QuerySet, Document, BooleanField, DateTimeField, StringField


class ValidQuerySet(QuerySet):

    def valid_objs(self, *q_objs, **kwargs):
        return self.filter(is_deleted=False, *q_objs, **kwargs)

    def exists(self, *q_objs, **kwargs):
        return bool(self.filter(is_deleted=False, *q_objs, **kwargs).first())

    def valid_get(self, *q_objs, **kwargs):
        return self.get(is_deleted=False, *q_objs, **kwargs)


class CommonDocument(Document):
    id = StringField(name='_id', primary_key=True)
    is_deleted = BooleanField(default=False)
    create_time = DateTimeField()
    update_time = DateTimeField(default=datetime.utcnow)

    def save(self, *args, **kwargs):
        # 也可以选择重写clean
        if not self.create_time:
            self.create_time = datetime.utcnow()
            self.id = ObjectId().__str__()
        self.update_time = datetime.utcnow()
        return super(CommonDocument, self).save(*args, **kwargs)

    def update(self, **kwargs):
        kwargs['update_time'] = datetime.utcnow()
        return super(CommonDocument, self).update(**kwargs)

    meta = {
        'abstract': True,
        'queryset_class': ValidQuerySet
    }
