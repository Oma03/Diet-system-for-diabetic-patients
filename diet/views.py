from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django .contrib.auth import login, logout, authenticate
from django .contrib.auth.decorators import login_required
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


@ login_required
def details(request):
    if request.method == 'GET':
        return render(request, 'diet/details.html')
    else:
        user = request.user
        has_detail = DetailsN.objects.filter(user=user).exists()
        detail = DetailsN.objects.get(user=user)
        diabetes_type = request.POST['diabetes_type']
        weight = request.POST['weight']
        height = request.POST['height']
        gender = request.POST['gender']
        activity_level = request.POST['activity_level']
        age = request.POST['age']

        # Calculate the user's BMR based on their gender, weight, height, and age
        if gender == 'Female'.casefold():
            bmr_calc = 447.6 + (9.2 * int(weight)) + (3.1 * int(height)) - (4.3 * int(age))
        else:
            bmr_calc = 88.36 + (13.4 * int(weight)) + (4.8 * int(height)) - (5.7 * int(age))

        # Adjust the BMR based on the user's activity level
        if activity_level == 'Sedentary (little or no exercise)'.casefold():
            daily_calories = bmr_calc * 1.2
        elif activity_level == 'Lightly active (light exercise 1-3 days per week)'.casefold():
            daily_calories = bmr_calc * 1.375
        elif activity_level == 'Moderately active (moderate exercise 3-5 days per week)'.casefold():
            daily_calories = bmr_calc * 1.55
        elif activity_level == 'Very active (hard exercise 6-7 days per week)'.casefold():
            daily_calories = bmr_calc * 1.725
        else:
            daily_calories = bmr_calc * 1.9
            details_b = DetailsN(diabetes_type=diabetes_type, weight=weight, height=height, gender=gender,
                                 activity_level=activity_level, age=age, bmr=bmr_calc, daily_calories=daily_calories)
            details_b.save()

        # Render the calculated values to the user
        context = {
            'user': user,
            'has_detail': has_detail,
            'detail': detail,
        }

    return render(request, 'diet/details.html', context)

