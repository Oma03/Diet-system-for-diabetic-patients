from django.shortcuts import render
from django.contrib.auth.models import User
from django .contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Contact, DetailsN


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
            username = request.POST['username']
            email = request.POST['email']
            pass2 = request.POST['pass2']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            try:
                User.objects.get(username=username)
                messages.error(request, 'Username is taken')
                return render(request, 'diet/signup.html')
            except:
                user = User.objects.create_user(username=username, email=email,
                                                password=pass2)
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                surname = request.POST.get('last_name')
                firstname = request.POST.get('first_name')
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
    if request.method == 'GET':
        return render(request, 'diet/details.html')
    else:
        diabetes_type = request.POST['diabetes_type']
        weight = request.POST['weight']
        height = request.POST['height']
        gender = request.POST['gender']
        activity_level = request.POST['activity_level']
        age = request.POST['age']

        details_b = DetailsN(diabetes_type=diabetes_type, weight=weight, height=height, gender=gender,
                             activity_level=activity_level, age=age)
        details_b.save()

    request.session['details_b_saved'] = True

    return render(request, 'diet/details.html')


def bmr(request):

    # Retrieving User's details from the database
    details_n = DetailsN.objects.get(user=request.user)

    # Calculate the user's BMR based on their gender, weight, height, and age
    if details_n.gender == 'Female'.casefold():
        bmr_calc = 447.6 + (9.2 * details_n.weight) + (3.1 * details_n.height) - (4.3 * details_n.age)
    else:
        bmr_calc = 88.36 + (13.4 * details_n.weight) + (4.8 * details_n.height) - (5.7 * details_n.age)

    # Adjust the BMR based on the user's activity level
    if details_n.activity_level == 'Sedentary (little or no exercise)'.casefold():
        daily_calories = bmr_calc * 1.2
    elif details_n.activity_level == 'Lightly active (light exercise 1-3 days per week)'.casefold():
        daily_calories = bmr_calc * 1.375
    elif details_n.activity_level == 'Moderately active (moderate exercise 3-5 days per week)'.casefold():
        daily_calories = bmr_calc * 1.55
    elif details_n.activity_level == 'Very active (hard exercise 6-7 days per week)'.casefold():
        daily_calories = bmr_calc * 1.725
    else:
        daily_calories = bmr_calc * 1.9

    details_s = DetailsN(bmr=bmr_calc, daily_calories=daily_calories)
    details_s.save()

    # Render the calculated values to the user
    context = {
        'bmr_calc': bmr_calc,
        'daily_calories': daily_calories,
    }

    return render(request, 'diet/bmr.html', context)
