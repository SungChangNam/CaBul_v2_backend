from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class UserRegistrationTest(APITestCase):
    def test_registration(self):  #회원가입 테스트
        url = reverse("rest_register")   # url name
        user_data = {
                "email":"test@naver.com",
                "name":"name",
                "nickname":"junseok",
                "password1":"password123@",
                "password2":"password123@"
            }
        response = self.client.post(url, user_data)  # APITestCase의 기본적인 세팅
        self.assertEqual(response.status_code, 201)
