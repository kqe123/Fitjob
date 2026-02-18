from django.urls import path
from .views import *

app_name = "user"   # ✅ 이거 꼭 있어야 namespace가 생김

urlpatterns = [
    path("login/", login_try, name="login"),
    path("signup/", signup_try, name="signup"),
    path("logout/", logout_try, name="logout")
]

