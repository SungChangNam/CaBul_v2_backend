from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from users import views
from dj_rest_auth.registration.views import VerifyEmailView

urlpatterns = [
    path('delete/', views.UserView.as_view(), name='user_view'),
    path('<int:user_id>/', views.ProfileView.as_view(), name='profilw_view'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),  # 로그인 및 기타 dj-rest-auth 기능
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')), #회원가입
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'), #이메일 인증 
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', views.ConfirmEmailView.as_view(), name='account_confirm_email'), # 이메일 인증
    path('kakao/login', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),

]