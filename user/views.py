from django.shortcuts import render
from .models import User 
from django.contrib import messages
from django.shortcuts import redirect
import re
from .forms import SignupForm

def login(request) :
    return render(request, "user/login.html")

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST) # POST 요청으로 받은 모든 파라미터를 폼에 전달 
        if form.is_valid(): # is_valid() : Form에 정의된 모든 검증 로직을 한 번에 실행하는 트리거 함수
            form.save()
            messages.success(request, "✅ 회원가입이 완료되었습니다.")
            return redirect("user:signup")
        # 실패면 그대로 signup 페이지 렌더 (이동 X)
        return render(request, "user/signup.html", {"form": form})

    form = SignupForm()
    return render(request, "user/signup.html", {"form": form})
# Create your views here.
