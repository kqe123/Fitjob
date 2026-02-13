# user/forms.py
import re
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

# 아이디: 5~20 영문/숫자
USERNAME_RULE = re.compile(r"^[A-Za-z0-9]{5,20}$")

# 비밀번호 : 8자 이상 + 영문/숫자/특수문자 포함
PASSWORD_RULE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$")

# 닉네임: 2~10자, 한글/영문/숫자/_
NICKNAME_RULE = re.compile(r"^[가-힣A-Za-z0-9_]{2,10}$")

# 모델폼 : Django 모델과 연동된 폼
class SignupForm(forms.ModelForm):
    # 재정의 필드
    username = forms.CharField(error_messages={"required": "아이디를 입력해주세요."})
    nickname = forms.CharField(error_messages={"required": "닉네임을 입력해주세요."})

    # 재정의 필드
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="비밀번호",
        error_messages={"required": "비밀번호를 입력해주세요."},
    )
    # 재정의 필드
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="비밀번호 확인",
        error_messages={"required": "비밀번호 확인을 입력해주세요."},
    )

    class Meta:
        model = User # User 모델과 연동
        fields = ["username", "nickname"] # 폼 필드로 username, nickname을 받음.

    # 1. 아이디 유효성 + 중복 검사
    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        
        if not USERNAME_RULE.match(username):
            raise ValidationError("아이디는 5~20자, 영문/숫자만 가능합니다.")
        
        if User.objects.filter(username=username).exists():
            raise ValidationError("이미 사용 중인 아이디입니다.")
        
        return username

    # 2. 닉네임 유효성 + 중복 검사
    def clean_nickname(self):
        nickname = (self.cleaned_data.get("nickname") or "").strip()

        if not NICKNAME_RULE.match(nickname):
            raise ValidationError("닉네임은 2~10자, 한글/영문/숫자/_ 만 가능합니다.")

        if User.objects.filter(nickname=nickname).exists():
            raise ValidationError("이미 사용 중인 닉네임입니다.")

        return nickname

    # 3. 비밀번호1 유효성 검사
    def clean_password1(self):
        pw1 = (self.cleaned_data.get("password1") or "").strip()
        if not PASSWORD_RULE.match(pw1):
            raise ValidationError("비밀번호는 8자 이상, 영문/숫자/특수문자를 모두 포함해야 합니다.")
        return pw1
    
    # 4. 비밀번호2 유효성 검사
    def clean_password2(self):
        pw2 = (self.cleaned_data.get("password2") or "").strip()
        if not PASSWORD_RULE.match(pw2):
            raise ValidationError("비밀번호는 8자 이상, 영문/숫자/특수문자를 모두 포함해야 합니다.")
        return pw2
    

    # 5. 폼 전체 검증(비밀번호 일치 검사)
    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get("password1")
        pw2 = cleaned.get("password2")
        if pw1 and pw2 and pw1 != pw2:
            self.add_error("password2", "비밀번호가 일치하지 않습니다.")
        return cleaned

    # 6. 저장 메서드 오버라이딩 (검증 x)
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user