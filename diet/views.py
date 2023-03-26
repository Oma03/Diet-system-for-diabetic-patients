from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django .contrib.auth import login, logout, authenticate
from django .contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Contact, DetailsN, DCalorie, MealPlan, FoodList, ContactUs, Testimonial, Doctors


# Create your views here.


def home(request):
    items = Testimonial.objects.all()
    return render(request, 'diet/index.html', {'items': items})


def about(request):
    items = Testimonial.objects.all()
    return render(request, 'diet/about.html', {'items': items})


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
                contacts = Contact(user=user, timezone='Africa/Lagos', surname=surname, firstname=firstname, email=email,
                                   number=number, )
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
    items = Testimonial.objects.all()
    # try:
    #     details_b = DetailsN.objects.filter(user=request.user).first()
    #     details_c = DCalorie.objects.filter(user=request.user).first()
    #     saved = True
    # except DetailsN.DoesNotExist:
    #     saved = False
    #     details_b = None
    #
    # if details_b is not None:
    #     return render(request, 'diet/bmr.html', {'details_b': details_b, 'details_c': details_c})
    # else:

    if request.method == 'GET':
        return render(request, 'diet/details.html')
    else:
        diabetes_type = request.POST['diabetes_type']
        weight = request.POST['weight']
        height = request.POST['height']
        gender = request.POST['gender']
        pregnant = request.POST['pregnant']
        activity_level = request.POST['activity_level']
        age = request.POST['age']

        # Calculate the user's BMI
        bmi = round(int(weight) / ((int(height) / 100) ** 2))

        # Adjust factor based on BMI
        if bmi < 18.5:  # Underweight
            factor = 1.2
        elif 18.5 <= bmi < 25:  # Normal weight
            factor = 1.0
        elif 25 <= bmi < 30:  # Overweight
            factor = 0.8
        else:  # Obese
            factor = 0.6

        # Calculate the user's BMR based on their gender, weight, height, and age
        if gender == 'Female'.casefold():
            bmr_calc = round(447.6 + (9.2 * int(weight)) + (3.1 * int(height)) - (4.3 * int(age)))
        else:
            bmr_calc = round(88.36 + (13.4 * int(weight)) + (4.8 * int(height)) - (5.7 * int(age)))

        # Adjust the BMR based on the user's activity level
        if activity_level == 'Sedentary (little or no exercise)'.casefold():
            daily_calories = round(bmr_calc * 1.2 * factor)
        elif activity_level == 'Lightly active (light exercise 1-3 days per week)'.casefold():
            daily_calories = round(bmr_calc * 1.375 * factor)
        elif activity_level == 'Moderately active (moderate exercise 3-5 days per week)'.casefold():
            daily_calories = round(bmr_calc * 1.55 * factor)
        elif activity_level == 'Very active (hard exercise 6-7 days per week)'.casefold():
            daily_calories = round(bmr_calc * 1.725 * factor)
        else:
            daily_calories = round(bmr_calc * 1.9 * factor)

        # calculate macronutrient breakdown based on diabetes type
        if diabetes_type == 'type1':
            carb_percentage = 45
            protein_percentage = 20
            fat_percentage = 35
        elif diabetes_type == 'type2':
            carb_percentage = 40
            protein_percentage = 30
            fat_percentage = 30
        else:
            carb_percentage = 50
            protein_percentage = 25
            fat_percentage = 25

        # adjust macronutrient breakdown for pregnant people
        if pregnant == 'yes':
            carb_percentage += 5
            protein_percentage += 5
            fat_percentage -= 10

        # calculate calories and macros based on macronutrient breakdown
        carb_grams = round(daily_calories * (carb_percentage / 100) / 4)
        protein_grams = round(daily_calories * (protein_percentage / 100) / 4)
        fat_grams = round(daily_calories * (fat_percentage / 100) / 9)
        meal_carb_gram = round(carb_grams/4)
        meal_protein_gram = round(protein_grams/4)
        meal_fat_gram = round(fat_grams/4)

        details_b = DetailsN(user=request.user, diabetes_type=diabetes_type, weight=weight, height=height,
                             gender=gender, pregnant=pregnant, activity_level=activity_level, age=age,
                             bmr=bmr_calc, bmi=bmi, daily_calories=daily_calories)
        details_b.save()
        saved = True

        details_c = DCalorie(user=request.user, carb_grams=carb_grams, protein_grams=protein_grams,
                             fat_grams=fat_grams, meal_carb_gram=meal_carb_gram, meal_protein_gram=meal_protein_gram,
                             meal_fat_gram=meal_fat_gram)
        details_c.save()

        # if details_b is saved:
        #     return render(request, 'diet/bmr.html', {'details_b': details_b, 'details_c': details_c})

    return render(request, 'diet/details.html', {'details_b': details_b, 'saved': saved, 'items': items})


