from django.db import models
import uuid
from django.core.validators import MaxLengthValidator, MinLengthValidator

# Create your models here.
class Question(models.Model) :
    id = models.AutoField(primary_key=True, editable=False, unique=True) # 질문 고유 ID (1,2,3...)
    user_id = models.ForeignKey("user.User", on_delete=models.CASCADE) # FK (user앱의 User모델 PK)
    title = models.CharField(max_length=100, validators=[MaxLengthValidator(100)], default="새 세션", null=False) # 질문 제목
    content = models.TextField(validators=[MinLengthValidator(10), MaxLengthValidator(1500)], null=False) # 질문 내용
    created_at = models.DateTimeField(auto_now_add=True) # 생성일

    class Meta : 
        db_table = "question" # 테이블 이름 설정

class Answer(models.Model) : 
    id = models.AutoField(primary_key=True, editable=False, unique=True) # 답변 고유 ID (1,2,3...)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, null=False) # 해당 질문 ID (FK)
    user_id = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True) # 답변 작성자 (FK)
    content = models.TextField(validators=[MinLengthValidator(10), MaxLengthValidator(1500)], null=False) # 질문 내용
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    class Meta : 
        db_table = "answer" # 테이블 이름 설정