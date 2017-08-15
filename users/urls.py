from django.conf.urls import url
import django.contrib.auth.views
from users.views import *

urlpatterns = [
    url(r'^login/$', log_in, name='login'),

    url(r'^first_session/(?P<activationKey>\w+)$', FirstSession.as_view(), name='first_session'),

    url(r'^administration', Administration.as_view(), name='administration'),
]