import os
import requests
from django.shortcuts import redirect
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from json import JSONDecodeError
from django.http import JsonResponse
from users.models import User
from django.http import HttpResponseRedirect
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.views import APIView
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.permissions import AllowAny
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from users.serializers import UserProfileSerializer, UserUpdateSerializer, PasswordChangeSerializer
from django.conf import settings
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.kakao import views as kakao_view
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
import requests
from rest_framework import status
from json.decoder import JSONDecodeError
import os
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view

BASE_URL = 'http://127.0.0.1:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'users/kakao/callback/'


class UserView(APIView): # 회원 전체 목록 (내 정보 제외)
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, user_id): # 회원정보 전체 보기(내 정보 제외)
            articles = User.objects.exclude(id=user_id)
            serializer = UserProfileSerializer(articles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserDeleteView(APIView): # User 삭제 View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
     
    def delete(self, request): # 회원탈퇴
        if request.user.is_authenticated:
            request.user.delete()
            return Response({"message":"탈퇴되었습니다!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)


class ProfileView(APIView):  # 회원정보 조회, 수정 View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, user_id): # 회원정보 상세 조회
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user)  
        return Response(serializer.data)
    
    def put(self, request, user_id): # 회원정보 수정
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = UserUpdateSerializer(user, data=request.data, partial=True, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"변경되었습니다!"}, status=status.HTTP_200_OK)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)


class PasswordChangeView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def put(self, request, user_id): # 회원정보 수정
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = PasswordChangeSerializer(user, data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"비밀번호가 변경되었습니다!"}, status=status.HTTP_200_OK)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)


class ConfirmEmailView(APIView): # 이메일 인증 View
    
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario
        return HttpResponseRedirect('/') # 인증성공

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React Router Route will handle the failure scenario
                return HttpResponseRedirect('/') # 인증실패
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs

class FollowView(APIView): # follow View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post (self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me == you:

            return Response({"message":"스스로를 follow 할 수 없습니다"})
        else:
            if me in you.followee.all():
                you.followee.remove(me)
                return Response({"message":"unfollow했습니다."}, status=status.HTTP_200_OK)
            else:
                you.followee.add(me)
                return Response({"message":"follow했습니다."}, status=status.HTTP_200_OK)


def kakao_login(request): # 카카오 소셜 로그인 함수
    client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code&scope=account_email")

@api_view(['GET'])
def kakao_callback(request): # 카카오 소셜 로그인 callback 함수
    client_id = os.environ.get("SOCIAL_AUTH_KAKAO_CLIENT_ID")
    code = request.GET.get("code")
    redirect_uri = KAKAO_CALLBACK_URI

    # code로 access token 요청
    token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&code={code}")
    token_response_json = token_request.json()
    error = token_response_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_response_json.get("access_token")
    
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_json = profile_request.json()
    kakao_account = profile_json.get('kakao_account')


    email = kakao_account.get("email", None) # 이메일!


    # 이메일 없으면 오류 => 카카오톡 최신 버전에서는 이메일 없이 가입 가능해서 추후 수정해야함

    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저

        # social_user = SocialAccount.objects.get(user=user)
        # if social_user is None:
        #     return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        # if social_user.provider != 'kakao':
        #     return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)

        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}users/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
        # return Response({'message': '로그인 되었습니다!'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}users/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        accept_json.pop('user', None)
        # return JsonResponse(accept_json)
        return Response({'message': '가입 되었습니다!'}, status=status.HTTP_200_OK)

class KakaoLogin(SocialLoginView): 
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI
