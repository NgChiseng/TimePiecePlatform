from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

# Class that will render the products-publication.html to show the admin existing in the TimePiece Platform.
class ProductsPublication(TemplateView):
    template_name = 'products-publication.html'

# Class that will render the products-in-process.html to show the admin existing in the TimePiece Platform.
class ProductsInProcess(TemplateView):
    template_name = 'products-in-process.html'

# Class that will render the products-finished.html to show the admin existing in the TimePiece Platform.
class ProductsFinished(TemplateView):
    template_name = 'products-finished.html'

# Class that will render the products-canceled.html to show the admin existing in the TimePiece Platform.
class ProductsCanceled(TemplateView):
    template_name = 'products-canceled.html'

# Class that will render the services-publication.html to show the admin existing in the TimePiece Platform.
class ServicesPublication(TemplateView):
    template_name = 'services-publication.html'

# Class that will render the services-in-process.html to show the admin existing in the TimePiece Platform.
class ServicesInProcess(TemplateView):
    template_name = 'services-in-process.html'

# Class that will render the services-finished.html to show the admin existing in the TimePiece Platform.
class ServicesFinished(TemplateView):
    template_name = 'services-finished.html'

# Class that will render the services-canceled.html to show the admin existing in the TimePiece Platform.
class ServicesCanceled(TemplateView):
    template_name = 'services-canceled.html'

# Class that will render the donations-publication.html to show the admin existing in the TimePiece Platform.
class DonationsPublication(TemplateView):
    template_name = 'donations-publication.html'

# Class that will render the donations-done.html to show the admin existing in the TimePiece Platform.
class DonationsDone(TemplateView):
    template_name = 'donations-done.html'