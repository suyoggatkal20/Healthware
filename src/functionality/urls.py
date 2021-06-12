from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from functionality import urls as fun_url
from functionality.views import Weight,AddWeight

urlpatterns = [
    path('add_weight/', AddWeight.as_view()),
    path('weight/', Weight.as_view()),
    path('add_weight/', AddWeight.as_view()),
    path('weight/', Weight.as_view()),
]