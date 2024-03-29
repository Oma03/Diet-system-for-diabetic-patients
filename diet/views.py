from django.shortcuts import redirect, render
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


def forgot(request):
    if request.method == 'GET':
        return render(request, 'diet/forgot.html')
    else:
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        user = authenticate(email=email)
        if user is not None:
            if pass1 == pass2:
                user.set_password(pass2)
                user.save()
                messages.success(request, 'Password successfully changed')
                return render(request, 'diet/index.html')
            else:
                messages.error(request, 'Passwords do not match')
                return render(request, 'diet/forgot.html')
        else:
            messages.error(request, 'Invalid email')
            return render(request, 'diet/forgot.html')


def logoutaccount(request):
    logout(request)
    return render(request, 'diet/loginaccount.html')


@ login_required
def details(request):
    items = Testimonial.objects.all()
    try:
        details_b = DetailsN.objects.filter(user=request.user).first()
        details_c = DCalorie.objects.filter(user=request.user).first()

    except DetailsN.DoesNotExist and DCalorie.DoesNotExist:
        details_b = None
        details_c = None

    if details_b and details_c is not None:
        return render(request, 'diet/bmr.html', {'details_b': details_b, 'details_c': details_c})

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
            bmr_calc = round(447.6 + (9.2 * int(weight)) +
                             (3.1 * int(height)) - (4.3 * int(age)))
        else:
            bmr_calc = round(88.36 + (13.4 * int(weight)) +
                             (4.8 * int(height)) - (5.7 * int(age)))

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

        details_c = DCalorie(user=request.user, carb_grams=carb_grams, protein_grams=protein_grams,
                             fat_grams=fat_grams, meal_carb_gram=meal_carb_gram, meal_protein_gram=meal_protein_gram,
                             meal_fat_gram=meal_fat_gram)

        try:
            details_b.save()
            details_c.save()
            saved = True

        except:
            saved = False

        if saved:
            return render(request, 'diet/bmr.html', {'details_b': details_b, 'details_c': details_c})

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
            bmr_calc = round(447.6 + (9.2 * int(weight)) +
                             (3.1 * int(height)) - (4.3 * int(age)))
        else:
            bmr_calc = round(88.36 + (13.4 * int(weight)) +
                             (4.8 * int(height)) - (5.7 * int(age)))

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

        details_b = DetailsN.objects.filter(user=request.user)
        details_c = DCalorie.objects.filter(user=request.user)

        details_b.update(user=request.user, diabetes_type=diabetes_type, weight=weight, height=height,
                         gender=gender, pregnant=pregnant, activity_level=activity_level, age=age, bmr=bmr_calc,
                         bmi=bmi, daily_calories=daily_calories)

        details_c.update(user=request.user, carb_grams=carb_grams, protein_grams=protein_grams, fat_grams=fat_grams,
                         meal_carb_gram=meal_carb_gram, meal_protein_gram=meal_protein_gram,
                         meal_fat_gram=meal_fat_gram)

        try:
            for detail_b in details_b:
                detail_b.save()

            for detail_c in details_c:
                detail_c.save()
            saved = True

        except:
            saved = False

        if saved:
            return redirect('diet:details')

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

        contact = ContactUs(lastname=lastname, firstname=firstname,
                            email=email, gender=gender, feedback=feedback)
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

    if request.method == 'GET':
        return render(request, 'diet/contactus2.html', {'doctors': doctors})
    else:
        detailss = DetailsN.objects.get(user=request.user)
        username = request.POST['username']
        email = request.POST['email']
        feedback = request.POST['feedback']

        try:
            send_mail(f'New feedback from {username}', f'Email: {email}\n\nMessage: {feedback}',  # message
                      email,  # from_email
                      ['ogunmetimilehin@gmail.com'],  # recipient_list
                      fail_silently=False,
                      )
            print('success')

            messages.success(request, 'Feedback received')
        except Exception as e:
            print(e)

            messages.error(request, 'Something went wrong')
    return render(request, 'diet/contactus2.html', {'doctors': doctors, 'detailss': detailss})


def testimony(request):
    items = Testimonial.objects.all()
    if request.method == 'GET':
        return render(request, 'diet/testimonial.html')
    else:
        email = request.POST['email']
        feedback = request.POST['feedback']

        testimony_u = Testimonial(
            user=request.user, email=email, feedback=feedback)
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
        results = FoodList.objects.filter(SearchName__icontains=query)

    else:
        print('not items')
        query = ""
        results = []
        messages.error(request, 'No items found')

    current_breakfast = ""

    try:
        current_breakfast = MealPlan.objects.get(user=request.user).breakfast
    except Exception as e:
        print(e)

    return render(request, 'diet/breakfast.html', {'current_time': current_time, 'current_day': current_day,
                                                   'calories': calories, 'items': items, 'results': results,
                                                   "current_breakfast": current_breakfast, "query": query})


