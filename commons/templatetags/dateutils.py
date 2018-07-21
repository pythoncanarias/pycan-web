#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import datetime

from django import template
from django.utils.safestring import mark_safe
from commons import filters

register = template.Library()

register.filter('as_month', filters.as_month)
register.filter('as_date', filters.as_date)
