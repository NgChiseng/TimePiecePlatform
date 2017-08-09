from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from users.forms import LoginForm

# Create your views here.

# Function that manage the log in of the users.
#
# @date [09/08/2017]
#
# @author [Chiseng Ng]
#
# @param [HttpRequest] request Request of the page.
#
# @returns [HttpResponse]
def log_in(request):

    if request.user.is_authenticated():
        print("autenticado")

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user_field = request.POST['username']
            password = request.POST['password']
            user_exists = search_user(user_field)

            if user_exists is not None:
                if user_exists.is_active:
                    user_authenticated = authenticate(username=user_exists.username, password=password)

                    if user_authenticated:
                        login(request, user_authenticated)
                        return HttpResponseRedirect('/admin')
                    else:
                        form.add_error(None, "Your data is incorrect.")
                        return render(request, 'page-login.html', {'form': form})
                else:
                    print("no active")

            else:
                form.add_error(None, "Your data is incorrect.")
                return render(request, 'page-login.html', {'form': form})
    else:
        form = LoginForm()

    context = {'form': form}

    return render(request, 'page-login.html', context)


# Function that verify if the user name or email belong to the DataBase.
#
# @date [09/08/2017]
#
# @author [Chiseng Ng]
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
