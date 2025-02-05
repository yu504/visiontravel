"""
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
#from .forms import UserRegistrationForm
#from .models import Language
from django.contrib import messages
from django.utils.translation import activate
from django.conf import settings

def login_view(request):
    # 言語設定の確認と変更
    lang = request.GET.get('lang', 'ja')  # URLパラメータで言語を取得、デフォルトは日本語
    activate(lang)  # 言語を変更
    request.session['django_language'] = lang  # セッションに言語を保存

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('mainmenu')  # ログイン後にリダイレクトするページ
        else:
            error_message = "ユーザー名またはパスワードが間違っています。"
            return render(request, 'user/login.html', {'form': form, 'error': error_message})

    else:
        form = AuthenticationForm()

    return render(request, 'user/login.html', {'form': form})

def logout_view(request):
    logout(request)  # ログアウト処理
    return redirect('login')  # ログインページにリダイレクト

def register(request):
    return render(request, 'user/register.html')  # 新規登録用テンプレートを返す


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '登録が完了しました。ログインしてください。')
            return redirect('login')  # ログインページのURL名に置き換えてください
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})

from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            # Django 標準の `urlsafe_base64_encode` を使用して `uidb64` を生成
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            # パスワードリセットページへリダイレクト
            return redirect(reverse_lazy('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
        return super().form_valid(form)
"""

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.utils.translation import activate

User = get_user_model()

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 言語コードを適用（デフォルトは1=日本語, 2=English）
            if user.language_code == 2:  # English
                activate('en')
            else:  # 日本語
                activate('ja')

            return redirect('mainmenu')  # メインメニューへリダイレクト

        else:
            return render(request, "user/login.html", {"error": "ユーザー名またはパスワードが違います"})

    return render(request, "user/login.html")





'''
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('mainmenu')  # ログイン後にリダイレクトするページ
        else:
            # フォームが無効な場合、カスタムエラーメッセージを設定
            error_message = "ユーザー名またはパスワードが間違っています。"
            return render(request, 'user/login.html', {'form': form, 'error': error_message})
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})
'''


def logout_view(request):
    logout(request)  # ログアウト処理
    return redirect('login')  # ログインページにリダイレクト

def register(request):
    return render(request, 'user/register.html')  # 新規登録用テンプレートを返す


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '登録が完了しました。ログインしてください。')
            return redirect('login')  # ログインページのURL名に置き換えてください
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})

from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            # Django 標準の `urlsafe_base64_encode` を使用して `uidb64` を生成
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            # パスワードリセットページへリダイレクト
            return redirect(reverse_lazy('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
        return super().form_valid(form)




