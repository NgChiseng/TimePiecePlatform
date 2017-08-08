# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User, Group
from django.db import models

# Function that take the first_name and second_name of the django User models and returns the complete name.
#
# @date [08/08/2017]
#
# @author [Chiseng Ng]
#
# @references [https://github.com/patriv/ProjectManagement/blob/master/users/models.py]
#             [https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html]
#             [https://docs.djangoproject.com/en/1.11/ref/contrib/auth/]
# @param [object] self It is the self object.
#
# @returns [string] String that represent the complete name.
# def get_name_complete(self):
#    return self.first_name + " " + self.last_name

# This wil add the get_name_complete function to the User model like one of its methods.
# User.add_to_class("__str__", get_name_complete)

# Create your models here.

# This class will represent the extends of the User Django model.
# @references [https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html]
class UserProfile(models.Model):

    user = models.OneToOneField(User)
    phone = models.CharField(max_length=11, blank=True)
    image_profile = models.ImageField(upload_to='images/', blank=True)
    address = models.TextField(max_length=128, blank=True)
    points_accumulated = models.IntegerField(default=0)
    # badge_acquired = models.ForeignKey('Rating')

    def __str__(self):
        return self.user.username
