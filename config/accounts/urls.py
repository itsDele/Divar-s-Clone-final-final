# urls.py
from django.urls import path
from .views import RegisterView, LoginView ,send_otp ,verify_otp

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("send_otp/", send_otp(), name="send_otp"),
    path("verify_otp/", verify_otp(), name="verify_otp"),
]
