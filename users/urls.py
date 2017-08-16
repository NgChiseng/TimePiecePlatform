from django.conf.urls import url
import django.contrib.auth.views
from users.views import *

# url(Path, Function or Class of the view, key to call each view in the html or view function)
urlpatterns = [
    url(r'^login/$', log_in, name='login'),

    url(r'^first-session/(?P<activationKey>\w+)$', FirstSession.as_view(), name='first_session'),

    url(r'^administration', Administration.as_view(), name='administration'),

    # url(r'^register-admin', RegisterAdmin.as_view(), name='register_admin'),
]