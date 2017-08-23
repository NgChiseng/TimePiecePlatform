import datetime
import hashlib
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from users.models import UserProfile
from users.forms import LoginForm, ActivationKeyVerificationForm, ForgotPasswordForm, UpdateProfileForm

# Create your views here.

# Function that manage the log in of the users.
#
# @date [09/08/2017]
#
# @author [Chiseng Ng]
#
# @reference [https://github.com/patriv/ProjectManagement/blob/master/users/views.py]
#
# @param [HttpRequest] request Request of the page.
#
# @returns [HttpResponse]
def log_in(request):
    if request.method == 'POST':
        print("Entra en Login Post")
        form = LoginForm(request.POST)

        if form.is_valid():
            print("Entra en Login form")
            user_field = request.POST['username']
            password = request.POST['password']
            # This will verify if the user submit empty fields
            if user_field == '' or password == '':
                form.add_error(None, "Your data is incorrect.")
                return render(request, 'login.html', {'form': form})
            user_exists = search_user(user_field)

            if (user_exists is not None):
                print("Entra en login user_exist")
                if user_exists.is_active:
                    print("Entra en login activate")
                    user_authenticated = authenticate(username=user_exists.username, password=password)

                    if user_authenticated:
                        login(request, user_authenticated)
                        return HttpResponseRedirect(reverse_lazy('administration'))
                    else:
                        form.add_error(None, "Your data is incorrect.")
                        return render(request, 'login.html', {'form': form})
                else:
                    print("no active")
                    new_user = UserProfile.objects.get(user_fk=user_exists.pk)
                    print(new_user)
                    activation_key = new_user.key_activation
                    if password == activation_key:
                        print("son iguales")
                        return HttpResponseRedirect(reverse('activation_key', kwargs={'activationKey': activation_key}))
                    else:
                        form.add_error(None, "Your data is incorrect.")
                        return render(request, 'login.html', {'form': form})

            else:
                form.add_error(None, "Your data is incorrect.")
                return render(request, 'login.html', {'form': form})
        print("If sin else")
    else:
        print("Entra en login else")
        form = LoginForm()

    context = {'form': form}
    print("Login a punto de render")
    return render(request, 'login.html', context)


# Function that verify if the user name or email belong to the DataBase.
#
# @date [09/08/2017]
#
# @author [Chiseng Ng]
#
# @reference [https://github.com/patriv/ProjectManagement/blob/master/users/views.py]
#
# @param [HttpRequest] request Request of the page.
#
# @returns [HttpResponse]
def search_user(user_field=None):
    try:
        user = User.objects.get(username=user_field)
        if user is not None:
            return user
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=user_field)
            if user is not None:
                return user
        except User.DoesNotExist:
            return None


# Class that will render the activation-key-verification.html for check the admins that enter to the system for first
# time.
class ActivationKeyVerification(TemplateView):
    template_name = 'activation-key-verification.html'

    # Function that render the activation verification screen for change the admins's password in their first session.
    #
    # @date [09/08/2017]
    #
    # @author [Chiseng Ng]
    #
    # @reference [https://github.com/patriv/ProjectManagement/blob/master/users/views.py]
    #
    # @param [HttpRequest] request Request of the page.
    #
    # @returns [HttpResponse]
    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = ActivationKeyVerificationForm(post_values)
        print(form.is_valid())
        if form.is_valid():
            activation_key = self.kwargs['activationKey']
            print("Obtuvo activation key")
            print(activation_key)
            user = UserProfile.objects.get(key_activation=activation_key)
            print("Obtuvo user")
            username = User.objects.get(pk=user.user_fk.pk)
            print(username.pk)
            print(activation_key)
            password = post_values['password']
            password_repeat = post_values['password_repeat']
            print(password_repeat)

            if password == password_repeat:
                username.set_password(password)
                username.is_active = 1
                print(username.is_active)
                print(username.password)
                username.save()
                form.add_error(None, 'The password was successfully changed.')
                return HttpResponseRedirect(reverse_lazy('login'))
            else:
                print("else")
                form.add_error(None,'Password do not match, please try again.')
                return render(request, 'activation-key-verification.html', {'form': form})
        else:
            return render(request, 'activation-key-verification.html', {'form': form})

