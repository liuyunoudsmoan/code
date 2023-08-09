from django.db import router
from django.urls import path, include, re_path
from .views import test



urlpatterns = [
    re_path(r'^demo$', test.as_view({'post': 'upload'})),
    re_path(r'^delete$', test.as_view({'post': 'deleteData'})),
    re_path(r'^generate$', test.as_view({'post': 'generate'}))
]