def set_breakfast(request, id):
    user = request.user

    food_items = FoodList.objects.get(id=id)
    current_time = timezone.now()
    current_day = current_time.strftime('%A')
    calories = DCalorie.objects.get(user=user)
    try:
        meal_plan = MealPlan.objects.get(user=user)
    except MealPlan.DoesNotExist:
        test = calories.meal_carb_gram
        test1 = food_items.CHOCDF_g
        if test1 <= test:
            new_calories = float(test) - float(test1)
            calories.update_meal_carb_gram(round(new_calories))
            messages.success(request, f'{test1} amount used, {new_calories} remains')
        else:
            messages.error(request, 'The meal has a larger carbohydrate gram '
                                    'than your required meal carbohydrate gram.')
        test2 = calories.meal_protein_gram
        test3 = food_items.PROTCNT_g
        if test3 <= test2:
            new_calories = float(test2) - float(test3)
            calories.update_meal_protein_gram(round(new_calories))
            messages.success(request, f'{test3} amount used, {new_calories} remains')
        else:
            messages.error(request, 'The meal has a larger protein gram '
                                    'than your required meal protein gram.')
        test4 = calories.meal_fat_gram
        test5 = food_items.FATCE_g
        if test5 <= test4:
            new_calories = float(test4) - float(test5)
            calories.update_meal_fat_gram(round(new_calories))
            messages.success(request, f'{test5} amount used, {new_calories} remains')
        else:
            messages.error(request, 'The meal has a larger fat gram '
                                    'than your required meal fat gram.')

        meal_plan = MealPlan(user=user, week_id=1, day=current_day, breakfast=food_items, lunch=None, snack=None,
                             dinner=None)
        meal_plan.save()
    test = calories.meal_carb_gram
    test1 = food_items.CHOCDF_g
    if test1 <= test:
        new_calories = float(test) - float(test1)
        calories.update_meal_carb_gram(round(new_calories))
        messages.success(request, f'{test1} amount used, {new_calories} remains')
    else:
        messages.error(request, 'The meal has a larger carbohydrate gram than your required meal carbohydrate gram.')
    test2 = calories.meal_protein_gram
    test3 = food_items.PROTCNT_g
    if test3 <= test2:
        new_calories = float(test2) - float(test3)
        calories.update_meal_protein_gram(round(new_calories))
        messages.success(request, f'{test3} amount used, {new_calories} remains')
    else:
        messages.error(request, 'The meal has a larger protein gram than your required meal protein gram.')
    test4 = calories.meal_fat_gram
    test5 = food_items.FATCE_g
    if test5 <= test4:
        new_calories = float(test4) - float(test5)
        calories.update_meal_fat_gram(round(new_calories))
        messages.success(request, f'{test5} amount used, {new_calories} remains')
    else:
        messages.error(request, 'The meal has a larger fat gram than your required meal fat gram.')

    meal_plan.update_breakfast(food_items)

    return redirect('diet:breakfast')


def lunch(request):
    items = FoodList.objects.all()
    calories = DCalorie.objects.get(user=request.user)
    current_time = timezone.now()
    current_day = current_time.strftime('%A')
    query = request.GET.get('search_food')

    if query:
        results = FoodList.objects.filter(SearchName__icontains=query)

    else:
        print('not items')
        query = ""
        results = []
        messages.error(request, 'No items found')

    current_lunch = ""

    try:
        current_lunch = MealPlan.objects.get(user=request.user).lunch
    except Exception as e:
        print(e)

    return render(request, 'diet/lunch.html', {'current_time': current_time, 'current_day': current_day,
                                               'calories': calories, 'items': items, 'results': results,
                                               "current_lunch": current_lunch, "query": query})


