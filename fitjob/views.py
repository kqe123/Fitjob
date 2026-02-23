from django.shortcuts import render
from .models import Question
from .forms import QuestionForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import redirect
def main(request) :
    return render(request, "fitjob/main.html")

def board(request) :
    page = request.GET.get("page", 1) # 페이지 번호 (기본값: 1)
    questions = Question.objects.all().order_by("-created_at") # 질문 전체 가져옴 (최신순)
    paginator = Paginator(questions, 10) # 10개씩 보여주는 Paginator 객체 생성
    page_obj = paginator.get_page(page) # 해당 페이지 객체 가져옴.
    user_questions_count = 0 # 해당 유저의 질문 개수 (기본값 : 0)

    if request.user.is_authenticated :
        user_questions_count = Question.objects.filter(user_id=request.user.id).count()
    context = {"questions" : page_obj, "user_question_count": user_questions_count}
    return render(request, "fitjob/board.html", context)

def question_create(request) :
    # 이미 로그인된 상태면 로그인 페이지 접근 불가
    if not request.user.is_authenticated :
        messages.info(request, "로그인 후 이용해주세요.")
        return redirect("user:login")
    
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ 질문이 등록되었습니다.")
            return redirect("fitjob:board")
        # 실패면 그대로 signup 페이지 렌더 (이동 X)
        return render(request, "fitjob/question_create.html", {"form": form})
    return render(request, "fitjob/question_create.html")

def question_detail(request, question_id) :
    question = Question.objects.get(id=question_id)
    user_questions_count = 0 # 해당 유저의 질문 개수 (기본값 : 0)

    if request.user.is_authenticated :
        user_questions_count = Question.objects.filter(user_id=request.user.id).count()
    context = {"question": question, "user_question_count": user_questions_count}
    return render(request, "fitjob/question_detail.html", context)

