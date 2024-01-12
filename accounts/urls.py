
from django.contrib import admin
from django.urls import path
from .views import sign_up,sign_in,sign_out
urlpatterns = [
    path("signup/",sign_up,name="signup"),
    path("signin/",sign_in,name="signin"),
    path("signout/",sign_out,name="signout"),
]