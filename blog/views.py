from django.shortcuts import render, HttpResponse
from blog.models import Role
from django.contrib.auth import authenticate
import json
import bcrypt

def register(request):
    if request.method == "POST":
        raw_user = json.loads(request.body)
        password = bcrypt.hashpw(raw_user["password"].encode("utf-8"), bcrypt.gensalt())
        password = password.decode("utf8")
        user = Role(name=raw_user["name"], email=raw_user["email"], password=password)
        user.save()
        obj = {
            "name":user.name,
            "email":user.email,
        }
        print(obj)
        print(HttpResponse(obj))
        return HttpResponse(obj)
    return HttpResponse("ok")

def login(request):
    if request.method == "GET":
        raw_user = json.loads(request.body)
        email = raw_user["email"]
        password = raw_user["password"].encode("utf-8")
        user = Role.objects.get(email=email)
        user_password = user.password
        if user is not None:
            if bcrypt.checkpw(password, user_password.encode("utf-8")):
                return HttpResponse(user)
            else:
                return HttpResponse("wrong password")
        else:
            return HttpResponse("Cannot find user")

def resetpassword(request):
    if request.method == "PUT":
        raw_user = json.loads(request.body)
        email = raw_user["email"]
        new_password = raw_user["new-password"]
        user = Role.objects.get(email=email)
        user.password = new_password
        user.save()
        return HttpResponse(user)