def set_lunch(request, id):
    user = request.user

    food_items = FoodList.objects.get(id=id)
    current_time = timezone.now()
    current_day = current_time.strftime('%A')
    calories = DCalorie.objects.get(user=user)
    try:
        meal_plan = MealPlan.objects.get(user=user)
    except MealPlan.DoesNotExist:
        test = calories.meal_carb_gram
        test1 = food_items.CHOCDF_g
        if test1 <= test:
            new_calories = float(test) - float(test1)
            calories.update_meal_carb_gram(round(new_calories))
            messages.success(request, f'{test1} amount used, {new_calories} remains')
        else:
            messages.error(request,
                           'The meal has a larger carbohydrate gram than your required meal carbohydrate gram.')
        test2 = calories.meal_protein_gram
        test3 = food_items.PROTCNT_g
        if test3 <= test2:
            new_calories = float(test2) - float(test3)
            calories.update_meal_protein_gram(round(new_calories))
            messages.success(request, f'{test3} amount used, {new_calories} remains')
        else:
            messages.error(request, 'The meal has a larger protein gram than your required meal protein gram.')
        test4 = calories.meal_fat_gram
        test5 = food_items.FATCE_g
        if test5 <= test4:
            new_calories = float(test4) - float(test5)
            calories.update_meal_fat_gram(round(new_calories))
            messages.success(request, f'{test5} amount used, {new_calories} remains')
        else:
            messages.error(request, 'The meal has a larger fat gram than your required meal fat gram.')
        meal_plan = MealPlan(user=user, week_id=1, day=current_day, breakfast=None, lunch=food_items, snack=None,
                             dinner=None)
        meal_plan.save()
    test = calories.meal_carb_gram
    test1 = food_items.CHOCDF_g
    if test1 <= test:
        new_calories = float(test) - float(test1)
        calories.update_meal_carb_gram(round(new_calories))
        messages.success(request, f'{test1} amount used, {new_calories} remains')
    else:
        messages.error(request, 'The meal has a larger carbohydrate gram than your required meal carbohydrate gram.')
    test2 = calories.meal_protein_gram
    test3 = food_items.PROTCNT_g
    if test3 <= test2:
        new_calories = float(test2) - float(test3)
        calories.update_meal_protein_gram(round(new_calories))
        messages.success(request, f'{test3} amount used, {new_calories} remains')
    else:
        messages.error(request, 'The meal has a larger protein gram than your required meal protein gram.')
    test4 = calories.meal_fat_gram
    test5 = food_items.FATCE_g
    if test5 <= test4:
        new_calories = float(test4) - float(test5)
        calories.update_meal_fat_gram(round(new_calories))
        messages.success(request, f'{test5} amount used, {new_calories} remains')
    else:
        messages.error(request, 'The meal has a larger fat gram than your required meal fat gram.')
    meal_plan.update_lunch(food_items)

    return redirect('diet:lunch')


def snack(request):
    items = FoodList.objects.all()
    calories = DCalorie.objects.get(user=request.user)
    current_time = timezone.now()
    current_day = current_time.strftime('%A')
    query = request.GET.get('search_food')

    if query:
        results = FoodList.objects.filter(SearchName__icontains=query)

    else:
        print('not items')
        query = ""
        results = []
        messages.error(request, 'No items found')

    current_snack = ""

    try:
        current_snack = MealPlan.objects.get(user=request.user).snack
    except Exception as e:
        print(e)

    return render(request, 'diet/snack.html', {'current_time': current_time, 'current_day': current_day,
                                               'calories': calories, 'items': items, 'results': results,
                                               "current_snack": current_snack, "query": query})


def set_snack(request, id):
    user = request.user

    food_items = FoodList.objects.get(id=id)
    current_time = timezone.now()
    current_day = current_time.strftime('%A')
    calories = DCalorie.objects.get(user=user)
    try:
        meal_plan = MealPlan.objects.get(user=user)
    except MealPlan.DoesNotExist:
        test = calories.meal_carb_gram
        test1 = food_items.CHOCDF_g
        if test1 <= test:
            new_calories = float(test) - float(test1)
            calories.update_meal_carb_gram(round(new_calories))
            messages.success(request, f'{test1} amount used, {new_calories} remains')
        else:
            messages.error(request,
                           'The meal has a larger carbohydrate gram than your required meal carbohydrate gram.')
        test2 = calories.meal_protein_gram
        test3 = food_items.PROTCNT_g
        if test3 <= test2:
            new_calories = float(test2) - float(test3)
            calories.update_meal_protein_gram(round(new_calories))
            messages.success(request, f'{test3} amount used, {new_calories} remains')
        else:
            messages.error(request, 'The meal has a larger protein gram than your required meal protein gram.')
        test4 = calories.meal_fat_gram
        test5 = food_items.FATCE_g
        if test5 <= test4:
            new_calories = float(test4) - float(test5)
            calories.update_meal_fat_gram(round(new_calories))
            messages.success(request, f'{test5} amount used, {new_calories} remains')
        else:
            messages.error(request, 'The meal has a larger fat gram than your required meal fat gram.')
        meal_plan = MealPlan(user=user, week_id=1, day=current_day, breakfast=None, lunch=None, snack=food_items,
                             dinner=None)
        meal_plan.save()
    test = calories.meal_carb_gram
    test1 = food_items.CHOCDF_g
    if test1 <= test:
        new_calories = float(test) - float(test1)
        calories.update_meal_carb_gram(round(new_calories))
        messages.success(request, f'{test1} amount used, {new_calories} remains')
    else:
        messages.error(request, 'The meal has a larger carbohydrate gram than your required meal carbohydrate gram.')
    test2 = calories.meal_protein_gram
    test3 = food_items.PROTCNT_g
    if test3 <= test2:
        new_calories = float(test2) - float(test3)
        calories.update_meal_protein_gram(round(new_calories))
        messages.success(request, f'{test3} amount used, {new_calories} remains')
    else:
        messages.error(request, 'The meal has a larger protein gram than your required meal protein gram.')
    test4 = calories.meal_fat_gram
    test5 = food_items.FATCE_g
    if test5 <= test4:
        new_calories = float(test4) - float(test5)
        calories.update_meal_fat_gram(round(new_calories))
        messages.success(request, f'{test5} amount used, {new_calories} remains')
    else:
        messages.error(request, 'The meal has a larger fat gram than your required meal fat gram.')
    meal_plan.update_snack(food_items)

    return redirect('diet:snack')


