"""
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    user_id = models.CharField(
        max_length=36,
        unique=True,
        editable=False,
        verbose_name='ユーザーID'
    )
    email = models.EmailField(unique=True, verbose_name='メールアドレス')
    language = models.CharField(
        max_length=10,
        choices=[
            ('ja', '日本語'),
            ('en', 'English'),
            ('es', 'Español'),
        ],
        default='ja',
        verbose_name='言語設定'
    )

    REQUIRED_FIELDS = ['email', 'language']
    USERNAME_FIELD = 'username'

    def save(self, *args, **kwargs):
        if not self.user_id:  # 初回保存時のみ生成
            self.user_id = str(uuid.uuid4())  # UUIDを生成
        super().save(*args, **kwargs)
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, user_name, mailaddress, password=None, language_code=1):
        if not mailaddress:
            raise ValueError("メールアドレスは必須です")
        user = self.model(
            user_name=user_name,
            mailaddress=self.normalize_email(mailaddress),
            language_code=language_code,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, mailaddress, password=None, language_code=1):
        user = self.create_user(user_name=user_name, mailaddress=mailaddress, password=password, language_code=language_code)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)  # これを追加
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=30, unique=True)
    mailaddress = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=15)
    language_code = models.IntegerField(choices=[(1, "日本語"), (2, "English")], default=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    # USERNAME_FIELDを'mailaddress'から'username'に変更
    USERNAME_FIELD = 'user_name'  # 変更後のフィールド名を指定
    REQUIRED_FIELDS = ['mailaddress', 'language_code']  # 'mailaddress'をREQUIRED_FIELDSに追加

    def __str__(self):
        return self.user_name
