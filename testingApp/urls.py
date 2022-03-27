from django.urls import path
from . import views

urlpatterns = [
    path('complaint', views.handle_complaint_page),
    path('display', views.handle_comp_submission)
]