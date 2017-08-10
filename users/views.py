from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from users.models import UserProfile
from users.forms import LoginForm, ActivationKeyVerificationForm

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
            user_exists = search_user(user_field)

            if user_exists is not None:
                print("Entra en login user_exist")
                if user_exists.is_active:
                    print("Entra en login activate")
                    user_authenticated = authenticate(username=user_exists.username, password=password)

                    if user_authenticated:
                        login(request, user_authenticated)
                        return HttpResponseRedirect('/admin')
                    else:
                        form.add_error(None, "Your data is incorrect.")
                        return render(request, 'page-login.html', {'form': form})
                else:
                    print("no active")
                    new_user = UserProfile.objects.get(user_fk=user_exists.pk)
                    print(new_user)
                    activation_key = new_user.key_activation
                    if password == activation_key:
                        print("son iguales")
                        return HttpResponseRedirect(reverse('first_session', kwargs={'activationKey': activation_key}))
                    else:
                        form.add_error(None, "Your data is incorrect.")
                        return render(request, 'page-login.html', {'form': form})

            else:
                form.add_error(None, "Your data is incorrect.")
                return render(request, 'page-login.html', {'form': form})
    else:
        print("Entra en login else")
        form = LoginForm()

    context = {'form': form}
    print("Login a punto de render")
    return render(request, 'page-login.html', context)


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
class FirstSession(TemplateView):
    template_name = 'activation-key-verification.html'

    def activation_key_verification(self, request, *args, **kwargs):
        post_values = request.POST.copy()
        form = ActivationKeyVerificationForm(post_values)
        print(form.is_valid())
        if form.is_valid():
            activation_key = self.kwargs['activationKey']
            user = UserProfile.objects.get(key_activation=activation_key)
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
                return render(request, 'page-login.html', {'form': form})
            else:
                print("else")
                form.add_error(None,'Password do not match, please try again.')
                return render(request, 'activation-key-verification.html', {'form': form})
        else:
            return render(request, 'activation-key-verification.html', {'form': form})
