from django.urls import path
from .views import DataSensor,History,DashBoard,Admin
urlpatterns = [
    path('DataSensor', DataSensor),
    path('History',History),
    path('DashBoard',DashBoard),
    path('Admin',Admin)

]
