from django.shortcuts import render
from .serializers import DepartmentSerializer,PersonnelSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Department,Personnel


class DepartmentListCreateView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer



class DepartmentRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class PersonnelListCreateView(ListCreateAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer



class PersonnelRUDView(RetrieveUpdateDestroyAPIView):
    queryset = Personnel.objects.all()
    serializer_class = PersonnelSerializer
