# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from users.models import *

# Register your models here.

# This will add the UserProfile model that will be managed by the Django management.
admin.site.register(UserProfile)
# This will add the Rating model that will be managed by the Django management.
admin.site.register(Rating)
