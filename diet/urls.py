from django.urls import path
from . import views
from .views import details
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
]
