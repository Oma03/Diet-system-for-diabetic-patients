from datetime import timedelta
import pytz as pytz
from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE
from django.utils import timezone

# Create your models here.


class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, null=True)
    surname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    email = models.EmailField()
    number = models.CharField(max_length=11)
    timezone = models.CharField(max_length=100, default='Africa/Lagos')

    def __str__(self):
        return f'{self.firstname}'


class DetailsN(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    diabetes_type = models.CharField(max_length=100)
    weight = models.FloatField()
    height = models.FloatField()
    gender = models.CharField(max_length=50)
    pregnant = models.CharField(max_length=10,  null=True)
    activity_level = models.CharField(max_length=500)
    age = models.IntegerField()
    bmr = models.CharField(max_length=50, null=True)
    bmi = models.CharField(max_length=100, null=True)
    daily_calories = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username


class DCalorie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    carb_grams = models.CharField(max_length=100)
    protein_grams = models.CharField(max_length=100)
    fat_grams = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class FoodList(models.Model):
    Category = models.CharField(max_length=10000)
    LocalName = models.CharField(max_length=20000000)
    EnglishName = models.CharField(max_length=20000000)
    ScientificName = models.CharField(max_length=20000000)
    ENERC_kJ = models.CharField(max_length=20000)
    ENERC_kcal = models.CharField(max_length=20000)
    WATER_g = models.CharField(max_length=20000)
    PROTCNT_g = models.CharField(max_length=20000)
    FATCE_g = models.CharField(max_length=20000)
    CHOCDF_g = models.CharField(max_length=20000)
    FIB_g = models.CharField(max_length=20000)
    ASH_g = models.CharField(max_length=20000)
    Ca_mg = models.CharField(max_length=20000)
    Fe_mg = models.CharField(max_length=20000)
    Mg_mg = models.CharField(max_length=20000)
    P_mg = models.CharField(max_length=20000)
    K_mg = models.CharField(max_length=20000)
    Na_mg = models.CharField(max_length=20000)
    Zn_mg = models.CharField(max_length=20000)
    Cu_mg = models.CharField(max_length=20000)
    Mn_mg = models.CharField(max_length=20000)
    VIT_A_RAE_mcg = models.CharField(max_length=20000)
    RETOL_mcg = models.CharField(max_length=20000)
    CARTB_mcg = models.CharField(max_length=20000)
    VITDEQ_mcg = models.CharField(max_length=20000)
    VITE_mg = models.CharField(max_length=20000)
    THIA_mg = models.CharField(max_length=20000)
    RIBF_mg = models.CharField(max_length=20000)
    NIAEQ_mg = models.CharField(max_length=20000)
    VIT_B6_mg = models.CharField(max_length=20000)
    FOL_mcg = models.CharField(max_length=20000)
    VITB12_mcg = models.CharField(max_length=20000)
    VITC_mg = models.CharField(max_length=20000)
    SearchName = models.CharField(max_length=2000000000)

    def __str__(self):
        return self.EnglishName


class MealPlan(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    week_id = models.IntegerField(unique=True)
    day = models.CharField(max_length=10, default=timezone.now().strftime('%A'), choices=DAY_CHOICES)
    breakfast = models.CharField(max_length=100)
    lunch = models.CharField(max_length=100)
    snack = models.CharField(max_length=100)
    dinner = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_week_id(self):
        user_tz = pytz.timezone(self.user.Contact.timezone)
        start_date = (self.created_at.astimezone(user_tz) - timedelta(
            days=self.created_at.astimezone(user_tz).weekday())).date()
        current_date = timezone.now().astimezone(user_tz).date()
        week_number = (current_date - start_date).days // 7 + 1
        if week_number < 1:
            # If the user creates a meal plan for a previous week, set the week number to the current week (week 1)
            week_number = 1
        return week_number

    def save(self, *args, **kwargs):
        if not self.week_id:
            self.week_id = self.generate_week_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.day
