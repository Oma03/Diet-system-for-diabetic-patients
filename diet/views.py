from django.shortcuts import render
from django.contrib.auth.models import User
from django .contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Contact


# Create your views here.


def home(request):
    return render(request, 'diet/index.html')


def about(request):
    return render(request, 'diet/about.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'diet/signup.html')
    else:
        if request.POST['pass1'] == request.POST['pass2']:
            try:
                User.objects.get(username=request.POST['username'])
                messages.error(request, 'Username is taken')
                return render(request, 'diet/signup.html')
            except:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['pass2'])
                                                # firstname=request.POST['firstname'],
                                                # lastname=request.POST['surname'])

                user.save()
                surname = request.POST.get('surname')
                firstname = request.POST.get('firstname')
                email = request.POST.get('email')
                number = request.POST.get('number')
                contacts = Contact(user=user, surname=surname, firstname=firstname, email=email, number=number, )
                contacts.save()
                login(request, user)
                return render(request, 'diet/index.html')
        else:
            messages.error(request, 'Passwords do not match')
            return render(request, 'diet/signup.html')


def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'diet/loginaccount.html')
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['pass2'])
        if user is None:
            messages.error(request, 'Username and Password do not match')
            return render(request, 'diet/loginaccount.html')
        else:
            login(request, user)
            return render(request, 'diet/index.html')


def logoutaccount(request):
    logout(request)
    return render(request, 'diet/loginaccount.html')


def details(request):

    return render(request, 'diet/details.html')
