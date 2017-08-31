from django.conf.urls import url
from api.views import CreateViewUser, DetailViewUser, CreateViewUserProfile, DetailViewUserProfile, LogInView


# url(Path, Function or Class of the view, key to call each view in the html or view function)
urlpatterns = [
    url(r'^users/$', CreateViewUser.as_view(), name='users'),

    url(r'^users/(?P<pk>[0-9]+)$', DetailViewUser.as_view(), name='users_detail'),

    url(r'^profiles/$', CreateViewUserProfile.as_view(), name='profiles'),

    url(r'^profiles/(?P<pk>[0-9]+)$', DetailViewUserProfile.as_view(), name='profiles_detail'),

    url(r'^api-login', LogInView.as_view(), name='api_login'),
]