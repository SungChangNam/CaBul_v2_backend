
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from articles import serializers
from articles.models import Feed, Comment
from rest_framework import generics
from rest_framework import filters
from rest_framework import permissions
from articles.serializers import ArticleSerializer, FeedSerializer, FeedListSerializer, FeedCommentSerializer
from django.db.models.query_utils import Q


# Create your views here.

class FeedCommentView(APIView): #댓글 (작성)(성창남)

    def post(self, request, feed_id):
        serializer = FeedCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, feed_id=feed_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ArticlesFeedView(APIView):
    
    def get(self, request):
        articles = Feed.objects.all()
        serializer = FeedListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FeedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            
class FeedCommentDetailView(APIView):  #댓글(수정,삭제)(성창남)

    def put(self, request, feed_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = FeedCommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
            
    def delete(self, request, feed_id, comment_id):
        comment = get_object_or_404(Comment, id= comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)     
        

class ArticlesFeedDetailView(APIView):
    
    def get(self, request, feed_id):
        feed = get_object_or_404(Feed, id=feed_id)
        serializer = FeedSerializer(feed)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, feed_id):
        feed = get_object_or_404(Feed, id= feed_id)
        if request.user == feed.user:
            serializer = FeedSerializer(feed, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, feed_id):
        feed = get_object_or_404(Feed, id= feed_id)
        if request.user == feed.user:
            feed.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
        

class ArticlesFeedLikeView(APIView): # Feed 좋아요
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request,feed_id ):
        feed = get_object_or_404(Feed, id=feed_id)
        if request.user in feed.like.all():
            feed.like.remove(request.user)
            return Response("좋아요취소했습니다", status=status.HTTP_200_OK)
        else:
            feed.like.add(request.user)
            return Response("좋아요했습니다", status=status.HTTP_200_OK)
        

class ArticlesSearchView(generics.ListAPIView): 
    queryset = Feed.objects.all()
    serializer_class = ArticleSerializer

    filter_backends = [filters.SearchFilter]
    # 검색 키워드를 지정했을 때, 매칭을 시도할 필드
    search_fields = ["title"]