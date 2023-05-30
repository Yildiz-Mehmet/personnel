from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name=models.CharField(max_length=32)
    user_id=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    created=models.DataTimeField(auto_now_add= True)
    updated=models.DataTimeField(auto_now= True)

    def __str__(self):
        return self.name
    

class Personnel(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    GENDER = (
        ('F','Female'),
        ('M','Male'),
        ('N','Prefer not to say'),
    )
    gender = models.CharField(max_length=1,choices=GENDER)
    TITLE =(
        ('S','Senior'),
        ('M','Med-Senior'),
        ('J','Junior'),
    )
    title = models.CharField(max_length=1,choices=TITLE)
    salary = models.IntegerField()
    started = models.DateField()
    department_id = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True)
    user_id = 
    created =
    updated =
