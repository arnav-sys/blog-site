from django.db import models


class Role(models.Model):
    name = models.CharField(max_length = 250)
    email = models.CharField(max_length = 250)
    password = models.CharField(max_length = 250)

class Blog(models.Model):
    title = models.CharField(max_length=250)
    imgurl = models.CharField(max_length=700)
    content = models.CharField(max_length=1000000)
    likes = models.IntegerField()
    user = models.ForeignKey(Role,on_delete=models.CASCADE)