from django.conf.urls import url
import django.contrib.auth.views
from django.contrib.auth.decorators import login_required

from users.views import *

# url(Path, Function or Class of the view, key to call each view in the html or view function)
# Note: the login_required decorator works for validate the urls that need login for enter, and redirect it to the
# login_url (This can to be optimized with a better organization of urls, file and design).
urlpatterns = [
    url(r'^login/$', log_in, name='login'),

    url(r'^activation-key/(?P<activationKey>\w+)$', ActivationKeyVerification.as_view(), name='activation_key'),

    url(r'^administration', login_required(Administration.as_view(), login_url='login'), name='administration'),

    url(r'^register-admin', login_required(RegisterAdmin.as_view(), login_url='login'), name='register_admin'),

    url(r'^customers', login_required(Customers.as_view(), login_url='login'), name='customers'),

    url(r'^forgot-password', ForgotPassword.as_view(), name='forgot_password'),

    url(r'^reset/(?P<token>.+)$', Password_Reset.as_view(), name='password_reset'),

    url(r'^profile/(?P<id>\w+)$', login_required(Profile.as_view(), login_url='login'), name='profile'),

    url(r'^logout', django.contrib.auth.views.logout, {'next_page': 'login'}, name='logout'),
]
