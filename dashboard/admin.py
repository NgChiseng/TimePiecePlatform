from django.contrib import admin
from dashboard.models import *

# Register your models here.

# This will add the Evaluation model that will be managed by the Django management.
admin.site.register(Evaluation)
# This will add the Announcement model that will be managed by the Django management.
admin.site.register(Announcement)
# This will add the ShoppingBag model that will be managed by the Django management.
admin.site.register(ShoppingBag)
# This will add the Transaction model that will be managed by the Django management.
admin.site.register(Transaction)
# This will add the Payment model that will be managed by the Django management.
admin.site.register(Payment)
