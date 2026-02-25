# user/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User = get_user_model()
from django.contrib.auth import authenticate
from .models import Question, Answer



# Question폼
# 모델폼 : Django 모델과 연동된 폼
class QuestionForm(forms.ModelForm):
    # 재정의 필드
    title = forms.CharField(error_messages={"required" : "※ 제목을 입력해주세요."})
    content = forms.CharField(widget=forms.Textarea, error_messages={"required" : "※ 내용을 입력해주세요."})

    class Meta:
        model = Question # Question 모델과 연동
        fields = ["title", "content"] 
    
    # 제목 검증
    def clean_title(self) :
        title = (self.cleaned_data.get("title") or "").strip()
        if len(title) > 100 : 
            raise ValidationError(" ※ 제목은 최대 100자까지 입력 가능합니다.")
        return title
    
    # 내용 검증
    def clean_content(self) :
        content = (self.cleaned_data.get("content") or "").strip()
        if len(content) < 10 or len(content) > 1500 :
            raise ValidationError(" ※ 내용은 10자 이상, 1500자 이하로 입력해주세요.")
        return content    
    
    # clean(), save() 모두 오버라딩 하지 않고, 그대로 사용
    
# Answer폼
# 모델폼 : Django 모델과 연동된 폼
class AnswerForm(forms.ModelForm):
    # 재정의 필드
    content = forms.CharField(widget=forms.Textarea, error_messages={"required" : "※ 내용을 입력해주세요."})

    class Meta:
        model = Answer
        fields = ["content"] 
    
    # 내용 검증
    def clean_content(self) :
        content = (self.cleaned_data.get("content") or "").strip()
        if len(content) < 10 or len(content) > 1500 :
            raise ValidationError(" ※ 내용은 10자 이상, 1500자 이하로 입력해주세요.")
        return content  
    
    # clean(), save() 모두 오버라딩 하지 않고, 그대로 사용