#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.backends import ModelBackend

from members.models import Member


class EmailBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None):
        try:
            member = Member.objects.get(email=username)
            user = member.user
            if user.check_password(password):
                return user
        except Member.DoesNotExist:
            pass
        return None
