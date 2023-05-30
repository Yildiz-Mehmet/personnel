from django.shortcuts import render
from .serializers import DepartmentSerializer,PersonnelSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Department,Personnel


class DepartmentListView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer



class DepartmentCreateUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class PersonnelListView(ListCreateAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer



class PersonnelCreateUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
