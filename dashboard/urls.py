from django.conf.urls import url
import django.contrib.auth.views
from dashboard.views import *

# url(Path, Function or Class of the view, key to call each view in the html or view function)
urlpatterns = [
    url(r'^products-publication/$', ProductsPublication.as_view(), name='products_publication'),

    url(r'^products-in-process/$', ProductsInProcess.as_view(), name='products_in_process'),

    url(r'^products-finished/$', ProductsFinished.as_view(), name='products_finished'),

    url(r'^products-canceled/$', ProductsCanceled.as_view(), name='products_canceled'),

    url(r'^services-publication/$', ServicesPublication.as_view(), name='services_publication'),

    url(r'^services-in-process/$', ServicesInProcess.as_view(), name='services_in_process'),

    url(r'^services-finished/$', ServicesFinished.as_view(), name='services_finished'),

    url(r'^services-canceled/$', ServicesCanceled.as_view(), name='services_canceled'),

    url(r'^donations-publication/$', DonationsPublication.as_view(), name='donations_publication'),

    url(r'^donations-done/$', DonationsDone.as_view(), name='donations_done'),

    #url(r'^first-session/(?P<activationKey>\w+)$', FirstSession.as_view(), name='first_session'),

    #url(r'^administration', Administration.as_view(), name='administration'),

    #url(r'^register-admin', RegisterAdmin.as_view(), name='register_admin'),

    #url (r'^customers', Customers.as_view(), name='customers'),
]