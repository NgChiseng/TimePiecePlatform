#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User, Group
from users.models import UserProfile
from django.db import models

# Form used for declare the login fields and validations on their.
class LoginForm(forms.Form):
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
        if password is None:
            password_len = 0
        else:
            password_len = len(password)

        if password and password != password_repeat:
            msj = "Las claves no coinciden, por favor intente de nuevo."
            self.add_error('password', msj)

        if (password_len < 8) or (password_len >= 16):
            msj = "La clave debe ser mayor a 8 digitos y menor que 15."
            self.add_error('password_repeat', msj)
        return self.cleaned_data

# Form used to declare the ForgotPassword field.
class ForgotPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', ]

# Form used to declare the Profile fields.
class UpdateProfileForm(forms.Form):

    username = forms.CharField(required=True)
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'id': "email", 'type': "email",
                                                                           'class': "validate"}))
    image_profile = forms.ImageField(required=False)

    class Meta:
        model = User, UserProfile
        fields = ('username', 'email', 'phone', 'image_profile',)

# Form of the Users that will be used on profile view.
class UserForm(forms.ModelForm):
    username = forms.CharField(required=True)
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'id': "email", 'type': "email",
                                                                           'class': "validate"}))
    image_profile = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_email(self):
        print("Clean email")
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).count() != 0:
            print("dentro del if")
            msj = "Este correo ya está siendo utilizado"
            self.add_error('email', msj)
        return email
