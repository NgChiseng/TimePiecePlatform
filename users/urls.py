from django.conf.urls import url
import django.contrib.auth.views
from users.views import *

# url(Path, Function or Class of the view, key to call each view in the html or view function)
urlpatterns = [
    url(r'^login/$', log_in, name='login'),

    url(r'^activation-key/(?P<activationKey>\w+)$', ActivationKeyVerification.as_view(), name='activation_key'),

    url(r'^administration', Administration.as_view(), name='administration'),

    url(r'^register-admin', RegisterAdmin.as_view(), name='register_admin'),

    url(r'^customers', Customers.as_view(), name='customers'),

    url(r'^forgot-password', ForgotPassword.as_view(), name='forgot_password'),

    url(r'^reset/(?P<token>.+)$', Password_Reset.as_view(), name='password_reset'),

    url(r'^profile/(?P<id>\w+)$', Profile.as_view(), name='profile'),

    url(r'^logout', django.contrib.auth.views.logout, {'next_page': 'login'}, name='logout'),
]