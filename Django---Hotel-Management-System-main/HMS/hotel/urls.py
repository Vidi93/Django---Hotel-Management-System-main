from django.urls import path
from . import views

urlpatterns = [
    path('reports/<str:report_type>/', views.generate_report, name='generate_report'),
]