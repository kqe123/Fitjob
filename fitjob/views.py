from django.shortcuts import render
from .models import Question
from django.core.paginator import Paginator
def main(request) :
    return render(request, "fitjob/main.html")

def board(request) :
    page = request.GET.get("page", 1) # 페이지 번호 (기본값: 1)
    
    questions = Question.objects.all().order_by("-created_at") # 질문 전체 가져옴 (최신순)

    paginator = Paginator(questions, 10) # 페이지당 10개씩 보여줌.
    page_obj = paginator.get_page(page) # 해당 페이지 객체 가져옴.
    context = {"questions" : page_obj}
    return render(request, "fitjob/board.html", context)

