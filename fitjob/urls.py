from django.urls import path
from .views import *

app_name = "fitjob"   # ✅ 이거 꼭 있어야 namespace가 생김
urlpatterns = [
    path("", main, name="main"),
    path("board/", board, name="board"),
    path("board/create/", question_create, name="question_create"),
    path("board/<int:question_id>/", question_detail, name="question_detail"),
]