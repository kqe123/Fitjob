from django.urls import path
from .views import *

app_name = "user"   # ✅ 이거 꼭 있어야 namespace가 생김

urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", signup, name="signup")
]