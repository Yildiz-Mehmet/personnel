# first installation stage

- python -m venv env
- source env/bin/activate
- pip install djangorestframework
- pip freeze > requirements.txt

# project need to be build for be setting

# we builded a project called main

- django-admin startproject main .

- settings => Installed_apps => + 'rest_framework'

# to make it work server

- python manage.py runserver

# migrate send django default tables to db.sqlite3 database

- python manage.py migrate

- python manage.py createsuperuser

# before you send githup build .gitignore

# install python-decouple and build .env

- pip install django-decouple

- settings => SECRET_KEY = config("SECRET_KEY")

- from decouple import config

# create the app

- python manage.py startapp personnel

- add installed_apps => + 'personnel',

# create model

- models.py =>

```py
from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name=models.CharField(max_length=32)
    user_id=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    created=models.DateTimeField(auto_now_add= True)
    updated=models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.name

class Personnel(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
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
    department_id = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,related_name='personnel')
    user_id = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    created=models.DateTimeField(auto_now_add= True)
    updated=models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.first_name +'-'+self.last_name

```

# after create models

- python manage.py makemigrations

- python manage.py migrate

# for see in admin

```py
from .models import Department, Personnel

admin.site.register(Department)
admin.site.register(Personnel)


```

# create serializers.py =>

```py
from rest_framework import serializers
from .models import Department,Personnel

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'

class PersonnelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Personnel
        fields = '__all__'


```

# now there is a views.py => we have to make a decision that what will be in view

```py

from django.shortcuts import render
from .serializers import DepartmentSerializer,PersonnelSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Department,Personnel

class DepartmentListCreateView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer



class PersonnelListCreateView(ListCreateAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer


class PersonnelRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer



class DepartmentRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


```

# now there is urls.py => create personnel.urls

```py

from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('personnel.urls')),
]



```

# personnel urls.py =>

```py

from django.urls import path
from .views import DepartmentListCreateView,DepartmentRUDView,PersonnelListCreateView,PersonnelRUDView,DepartmentPersonnelView

urlpatterns = [
    path('departments/',DepartmentListCreateView.as_view()),
    path('departments/<int:pk>/',DepartmentRUDView.as_view()),
    path('personnels/',PersonnelListCreateView.as_view()),
    path('personnels/<int:pk>/',PersonnelRUDView.as_view()),
    # path('department-personnels/',DepartmentPersonnelView.as_view()),
    path('department<str:department>/',DepartmentPersonnelView.as_view()),
]

```

# nested serializers => personnel will lined up under department

# serializers.py =>

```py
class DepartmentPersonnelSerializer(serializers.ModelSerializer):

    personnel = PersonnelSerializer(many=True, read_only=True)
    class Meta:
        model = Department
        fields = '__all__'

```

# views.py =>

```py
class DepartmentPersonnelView(ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentPersonnelSerializer


    def get_queryset(self):

        department = self.kwargs['department']
        return Department.objects.filter(name__iexact=department)
```

# models use related name => python manage.py makemigrations => python manage.py migrate

```py

department_id = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,related_name='personnel')

```

# we will write custom permission

# build permissions.py

```py
from rest_framework.permissions import IsAdminUser,SAFE_METHODS

class IsAdminOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):


        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
```

# add this you want all views

```py
    permission_classes = (
        IsAuthenticated,
        IsAdminOrReadOnly,
    )
```

# others

```py
permission_classes =[IsAuthenticated]

    def put(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:

            return self.update(request, *args, **kwargs)
        data = {
            'message':'You are not authorized to update!'
        }
        return Response(data,status=status.HTTP_401_UNAUTHORİZED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # self.perform_destroy(instance)
        if self.request.user.is_superuser:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {
            'message':'You are not authorized to delete!'
        }
        return Response(data,status=status.HTTP_401_UNAUTHORİZED)


```

# build users for authentication with token

- python manage.py startapp users

```py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

# dj-rest-auth add ınstalled_apps

```py
INSTALLED_APPS = (
    ...,
    'rest_framework',
    'rest_framework.authtoken',
    ...,
    'dj_rest_auth'
)
```

- pip install dj-rest-auth
- python manage.py migrate

# urlpattern add

# main urls.py

```py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('personnel.urls')),
    path('users/',include('users.urls')),
]

```

# users urls.py

```py
from django.urls import path,include
urlpatterns = [
    ...,
    path('auth/', include('dj_rest_auth.urls'))
]

```
