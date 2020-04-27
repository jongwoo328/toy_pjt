from django.urls import path
from . import views
from hotdeal import settings

app_name = 'hotdeal'

urlpatterns = [
    path('', views.index, name="index"),
    path('result/', views.result, name="result"),
]
if not settings.DEBUG:
      urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
