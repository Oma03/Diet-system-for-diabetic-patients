from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE

# Create your models here.


class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, null=True)
    surname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    email = models.EmailField()
    number = models.CharField(max_length=11)

    def __str__(self):
        return self.firstname


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