def bmr(request):
    items = Testimonial.objects.all()
    return render(request, 'diet/bmr.html', {'items': items})


def update(request):
    if request.method == 'GET':
        return render(request, 'diet/update.html')
    else:
        diabetes_type = request.POST['diabetes_type']
        weight = request.POST['weight']
        height = request.POST['height']
        gender = request.POST['gender']
        pregnant = request.POST['pregnant']
        activity_level = request.POST['activity_level']
        age = request.POST['age']

        # Calculate the user's BMI
        bmi = round(int(weight) / ((int(height) / 100) ** 2))

        # Adjust factor based on BMI
        if bmi < 18.5:  # Underweight
            factor = 1.2
        elif 18.5 <= bmi < 25:  # Normal weight
            factor = 1.0
        elif 25 <= bmi < 30:  # Overweight
            factor = 0.8
        else:  # Obese
            factor = 0.6

        # Calculate the user's BMR based on their gender, weight, height, and age
        if gender == 'Female'.casefold():
            bmr_calc = round(447.6 + (9.2 * int(weight)) + (3.1 * int(height)) - (4.3 * int(age)))
        else:
            bmr_calc = round(88.36 + (13.4 * int(weight)) + (4.8 * int(height)) - (5.7 * int(age)))

        # Adjust the BMR based on the user's activity level
        if activity_level == 'Sedentary (little or no exercise)'.casefold():
            daily_calories = round(bmr_calc * 1.2 * factor)
        elif activity_level == 'Lightly active (light exercise 1-3 days per week)'.casefold():
            daily_calories = round(bmr_calc * 1.375 * factor)
        elif activity_level == 'Moderately active (moderate exercise 3-5 days per week)'.casefold():
            daily_calories = round(bmr_calc * 1.55 * factor)
        elif activity_level == 'Very active (hard exercise 6-7 days per week)'.casefold():
            daily_calories = round(bmr_calc * 1.725 * factor)
        else:
            daily_calories = round(bmr_calc * 1.9 * factor)

        # calculate macronutrient breakdown based on diabetes type
        if diabetes_type == 'type1':
            carb_percentage = 45
            protein_percentage = 20
            fat_percentage = 35
        elif diabetes_type == 'type2':
            carb_percentage = 40
            protein_percentage = 30
            fat_percentage = 30
        else:
            carb_percentage = 50
            protein_percentage = 25
            fat_percentage = 25

        # adjust macronutrient breakdown for pregnant people
        if pregnant == 'yes':
            carb_percentage += 5
            protein_percentage += 5
            fat_percentage -= 10

        # calculate calories and macros based on macronutrient breakdown
        carb_grams = round(daily_calories * (carb_percentage / 100) / 4)
        protein_grams = round(daily_calories * (protein_percentage / 100) / 4)
        fat_grams = round(daily_calories * (fat_percentage / 100) / 9)
        meal_carb_gram = round(carb_grams / 4)
        meal_protein_gram = round(protein_grams / 4)
        meal_fat_gram = round(fat_grams / 4)

        details_b = DetailsN.objects.filter(user=request.user).first()
        details_c = DCalorie.objects.filter(user=request.user).first()

        details_b.update(user=request.user, diabetes_type=diabetes_type, weight=weight, height=height,
                         gender=gender, pregnant=pregnant, activity_level=activity_level, age=age, bmr=bmr_calc,
                         bmi=bmi, daily_calories=daily_calories)
        details_b.save()

        details_c.update(user=request.user, carb_grams=carb_grams, protein_grams=protein_grams, fat_grams=fat_grams,
                         meal_carb_gram=meal_carb_gram, meal_protein_gram=meal_protein_gram,
                         meal_fat_gram=meal_fat_gram)
        details_c.save()

    return render(request, 'diet/bmr.html', {'details_b': details_b, 'details_c': details_c})


