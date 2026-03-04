from django.urls import path
from .views import *

app_name = "fitjob"   # ✅ 이거 꼭 있어야 namespace가 생김
urlpatterns = [
    path("", main, name="main"),
    path("board/", board, name="board"),
    path("board/question_create/", question_create, name="question_create"),
    path("board/question_delete/<int:question_id>/", question_delete, name="question_delete"),
    path("board/answer_create/<int:question_id>/", answer_create, name="answer_create"),
    path("board/answer_delete/<int:answer_id>/<int:question_id>/", answer_delete, name="answer_delete"),
    path("board/<int:question_id>/", question_detail, name="question_detail"),
    path("board/question_report/<int:question_id>/", question_report, name="report_question"),
    path("board/answer_report/<int:answer_id>/<int:question_id>", answer_report, name="report_answer"),
    path("interview/", interview, name="interview"),
    path("coverletter/", coverletter, name="coverletter"),
]