def dinner(request):
    items = FoodList.objects.all()
    calories = DCalorie.objects.get(user=request.user)
    current_time = timezone.now()
    current_day = current_time.strftime('%A')
    query = request.GET.get('search_food')

    if query:
        results = FoodList.objects.filter(SearchName__icontains=query)

    else:
        print('not items')
        query = ""
        results = []
        messages.error(request, 'No items found')

    current_dinner = ""

    try:
        current_dinner = MealPlan.objects.get(user=request.user).dinner
    except Exception as e:
        print(e)

    return render(request, 'diet/dinner.html', {'current_time': current_time, 'current_day': current_day,
                                               'calories': calories, 'items': items, 'results': results,
                                               "current_dinner": current_dinner, "query": query})


def set_dinner(request, id):
    user = request.user

    food_items = FoodList.objects.get(id=id)
    current_time = timezone.now()
    current_day = current_time.strftime('%A')
    calories = DCalorie.objects.get(user=user)
    try:
        meal_plan = MealPlan.objects.get(user=user)
    except MealPlan.DoesNotExist:
        test = calories.meal_carb_gram
        test1 = food_items.CHOCDF_g
        if test1 <= test:
            new_calories = float(test) - float(test1)
            calories.update_meal_carb_gram(round(new_calories))
            messages.success(request, f'{test1} amount used, {new_calories} remains')
        else:
            messages.error(request,
                           'The meal has a larger carbohydrate gram than your required meal carbohydrate gram.')
        test2 = calories.meal_protein_gram
        test3 = food_items.PROTCNT_g
        if test3 <= test2:
            new_calories = float(test2) - float(test3)
            calories.update_meal_protein_gram(round(new_calories))
            messages.success(request, f'{test3} amount used, {new_calories} remains')
        else:
            messages.error(request, 'The meal has a larger protein gram than your required meal protein gram.')
        test4 = calories.meal_fat_gram
        test5 = food_items.FATCE_g
        if test5 <= test4:
            new_calories = float(test4) - float(test5)
            calories.update_meal_fat_gram(round(new_calories))
            messages.success(request, f'{test5} amount used, {new_calories} remains')
        else:
            messages.error(request, 'The meal has a larger fat gram than your required meal fat gram.')
        meal_plan = MealPlan(user=user, week_id=1, day=current_day, breakfast=None, lunch=None, snack=None,
                             dinner=food_items)
        meal_plan.save()
    test = calories.meal_carb_gram
    test1 = food_items.CHOCDF_g
    if test1 <= test:
        new_calories = float(test) - float(test1)
        calories.update_meal_carb_gram(round(new_calories))
        messages.success(request, f'{test1} amount used, {new_calories} remains')
    else:
        messages.error(request, 'The meal has a larger carbohydrate gram than your required meal carbohydrate gram.')
    test2 = calories.meal_protein_gram
    test3 = food_items.PROTCNT_g
    if test3 <= test2:
        new_calories = float(test2) - float(test3)
        calories.update_meal_protein_gram(round(new_calories))
        messages.success(request, f'{test3} amount used, {new_calories} remains')
    else:
        messages.error(request, 'The meal has a larger protein gram than your required meal protein gram.')
    test4 = calories.meal_fat_gram
    test5 = food_items.FATCE_g
    if test5 <= test4:
        new_calories = float(test4) - float(test5)
        calories.update_meal_fat_gram(round(new_calories))
        messages.success(request, f'{test5} amount used, {new_calories} remains')
    else:
        messages.error(request, 'The meal has a larger fat gram than your required meal fat gram.')
    meal_plan.update_dinner(food_items)

    return redirect('diet:dinner')


def weekly_plan(request):
    meal_plan = MealPlan.objects.get(user=request.user)

