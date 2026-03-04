from django.shortcuts import render
from .models import User 
from django.contrib import messages
from django.shortcuts import redirect
import re
from .forms import SignupForm, LoginForm, ChangePasswordForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash
import os
from django.conf import settings

SECTION_TEMPLATES = {
    "profile": "user/mypage_content/profile.html",
    "password": "user/mypage_content/password.html",
    "coverletter": "user/mypage_content/coverletter.html",
    }

def login_try(request) :
    # 이미 로그인된 상태면 로그인 페이지 접근 불가
    if request.user.is_authenticated :
        messages.info(request, "이미 로그인된 상태입니다.")
        return redirect("fitjob:main")

    # method = POST -> 로그인 시도
    if request.method == "POST" :
        form = LoginForm(request.POST)
        next_url = request.POST.get("next_url")
        # 로그인 성공
        if form.is_valid() : # 모든 검증 로직이 통과되면 True
            auth_user = form.cleaned_data.get("auth_user") # cleaned_data에서 User객체 가져옴.
            login(request, auth_user) # 로그인 인가 
            messages.success(request, f"✅ {auth_user.nickname}님 환영합니다.")

            # next_url이 None 또는 "" -> 메인화면으로 이동
            if not next_url :
                return redirect("fitjob:main")
            # next_url가 있음 -> 해당 주소로 이동
            return redirect(next_url)
        
        # 로그인 실패 -> 기존 입력 유지하고 새로고침
        return render(request, "user/login.html", {"form": form, "next_url" : next_url})
    
    # method = GET -> 페이지 렌더링
    # 페이지 이동 = GET이라고 생각하자.
    next_url = request.GET.get("next")
    context = {"form" : LoginForm(), "next_url" : next_url}
    return render(request, "user/login.html", context)

def logout_try(request) :
    logout(request)
    messages.success(request, "✅ 로그아웃 되었습니다.")
    return redirect("fitjob:main")


def signup_try(request):
    # 폼 요청 O -> 회원가입 시도
    if request.method == "POST":
        form = SignupForm(request.POST) # POST 요청으로 받은 모든 파라미터를 폼에 전달 
        if form.is_valid(): # is_valid() : Form에 정의된 모든 검증 로직을 한 번에 실행하는 트리거 함수
            form.save()
            messages.success(request, "✅ 회원가입이 완료되었습니다.")
            return redirect("user:signup")
        # 실패면 그대로 signup 페이지 렌더 (이동 X)
        return render(request, "user/signup.html", {"form": form})

    # 폼 요청 X -> 회원가입 페이지 렌더링
    form = SignupForm()
    return render(request, "user/signup.html", {"form": form})

@login_required(login_url='user:login')
def mypage(request, section="profile"):    
    section_template = SECTION_TEMPLATES.get(section)
    context = {"section" : section, "section_template" : section_template}
    return render(request, "user/mypage.html", context)

@login_required(login_url='user:login')
@require_POST
def change_password(request):    
    form = ChangePasswordForm(request.user, request.POST) # POST 요청으로 받은 모든 파라미터를 폼에 전달 
    if form.is_valid() :
        new_pw = form.cleaned_data["new_password1"]
        request.user.set_password(new_pw)
        request.user.save()
        update_session_auth_hash(request, request.user)  # ✅ 비번 바꿔도 로그인 유지 메서드

        messages.success(request, "✅ 비밀번호 변경이 완료되었습니다.")
        return redirect("fitjob:main")
        
    return render(request, "user/mypage.html", 
            {"form": form, "section" : "password", "section_template" : SECTION_TEMPLATES['password']})

@login_required(login_url='user:login')
@require_POST
def change_profile(request):    
    user = request.user
    nickname = request.POST.get("nickname", "").strip()
    img = request.FILES.get("profile_image")

    # ✅ 이전 파일 경로 백업
    old_image = user.profile_image.name  # 예: "profiles/xxx/avatar.png"

    # 1. 닉네임이 규칙을 통과한 경우 user.nickname 수정
    NICKNAME_RULE = re.compile(r"^[가-힣A-Za-z0-9_]{2,10}$")
    if not NICKNAME_RULE.match(nickname):
        messages.error(request, "⚠️ 별명은 2~10자 한글/영어/숫자로 이루어져야 합니다!")
        return redirect("user:mypage")  # 마이페이지(프로필)로 돌아감
    user.nickname = nickname

    # 2. 업로드 프로필 사진이 존재하고, 조건을 모두 만족할 경우에만 user.profile_image 수정
    if img : 
        # 이미지 파일이 아니라면 오류
        if not (img.content_type or "").startswith("image/"):
            messages.error(request, "⚠️ 이미지 파일만 업로드할 수 있습니다.")
            return redirect("user:mypage")

        # 용량이 3MB가 넘으면 오류
        if img.size > 3 * 1024 * 1024:
            messages.error(request, "⚠️ 이미지 용량은 3MB 이하만 가능합니다.")
            return redirect("user:mypage")
        
        user.profile_image = img

    # 3. ✅ 프로필 수정    
    user.save()

    # 4. 기존 프로필 이미지는 삭제 
    if old_image not in (user.profile_image.name, "profiles/default.png") :
        old_path = os.path.join(settings.MEDIA_ROOT, old_image)
        if os.path.exists(old_path):
            os.remove(old_path)

    messages.success(request, "✅ 프로필이 수정되었습니다.")
    return redirect("user:mypage")  # 마이페이지(프로필)로 돌아감


