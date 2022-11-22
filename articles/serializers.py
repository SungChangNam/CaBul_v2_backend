from rest_framework import serializers
from articles.models import Feed, Comment
from users.models import User


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Comment
        fields=('id', 'user', 'content', 'created_at',)
        
class FeedCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email
    
    class Meta:

        model = Comment
        fields='__all__'
        
class ArticleDetailSerializer(serializers.ModelSerializer):
    Feed_comment = CommentSerializer(many=True)

    def get_user(self, obj):
        return obj.user.email
        
    class Meta:
        model = Feed
        fields='__all__'

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feed
        fields='__all__'
        
class FeedSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Feed
        fields = '__all__'

class FeedListSerializer(serializers.ModelSerializer):
    like_count= serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return obj.like.count()

    class Meta:
        model = Feed
        fields='__all__'