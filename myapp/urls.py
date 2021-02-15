from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("", my_view, name="my-view"),
    path("dexeval", dex_evaluate, name="dex-eval"),
    path("dexinput", dex_input, name="dex-input"),
    path("hand", hand, name="hand"),
    re_path("^skills/(?P<skp_code>\d+\.\d+)/$", get_skills, name="get_skills"),
    path("handeval/", handeval, name="handeval"),
    path("test", skp_view, name = 'skp-view'),
    path("eval_hecat_dex", eval_hecat_dex, name = 'eval_hecat_dex'),
]
