from django.urls import path
from .views import DepartmentListCreateView,DepartmentRUDView,PersonnelListCreateView,PersonnelRUDView

urlpatterns = [
    path('departments/',DepartmentListCreateView.as_view()),
    path('departments/<int:pk>/',DepartmentRUDView.as_view()),
    path('personnels/',PersonnelListCreateView.as_view()),
    path('personnels/<int:pk>/',PersonnelRUDView.as_view()),
    

]