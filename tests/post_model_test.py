#!/usr/bin/env python
# encoding: utf-8
from datetime import datetime
from unittest import TestCase

import application.models as Models
from application import create_app


class PostModelTest(TestCase):
    def setUp(self):
        self.app = create_app('TESTING')
        Models.Role.objects.create(
            id=1, name="Test",
            permission=Models.Permission.DELETE)
        r = Models.Role.objects.all()[0]
        Models.User(
            id=10000, username="zhangsan",
            password="password",
            email="liqianglau@outlook.com",
            role=r).save()

    def tearDown(self):
        for p in Models.Post.objects.filter():
            p.delete()
        for u in Models.User.objects.filter():
            u.delete()

    def test_save(self):
        u = Models.User.objects.get_by_id(10000)
        p = Models.Post(
            title="123", slug="test", content="cnt",
            user=u, categories=[], tags=[],
            version=1, create_at=datetime.now(),
            last_update=datetime.now(), comments=[],
                 status=0)
        self.assertTrue(p.is_valid(), msg=p.errors)
        status = p.save()
        self.assertTrue(status)
