from django.shortcuts import render, HttpResponse
from blog.models import Role, Blog
from django.contrib.auth import authenticate
import json

MainUser = None

def register(request):
    if request.method == "POST":
        raw_user = json.loads(request.body)
        password = raw_user["password"]
        user = Role(name=raw_user["name"], email=raw_user["email"], password=password)
        user.save()
        global MainUser
        MainUser = user
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
        password = raw_user["password"]
        user = Role.objects.get(email=email)
        user_password = user.password
        if user is not None:
            global originalpassword
            if password == user_password:
                global MainUser
                print("ok")
                MainUser = user
                obj = {
                    "name":user.name,
                    "email":user.email,
                }
                return HttpResponse(obj)
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
        obj = {
            "name":user.name,
            "email":user.email,
        }
        return HttpResponse(obj)

def getallblogs(request):
    if request.method == "GET":
        blogs = Blog.objects.all()
        global MainUser
        print(blogs)
        bloglist = []
        for blog in blogs:
            bloglist.append({
            "title":blog.title,
            "imgurl":blog.imgurl,
            "content":blog.content,
            "likes":blog.likes,
            "username":MainUser.name,
            },)
        return HttpResponse(bloglist)

def addblog(request):
    if request.method == "POST":
        raw_blog = json.loads(request.body)
        title = raw_blog["title"]
        imgurl = raw_blog["imgurl"]
        content = raw_blog["content"]
        likes = 0
        global MainUser
        blog = Blog(title=title, imgurl=imgurl,content=content,likes=likes,user=MainUser)
        blog.save()
        bloglist = []
        bloglist.append({
            "title":blog.title,
            "imgurl":blog.imgurl,
            "content":blog.content,
            "likes":blog.likes,
            "username":MainUser.name,
        })
        return HttpResponse(bloglist)

def deleteblog(request):
    if request.method == "DELETE":
        raw_blog = json.loads(request.body)
        title = raw_blog["title"]
        blog = Blog.objects.get(title=title)
        blog.delete()
        return HttpResponse("blog deleted")

def editblog(request):
    if request.method == "PATCH":
        global MainUser
        raw_blog = json.loads(request.body)
        title = raw_blog["title"]
        blog = Blog.objects.get(title=title)
        print(blog)
        blog.title = raw_blog["title"]
        blog.content = raw_blog["content"]
        blog.imgurl = raw_blog["imgurl"]
        blog.save()
        bloglist = []
        bloglist.append({
            "title":blog.title,
            "imgurl":blog.imgurl,
            "content":blog.content,
            "likes":blog.likes,
            "username":MainUser.name,
        })
        return HttpResponse(bloglist)

def likeblog(request):
    if request.method == "PUT":
        raw_blog = json.loads(request.body)
        blog = Blog.objects.get(title=raw_blog["title"])
        blog.likes = blog.likes + 1
        blog.save()
        bloglist = []
        bloglist.append({
            "title":blog.title,
            "imgurl":blog.imgurl,
            "content":blog.content,
            "likes":blog.likes,
            "username":MainUser.name,
        })
        return HttpResponse(bloglist)