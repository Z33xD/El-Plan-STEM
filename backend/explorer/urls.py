from django.urls import path
from . import views

urlpatterns = [
    path('explorer/',views.dataexp),
]