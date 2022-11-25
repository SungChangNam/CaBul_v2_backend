from django.urls import path, re_path, include
from users import views
from dj_rest_auth.registration.views import VerifyEmailView

urlpatterns = [
    path('delete/', views.UserDeleteView.as_view(), name='user_view'), # 회원 삭제 url
    path('all/<int:user_id>/', views.UserView.as_view(), name='user_all_view'), # 회원정보 전체 조회 url
    path('<int:user_id>/', views.ProfileView.as_view(), name='profile_view'), # 회원 정보 상세 조회, 수정 url
    path('<int:user_id>/passwordchange/', views.PasswordChangeView.as_view(), name='passwordchange_view'), # 비밀번호 변경 url
    path('dj-rest-auth/', include('dj_rest_auth.urls')),  # 로그인 및 기타 dj-rest-auth 기능 url
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')), #회원가입 dj-rest-auth url
    path('follow/<int:user_id>/', views.FollowView.as_view(),name='follow_view'), # follow url
    # path('api/kakao/', views.KakaoLoginView.as_view(), name='kakao_login'),
    path('kakao/login/', views.kakao_login, name='kakao_login'), # 카카오 소셜로그인 url
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),# 카카오 소셜로그인 url
    path('kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),# 카카오 소셜로그인 url
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'), #이메일 인증 url
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', views.ConfirmEmailView.as_view(), name='account_confirm_email'), # 이메일 인증 url
]