def create(request):
    itemss = Testimonial.objects.all()
    items = FoodList.objects.all()
    calories = DCalorie.objects.get(user=request.user)
    searchTerm = request.GET.get('search_food')
    current_time = timezone.now()
    current_day = current_time.strftime('%A')
    # if request.method == 'POST':
    #     meal_plan = MealPlan(user=request.user, day=current_day,
    #                          breakfast=request.POST['breakfast'],
    #                          lunch=request.POST['lunch'],
    #                          snack=request.POST['snack'],
    #                          dinner=request.POST['dinner'])
    #     meal_plan.save()
    #     # return HttpResponseRedirect('weekly_meal_plan')

    return render(request, 'diet/create.html', {'searchTerm': searchTerm, 'current_time': current_time,
                                                'current_day': current_day, 'calories': calories,
                                                'items': items, 'itemss': itemss})


def contactus(request):
    if request.method == 'GET':
        return render(request, 'diet/contactus.html')
    else:
        lastname = request.POST['lastname']
        firstname = request.POST['firstname']
        email = request.POST['email']
        gender = request.POST['gender']
        feedback = request.POST['feedback']

        contact = ContactUs(lastname=lastname, firstname=firstname, email=email, gender=gender, feedback=feedback)
        contact.save()

        send_mail(f'New feedback from {firstname}', f'Email: {email}\n\nMessage: {feedback}',  # message
                  email,  # from_email
                  ['dietdoctorproject@gmail.com'],  # recipient_list
                  fail_silently=False,
                  )

        messages.success(request, 'Feedback received')
        return render(request, 'diet/contactus.html')


def contactus2(request):
    doctors = Doctors.objects.all()
    # if request.method == 'GET':
    #     return render(request, 'diet/contactus2.html')
    # else:
    #     detailss = DetailsN.objects.get(user=request.user)
        # send_mail(f'New feedback from {username}', f'Email: {email}\n\nMessage: {feedback}',  # message
        #           email,  # from_email
        #           ['dietdoctorproject@gmail.com'],  # recipient_list
        #           fail_silently=False,
        #           )

        # messages.success(request, 'Feedback received')
    return render(request, 'diet/contactus2.html', {'doctors': doctors})


def testimony(request):
    items = Testimonial.objects.all()
    if request.method == 'GET':
        return render(request, 'diet/testimonial.html')
    else:
        email = request.POST['email']
        feedback = request.POST['feedback']

        testimony_u = Testimonial(user=request.user, email=email, feedback=feedback)
        testimony_u.save()

        messages.success(request, 'Feedback received, Thank you!!!')
        return render(request, 'diet/testimonial.html', {'items': items})


def breakfast(request):
    # items_search = FoodList.objects.filter('SearchName').first()
    items = FoodList.objects.all()
    calories = DCalorie.objects.get(user=request.user)
    current_time = timezone.now()
    current_day = current_time.strftime('%A')
    query = request.GET.get('search_food')
    if query:
        results = FoodList.objects.filter(SearchName__icontains=query).first()
    else:
        results = []
        messages.error(request, 'No items found')
    # else:
    #     meal_plan = MealPlan(user=request.user, day=current_day, breakfast=request.POST['breakfast'])
    return render(request, 'diet/breakfast.html', {'current_time': current_time, 'current_day': current_day,
                                                   'calories': calories, 'items': items, 'results': results})
