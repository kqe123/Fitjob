from django.shortcuts import render
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

def main(request) :
    return render(request, "fitjob/main.html")

def board(request) :
    page = request.GET.get("page", 1) # 페이지 번호 (기본값: 1)
    questions = Question.objects.all().order_by("-created_at") # 질문 전체 가져옴 (최신순)
    paginator = Paginator(questions, 10) # 10개씩 보여주는 Paginator 객체 생성
    page_obj = paginator.get_page(page) # 해당 페이지 객체 가져옴.
    user_questions_count = 0 # 해당 유저의 질문 개수 (기본값 : 0)

    if request.user.is_authenticated :
        user_questions_count = Question.objects.filter(user=request.user).count()
    context = {"questions" : page_obj, "user_question_count": user_questions_count}
    return render(request, "fitjob/board.html", context)

def question_create(request) :
    # 로그인 상태 X -> 로그인 창으로 이동
    if not request.user.is_authenticated :
        messages.info(request, "로그인 후 이용해주세요.")
        return redirect("user:login")
    
    # POST 요청 -> 질문 등록 시도
    if request.method == "POST":
        form = QuestionForm(request.POST)
        # 질문 등록 성공 -> 취업톡 페이지로 이동
        if form.is_valid():
            question = form.save(commit=False) # 임시 저장
            question.user = request.user # 보안상 따로 투입
            question.save() # 진짜 실제 DB 저장
            messages.success(request, "✅ 질문이 등록되었습니다.")
            return redirect("fitjob:board")
        
        # 질문 등록 실패 -> 기존 입력 유지하며, 질문 등록 페이지 새로고침
        return render(request, "fitjob/question_create.html", {"form": form})
    
    # GET 요청 -> 페이지 렌더링
    return render(request, "fitjob/question_create.html")

@require_POST # POST 요청이 아니면 405 에러 출력
def question_delete(request, question_id) :
    # 로그인 상태 X -> 로그인 창으로 이동
    if not request.user.is_authenticated :
        messages.info(request, "로그인 후 이용해주세요.")
        return redirect("user:login")
    
    question = Question.objects.get(id=question_id)
    if request.user != question.user : 
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect("fitjob:question_detail", question_id=question_id) 

    question.delete() # 해당 질문 삭제
    messages.success(request, "✅ 해당 글이 삭제되었습니다.")
    return redirect("fitjob:board")
    


@require_POST # POST 요청이 아니면 405 에러 출력
def answer_create(request, question_id) :
    # 로그인 상태 X -> 잘못된 접근 알림
    if not request.user.is_authenticated :
        messages.info(request, "잘못된 접근입니다. 로그인 상태를 확인해주세요.")
        return redirect("user:login")
    
    question = Question.objects.get(id=question_id)
    form = AnswerForm(request.POST)

    # 답변 등록 성공 -> 상세 페이지로 새로고침
    if form.is_valid():
        answer = form.save(commit=False)
        answer.user = request.user # 보안상 따로 투입
        answer.question = question # 보안상 따로 투입
        answer.save()
        messages.success(request, "✅ 답변이 등록되었습니다.")
        return redirect("fitjob:question_detail", question_id=question_id) 

    # 답변 등록 실패 -> 기존 입력 유지하면서 상세 페이지로 새로고침
    answers = Answer.objects.filter(question=question_id)
    user_questions_count = Question.objects.filter(user=request.user).count()
    context = {"question": question, "user_question_count": user_questions_count, "answers" : answers, "form" : form}
    return render(request, "fitjob/question_detail.html", context)

@require_POST # POST 요청이 아니면 405 에러 출력
def answer_delete(request, answer_id, question_id) :
    # 로그인 상태 X -> 로그인 창으로 이동
    if not request.user.is_authenticated :
        messages.info(request, "로그인 후 이용해주세요.")
        return redirect("user:login")
    
    answer = Answer.objects.get(id=answer_id)
    if request.user != answer.user : 
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect("fitjob:question_detail", question_id=question_id) 

    answer.delete() # 해당 질문 삭제
    messages.success(request, "✅ 해당 답변이 삭제되었습니다.")
    return redirect("fitjob:question_detail", question_id=question_id) 

def question_detail(request, question_id) :
    question = Question.objects.get(id=question_id)
    answers = Answer.objects.filter(question=question_id)
    user_questions_count = 0 # 해당 유저의 질문 개수 (기본값 : 0)

    if request.user.is_authenticated :
        user_questions_count = Question.objects.filter(user=request.user).count()
    
    context = {"question": question, "user_question_count": user_questions_count, "answers" : answers}
    return render(request, "fitjob/question_detail.html", context)

