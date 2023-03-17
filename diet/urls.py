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
]
