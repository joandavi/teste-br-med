from django.contrib import admin
from django.urls import path

from .views import currencyApi

urlpatterns = [
   path(
        "currencies",
        currencyApi.as_view(),
        name="rates_list"
    ),
]