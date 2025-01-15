# urls.py
from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("send_otp/", LoginView.as_view(), name="send_otp"),
    path("verify_otp/", LoginView.as_view(), name="verify_otp"),
]
