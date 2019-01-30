from django.urls import path,re_path
from .views import *

app_name = "main"

urlpatterns = [
    path('', main, name="main"),
    path('run', room_segmentation, name="run"),
    re_path(r'sample/(?P<map_name>\w+)/$',sample_view),
    path('xhrTest',xhr_test,name="xhrTest")
]
