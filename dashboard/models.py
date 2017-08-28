from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# This class will contain the announcements created by the TimePiece App users.
class Announcement(models.Model):

    user_email_fk = models.ForeignKey(User)
    picture = models.ImageField(upload_to='announcement_images/', blank=True, null=True)
    title = models.CharField(max_length=128)
    type = models.CharField(max_length=32) # { product, service, donation }
    price = models.IntegerField(blank=True, null=True)  # { Null if donation }
    unit = models.CharField(max_length=32, blank=True, null=True) # { Null if donation }
    address = models.CharField(max_length=256, blank=True, null=True) # { Null if donation }
    expected_amount = models.IntegerField(blank=True, null=True) # { Null if not donation }
    received_amount = models.IntegerField(blank=True, null=True) # { Null if not donation }
    description = models.CharField(max_length=512, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modification_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_user_name(self):
        return self.user_email_fk.first_name

# This class will contain the evaluation transaction data.
class Evaluation(models.Model):

    user_email_fk = models.ForeignKey(User)
    announcement_id_fk = models.ForeignKey(Announcement)
    type = models.CharField(max_length=32) # { announce, donation, purchase }
    operation = models.CharField(max_length=32) # { created, bought }
    points = models.IntegerField()
    evaluation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.announcement_id_fk) + ',' + str(self.user_email)

    def get_announce_title(self):
        return self.announcement_id_fk.title

# This class will contain the shopping bag transaction data in TimePiece app.
class ShoppingBag(models.Model):

    advertiser_email_fk = models.ForeignKey(User, related_name='shopping_advertiser_email_fk')
    applicant_email_fk = models.ForeignKey(User, related_name='shopping_applicant_email_fk')
    announcement_id_fk = models.ForeignKey(Announcement)
    add_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.announcement_id_fk) + ',' + str(self.advertiser_email_fk) + ',' + str(self.applicant_email_fk)

    def get_advertiser_name(self):
        return self.advertiser_email_fk.first_name

    def get_announcement_type(self):
        return self.announcement_id_fk.type

# This class will contain the all the transaction of the TimePiece app.
class Transaction(models.Model):

    advertiser_email_fk = models.ForeignKey(User, related_name='advertiser_email_fk')
    applicant_email_fk = models.ForeignKey(User, related_name='applicant_email_fk')
    announcement_id_fk = models.ForeignKey(Announcement)
    payment_token = models.CharField(max_length=512)
    applicant_payment_date = models.DateTimeField(auto_now_add=True)
    applicant_end_date = models.DateTimeField(blank=True, null=True) # { Null if the applicant not confirm }
    advertiser_end_date = models.DateTimeField(blank=True, null=True) # { Null if the advertiser not confirm }
    applicant_status = models.CharField(max_length=32) # {In process, Canceled, Terminated}
    advertiser_status = models.CharField(max_length=32) # {In process, Canceled, Terminated}
    payment_date = models.DateTimeField(blank=True, null=True) # { Null if the system not paid yet }
    payment_total_transaction = models.IntegerField() # { If not donation is equal to price * quantity }
    price = models.IntegerField(blank=True, null=True) # { fk_Announ and Null if Donation }
    unit = models.IntegerField(blank=True, null=True) # { fk_Announ and Null if Donation }
    quantity = models.IntegerField(blank=True, null=True) # { fk_Announ and Null if Donation }

    def __str__(self):
        return self.id

    def get_advertiser_name(self):
        return self.advertiser_email_fk.first_name

    def get_announcement_type(self):
        return self.announcement_id_fk.type

# This class that will contain the payments that was make in the TimePiece app.
class Payment(models.Model):

    transaction_id_fk = models.ForeignKey(Transaction)
    applicant_total_payment = models.IntegerField()
    total_payment_to_advertisers = models.IntegerField()

    def __str__(self):
        return self.id

    def get_payment_token(self):
        return self.transaction_id_fk.payment_token

    def get_applicant_payment_date(self):
        return self.transaction_id_fk.applicant_payment_date





