import re

from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.hashers import check_password

from users.models import User
from articles.serializers import FeedDetailSerializer



class customRegistrationSerializer(RegisterSerializer):  # dj-rest-auth 회원가입 시리얼라이저
    
    nickname = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=20)
    
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['name'] = self.validated_data.get('name', '')

        return data
    
    
class UserProfileSerializer(serializers.ModelSerializer): # user 정보 상세조회 serializer
    followee = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    follow_count = serializers.SerializerMethodField()
    followee_count = serializers.SerializerMethodField()
    feed_set = FeedDetailSerializer(many=True, read_only=True)
    feed_set_count = serializers.SerializerMethodField()
    
    def get_follow_count(self, obj):
        return obj.follow.count()
    
    def get_followee_count(self, obj):
        return obj.followee.count()
    
    def get_feed_set_count(self, obj):
        return obj.feed_set.count()
    
    #   프로필 조회
    class Meta:
        model = User
        fields=("id", "name","nickname","email", "follow_count", "followee_count", "last_login", "feed_set", "follow", "followee", "profile_image", "feed_set", "feed_set_count")

class UserUpdateSerializer(serializers.ModelSerializer):  # 회원정보 변경 serializer
    class Meta:
        model = User
        fields=("nickname","name", "profile_image")
    
    def update(self, instance, validated_data): # 비밀번호 수정 
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)
            
        instance.save()
        
        return instance


class PasswordChangeSerializer(serializers.ModelSerializer): # 비밀번호 변경 serializer
    password2 = serializers.CharField(error_messages={'required':'비밀번호를 입력해주세요.', 'blank':'비밀번호를 입력해주세요.', 'write_only':True})
    
    class Meta:
        model = User
        fields=("password","password2",)
    
    def validate(self, data):
        PASSWORD_VALIDATION = r"^(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,16}"
        PASSWORD_PATTERN = r"(.)\1+\1"
        
        current_password = self.context.get("request").user.password
        password = data.get('password')
        password2 = data.get('password2')
        
        #현재 비밀번호와 바꿀 비밀번호 비교
        if check_password(password, current_password):
            raise serializers.ValidationError(detail={"password":"현재 비밀번호와 동일합니다!."})
        
        #비밀번호 일치
        if password != password2:
            raise serializers.ValidationError(detail={"password":"비밀번호 확인이 일치하지 않습니다!"})
        
        #비밀번호 유효성 검사
        if not re.search(PASSWORD_VALIDATION, str(password)):
            raise serializers.ValidationError(detail={"password":"비밀번호는 8자 이상 16자이하의 영문, 숫자, 특수문자 조합이어야 합니다! "})
        
        #비밀번호 문자열 동일여부 검사
        if re.search(PASSWORD_PATTERN, str(password)):
            raise serializers.ValidationError(detail={"password":"너무 일상적인 숫자or단어 입니다!"})

        return data
    
    
    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)
        instance.set_password(instance.password)
        instance.save()
        return instance
    
    