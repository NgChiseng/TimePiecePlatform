#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User, Group
from users.models import UserProfile
from django.db import models

# Form used for declare the login fields and validations on their.
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

# Form used to declare the activationKeyVerification fields and validations on their.
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

    # Function that will validate the field that the user entered.
    #
    # @date [15/08/2017]
    #
    # @author [Chiseng Ng]
    #
    # @reference [https://github.com/patriv/ProjectManagement/blob/master/users/forms.py]
    #
    # @param [HttpRequest] request Request of the page.
    #
    # @returns [HttpResponse]
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

# Form used to declare the ForgotPassword field.
class ForgotPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', ]
