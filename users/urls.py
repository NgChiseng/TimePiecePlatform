from django.conf.urls import url
import django.contrib.auth.views
from users.views import *

urlpatterns = [
    url(r'^$', log_in, name='login'),
]