from django.urls import path
from . import views
app_name = "diet"

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('loginaccount/', views.loginaccount, name='loginaccount'),
    path('logout/', views.logoutaccount, name='logoutaccount'),
    path('details/', views.details, name='details'),
    path('update/', views.update, name='update'),
    path('bmr/', views.bmr, name='bmr'),
    path('create/', views.create, name='create'),
    path('contactus/', views.contactus, name='contactus'),
    path('contactus2/', views.contactus2, name='contactus2'),
    path('testimony/', views.testimony, name='testimony'),
    path('forgot/', views.forgot, name='forgot'),
    path('breakfast/', views.breakfast, name='breakfast'),
    path('breakfast/set_breakfast/<id>', views.set_breakfast, name='set_breakfast'),
    path('lunch/', views.lunch, name='lunch'),
    path('lunch/set_lunch/<id>', views.set_lunch, name='set_lunch'),
    path('snack/', views.snack, name='snack'),
    path('snack/set_snack/<id>', views.set_snack, name='set_snack'),
    path('dinner/', views.dinner, name='dinner'),
    path('dinner/set_dinner/<id>', views.set_dinner, name='set_dinner'),
]
