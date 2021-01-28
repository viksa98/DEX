from django.urls import path
from .views import *

urlpatterns = [
    path('', my_view, name='my-view'),
    path('dexeval', dex_evaluate, name='dex-eval'),
    path('dexinput', dex_input, name='dex-input'),
]
