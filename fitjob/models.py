from django.db import models
import uuid
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db.models import Q

# Create your models here.
class Question(models.Model) :
    id = models.AutoField(primary_key=True, editable=False, unique=True) # 질문 고유 ID (1,2,3...)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE) # FK (user앱의 User모델 PK)
    title = models.CharField(max_length=100, validators=[MaxLengthValidator(100)], default="새 세션", null=False) # 질문 제목
    content = models.TextField(validators=[MinLengthValidator(10), MaxLengthValidator(1500)], null=False) # 질문 내용
    created_at = models.DateTimeField(auto_now_add=True) # 생성일

    class Meta : 
        db_table = "question" # 테이블 이름 설정

class Answer(models.Model) : 
    id = models.AutoField(primary_key=True, editable=False, unique=True) # 답변 고유 ID (1,2,3...)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False) # 해당 질문 ID (FK)
    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True) # 답변 작성자 (FK)
    content = models.TextField(validators=[MinLengthValidator(10), MaxLengthValidator(1500)], null=False) # 질문 내용
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    class Meta : 
        db_table = "answer" # 테이블 이름 설정

class Report(models.Model) :
    # id는 기본적으로 생성됨.
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, null=False) # 신고자 FK (user앱의 User모델 PK)
    # 신고 대상 question 또는 answer
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True) # 대상 question (없으면 null)
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, blank=True) # 대상 answer (없으면 null)
    
    STATUS = [
        ("PENDING", "대기 중"),
        ("RESOLVED", "처리 완료"),
        ("REJECTED", "반려"),
    ]
    reason = models.CharField(max_length=200, null=False) # 신고 사유
    status = models.CharField(max_length=10, choices=STATUS, default="PENDING") # 처리 현황
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    class Meta : 
        db_table = "report" # 테이블 이름 설정
        constraints = [
            # 제약1 : question, answer 둘 중 하나는 무조건 존재해야함. 
            models.CheckConstraint(
                condition=(Q(question__isnull=False, answer__isnull=True) |
                       Q(question__isnull=True,  answer__isnull=False)),
                name="report_target_xor"
            ),
            # 제약2 : 중복 신고 방지 (user+question, user+answer)
            models.UniqueConstraint(fields=["user", "question"], name="uniq_user_question_report"),
            models.UniqueConstraint(fields=["user", "answer"],   name="uniq_user_answer_report"),
        ]