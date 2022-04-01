from unicodedata import name
from django.urls import path
from blog import views

urlpatterns = [
    path("register", views.register, name="register"),
    path("resetpassword",views.resetpassword,name="resetpassword"),
    path("login",views.login, name="login")
]
