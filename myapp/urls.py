from django.urls import path
from .views import *

urlpatterns = [
    path("", provide_attributes, name="provide-attributes"),
    path("dexeval", dex_evaluate, name="dex-eval"),
    path("dexinput", dex_input, name="dex-input"),
    path("dexresult", dex_result, name="dex-result"),
]
