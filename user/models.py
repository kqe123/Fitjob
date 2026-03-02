from django.db import models
# 우리가 만들 User 모델의 부모 클래스
from django.contrib.auth.models import AbstractUser
# 슈퍼 유저나 일반 유저를 생성할 때 사용할 매니저 클래스
from django.contrib.auth.models import BaseUserManager
# Create your models here.  
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator, MinLengthValidator
import uuid

def user_profile_upload_path(instance, filename):
    # 파일명이 겹칠 수 있으니 uuid로 저장하는 걸 추천
    ext = filename.split(".")[-1]
    return f"profiles/{instance.id}/avatar.{ext}"

# 아이디 유효성 검사기
username_validator = RegexValidator(
    regex=r"^[a-zA-Z0-9]{5,20}$",
    message="아이디는 5~20자 영문/숫자만 가능합니다.",
)

# 닉네임 유효성 검사기
nickname_validator = RegexValidator(
    regex=r"^[가-힣a-zA-Z0-9_]{2,10}$",
    message="닉네임은 2~10자(한글/영문/숫자/_)만 가능합니다.",
)

# 커스텀 유저 매니저
class CustomUserManager(BaseUserManager) :
    use_in_migrations = True

    #일반 유저 생성 메서드
    def create_user(self, username, password=None, **extra_fields) :
        if not username : 
            raise ValueError("User ID is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    #슈퍼 유저 생성 메서드
    def create_superuser(self, username, password=None, **extra_fields) :
        user = self.create_user(username=username, password=password, **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# 커스텀 유저 모델
class User(AbstractUser, PermissionsMixin) : 
    objects = CustomUserManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # PK (일련번호)
    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[username_validator],
    )

    nickname = models.CharField(
        max_length=12,
        unique=True,
        null=True,
        blank=True,
        validators=[nickname_validator, MinLengthValidator(2)],
    )
    
    profile_image = models.ImageField(
        upload_to=user_profile_upload_path,
        null=True,
        blank=True,
        default="profiles/default.png"   # ✅ 기본 이미지 경로
    )

    is_admin = models.BooleanField(default=False) # 관리자 여부
    created_at = models.DateTimeField(auto_now_add=True) # 생성일
    updated_at = models.DateTimeField(auto_now=True) # 수정일

    class Meta : 
        db_table = "customuser" # 테이블 이름 설정

    USERNAME_FIELD = 'username' # 로그인에 사용할 필드
    REQUIRED_FIELDS = [] 