# Class that will render the admins.html to show the admin existing in the TimePiece Platform.
class Administration(TemplateView):
    template_name = 'admins.html'

    # Function that will return the admins data context to the screen of admins.html
    #
    # @date [15/08/2017]
    #
    # @author [Chiseng Ng]
    #
    # @reference [https://github.com/patriv/ProjectManagement/blob/master/users/views.py]
    #
    # @param [HttpRequest] request Request of the page.
    #
    # @param [AdministrationObject] self The self object that inherited the TemplateView property and used to render the
    # screen.
    #
    # @param [reference] **kwargs Reference that link the context param with the key corresponding to the html file.
    #
    # @returns [HttpResponse]
    def get_context_data(self, **kwargs):
        context = super(Administration, self).get_context_data(**kwargs)
        print("get users")
        admin = UserProfile.objects.all()
        for i in admin:
            print(i.phone)
        context['admins'] = admin
        return context

# Class that will render the admins-register.html to show the admin existing in the TimePiece Platform.
class RegisterAdmin(TemplateView):
    template_name = 'admins-register.html'

# Class that will render the customers.html to show the admin existing in the TimePiece Platform.
class Customers(TemplateView):
    template_name = 'customers.html'

# Class that will render the forgot-password.html to received the email and begin the password reset process.
class ForgotPassword(TemplateView):
    template_name = 'forgot-password.html'
    form_class = ForgotPasswordForm

    # Function that render the forgot password screen, verify if the email exist on DB and send the email for reset the
    #password.
    #
    # @date [22/08/2017]
    #
    # @author [Chiseng Ng]
    #
    # @reference [https://github.com/patriv/ProjectManagement/blob/master/users/views.py]
    #
    # @param [HttpRequest] request Request of the page.
    #
    # @returns [HttpResponse]
    def post(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = ForgotPasswordForm(post_values)

        if form.is_valid():
            email_entered = post_values['email']
            user_exist = User.objects.filter(email=email_entered).exists()

            if user_exist:
                username = User.objects.get(email=email_entered)

                if username.is_active:

                    # This block will obtain the user_profile objects, create the token and the expiration date and
                    #handlered with its variables corresponding.
                    user_profile = UserProfile.objects.get(user_fk=username)
                    user_profile.key_activation = create_token()
                    print("Token= " + user_profile.key_activation)
                    user_profile.date_key_expiration = datetime.datetime.today() + datetime.timedelta(days=1)
                    print(user_profile.date_key_expiration)
                    user_profile.save()

                    # This block will manage the Gmail email service, that will be used to send the email with the data
                    #corresponding to the admin. that forgot his password.

                    # Form field used to pass the data to the email structure html.
                    fields = {
                        'username': username,
                        'key': user_profile.key_activation,
                        'date_expiration': user_profile.date_key_expiration,
                        'host': request.META['HTTP_HOST']
                    }

                    # This will define the information of the document for the email, send the email and return to the
                    #login screen.
                    email_subject = "Recuperación de Contraseña[ TimePiece ]"
                    message_template = "password-reset-email.html"
                    send_email(email_subject, message_template, fields, email_entered)
                    return render(request, 'send-email-done.html')

                else:
                    form.add_error(None, 'Lo sentimos, debe activar la cuenta')
                    return render(request, 'login.html', {'form': form})

            else:
                print("else no user")
                form.add_error(None, 'El correo ingresado no es válido, por favor verifique')
                return render(request, 'forgot-password.html', {'form': form})
        else:
            print("form is not valid")
            form.add_error(None, 'Ingrese un correo electrónico válido')
            return render(request, 'forgot-password.html', {'form': form})

# Class that will render the password-reset.html, for reset the password.
class Password_Reset(TemplateView):
    template_name = 'password-reset.html'

    # Function that render the forgot password screen, verify if the email exist on DB and send the email for reset the
    # password.
    #
    # @date [22/08/2017]
    #
    # @author [Chiseng Ng]
    #
    # @reference [https://github.com/patriv/ProjectManagement/blob/master/users/views.py]
    #
    # @param [HttpRequest] request Request of the page.
    #
    # @returns [HttpResponse]
    def post(self, request, *args, **kwargs):
        print("post reset")
        post_values = request.POST.copy()
        form = ActivationKeyVerificationForm(post_values)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            activation_key = self.kwargs['token']
            print("Token:" + activation_key)
            user = UserProfile.objects.get(key_activation=activation_key)
            print(user)
            username = User.objects.get(pk=user.user_fk.pk)
            print(username.pk)
            print(activation_key)
            password = post_values['password']
            password_repeat = post_values['password_repeat']
            print(password)
            print(password_repeat)
            if password == password_repeat:
                print("las claves son iguales")
                username.set_password(password)
                username.save()
                print("Se guardo la clave")
                form.add_error(None, "Las contraseña se ha restablecido exitosamente.")
                return HttpResponseRedirect(reverse_lazy('login'))
            else:
                print("else")
                messages.success(request, 'Las contraseñas no coinceden, por favor verifique.')
                return HttpResponseRedirect(reverse_lazy('password_reset', kwargs={'token': activation_key}))
        else:
            form.add_error(None,'Se ha producido un error ')
            return render(request, 'password-reset.html', {'form': form, 'token': self.kwargs['token']})

# Class that will render the profile.html, show the actual data and permit the modification of its.
class Profile(TemplateView):
    template_name = 'page-profile.html'
    form_class = UpdateProfileForm

    def get_context_data(self, **kwargs):
        context = super(
            Profile, self).get_context_data(**kwargs)
        print("get")

        print(self.kwargs['id'])

        user = UserProfile.objects.get(user_fk_id=self.kwargs['id'])
        # print(user)
        # if not user:
        #   data = {
        #      'first_name': User.first_name,
        #     'last_name' : User.last_name
        # }
        # else:
        data = {'first_name': user.user_fk.first_name,
                'last_name': user.user_fk.last_name,
                'username': user.user_fk.username,
                'email': user.user_fk.email,
                'phone': user.phone,
                'image_profile': user.image_profile
                }
        form = LoginForm(initial=data)
        context['form'] = form
        context['users'] = user
        return context

    def post(self, request, *args, **kwargs):
        form = UpdateProfileForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            user_pk = kwargs['id']
            userProfile = UserProfile.objects.get(user_fk=user_pk)

            user = User.objects.get(pk=userProfile.user_fk_id)
            print(user)
            user.first_name = request.POST['first_name']
            print(user.first_name)
            user.last_name = request.POST['last_name']
            userProfile.phone = request.POST['phone']
            if (request.FILES == {}):
                pass
            else:
                print(request.FILES)
                userProfile.imageProfile = request.FILES['image_profile']
                userProfile.loadPhoto = True

            print(userProfile.imageProfile)
            user.username = request.POST['username']
            user.save()
            userProfile.save()
            messages.success(request, "Su perfil ha sido actualizado exitosamente")
            return HttpResponseRedirect(reverse_lazy('profile', kwargs={'id': user_pk}))

        else:
            return render(request, 'page-profile.html',
                          {'form': form})

# Function that will generate the tokens.
#
# @date [22/08/2017]
#
# @author [Chiseng Ng]
#
# @reference [https://github.com/patriv/ProjectManagement/blob/master/users/views.py]
#
# @param [None]
#
# @returns [String_Token]
def create_token():

    # This generate the first token key.
    chars = list('ABCDEFGHIJKLMNOPQRSTUVWYZabcdefghijklmnopqrstuvwyz0123456789')
    random.shuffle(chars)
    chars = ''.join(chars)
    sha1 = hashlib.sha1(chars.encode('utf8'))
    token = sha1.hexdigest()
    key = token[:12]

    # This verify if the token key exist on the date base and if is positive will generate other.
    while UserProfile.objects.filter(key_activation=key).exists():
        print('Exist')
        chars = list('ABCDEFGHIJKLMNOPQRSTUVWYZabcdefghijklmnopqrstuvwyz0123456789')
        random.shuffle(chars)
        chars = ''.join(chars)
        sha1 = hashlib.sha1(chars.encode('utf8'))
        token = sha1.hexdigest()
        key = token[:12]

    return key


# Function that will end to build the email and will send it.
#
# @date [22/08/2017]
#
# @author [Chiseng Ng]
#
# @reference [https://github.com/patriv/ProjectManagement/blob/master/users/views.py]
#
# @param [String] subject Subject of the email.
#
# @param [String] message_template Name of the template file that will contain the email format or design.
#
# @param [Form] context Form with the fields or context of the email, that will be linked to the message_template.
#
# @param [String] email Email entered for the admin. obtained of the request.
#
# @returns [String_Token]
def send_email(subject, message_template, context, email):
    message = get_template(message_template).render(context)
    msg = EmailMessage(subject, message, to=[email], from_email='TimePiece - Activacion de Cuenta')
    msg.content_subtype = 'html'
    msg.send()
