from django.conf.urls import url
import django.contrib.auth.views
from django.contrib.auth.decorators import login_required

from dashboard.views import *

# url(Path, Function or Class of the view, key to call each view in the html or view function)
# Note: the login_required decorator works for validate the urls that need login for enter, and redirect it to the
# login_url (This can to be optimized with a better organization of urls, file and design).
urlpatterns = [
    url(r'^products-publication/$', login_required(ProductsPublication.as_view(), login_url='login'), name='products_publication'),

    url(r'^products-in-process/$', login_required(ProductsInProcess.as_view(), login_url='login'), name='products_in_process'),

    url(r'^products-finished/$', login_required(ProductsFinished.as_view(), login_url='login'), name='products_finished'),

    url(r'^products-canceled/$', login_required(ProductsCanceled.as_view(), login_url='login'), name='products_canceled'),

    url(r'^services-publication/$', login_required(ServicesPublication.as_view(), login_url='login'), name='services_publication'),

    url(r'^services-in-process/$', login_required(ServicesInProcess.as_view(), login_url='login'), name='services_in_process'),

    url(r'^services-finished/$', login_required(ServicesFinished.as_view(), login_url='login'), name='services_finished'),

    url(r'^services-canceled/$', login_required(ServicesCanceled.as_view(), login_url='login'), name='services_canceled'),

    url(r'^donations-publication/$', login_required(DonationsPublication.as_view(), login_url='login'), name='donations_publication'),

    url(r'^donations-done/$', login_required(DonationsDone.as_view(), login_url='login'), name='donations_done'),

    url(r'^payments-registered/$', login_required(PaymentsRegistered.as_view(), login_url='login'), name='payments_registered'),

    url(r'^payments-transaction/$', login_required(PaymentsTransaction.as_view(), login_url='login'), name='payments_transaction'),

    url(r'^shopping-car/$', login_required(ShoppingCar.as_view(), login_url='login'), name='shopping_car'),
]
