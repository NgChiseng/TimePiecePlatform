# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 20:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='announcement_images/')),
                ('title', models.CharField(max_length=128)),
                ('type', models.CharField(max_length=32)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('unit', models.CharField(blank=True, max_length=32, null=True)),
                ('address', models.CharField(blank=True, max_length=256, null=True)),
                ('expected_amount', models.IntegerField(blank=True, null=True)),
                ('received_amount', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=512)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_modification_date', models.DateTimeField(auto_now_add=True)),
                ('user_email_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=32)),
                ('operation', models.CharField(max_length=32)),
                ('points', models.IntegerField()),
                ('evaluation_date', models.DateTimeField(auto_now_add=True)),
                ('announcement_id_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Announcement')),
                ('user_email_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant_total_payment', models.IntegerField()),
                ('total_payment_to_advertisers', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingBag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('advertiser_email_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_advertiser_email_fk', to=settings.AUTH_USER_MODEL)),
                ('announcement_id_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Announcement')),
                ('applicant_email_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_applicant_email_fk', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_token', models.CharField(max_length=512)),
                ('applicant_payment_date', models.DateTimeField(auto_now_add=True)),
                ('applicant_end_date', models.DateTimeField(blank=True, null=True)),
                ('advertiser_end_date', models.DateTimeField(blank=True, null=True)),
                ('applicant_status', models.CharField(max_length=32)),
                ('advertiser_status', models.CharField(max_length=32)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('payment_total_transaction', models.IntegerField()),
                ('price', models.IntegerField(blank=True, null=True)),
                ('unit', models.IntegerField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('advertiser_email_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advertiser_email_fk', to=settings.AUTH_USER_MODEL)),
                ('announcement_id_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Announcement')),
                ('applicant_email_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicant_email_fk', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='transaction_id_fk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Transaction'),
        ),
    ]
