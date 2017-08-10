#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User, Group
from users.models import UserProfile
from django.db import models

class LoginForm(forms.Form):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class ActivationKeyVerificationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password: ",
        widget=forms.PasswordInput()
    )

    password_repeat = forms.CharField(
        label="Repeat Password: ",
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['password', ]

    def clean(self):
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')
        password_len = len(password)

        if password and password != password_repeat:
            msj = "Password don't match, please try again."
            self.add_error('password', msj)

        if (password_len < 8) or (password_len >= 16):
            msj = "The password must be 8-digit and less than 15."
            self.add_error('password_repeat', msj)
        return self.cleaned_data
