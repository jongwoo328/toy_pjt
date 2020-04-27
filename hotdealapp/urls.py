from django.urls import path
from . import views
from hotdeal import settings

app_name = 'hotdeal'

urlpatterns = [
    path('', views.index, name="index"),
    path('result/', views.result, name="result"),
]
if not settings.DEBUG:
      urlpatterns += staticfiles_urlpatterns()
