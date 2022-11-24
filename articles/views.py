from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
from articles.models import Feed, Comment, TaggedFeed
from rest_framework import generics
from rest_framework import filters
from rest_framework import permissions
from articles.serializers import ArticleSerializer, FeedSerializer, FeedListSerializer, FeedCommentSerializer, TagSerializer, FeedDetailSerializer
from articles.deep_learning import upload_category, transform
import cv2
import random
from rest_framework_simplejwt.authentication import JWTAuthentication




class ArticlesFeedView(APIView): # 게시글 전체보기, 등록 View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request): # 게시글 전체 보기
        articles = Feed.objects.all()
        serializer = FeedListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request): # 게시글 등록
        
        serializer = FeedSerializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save(user=request.user)
            img = serializer.data["original_image"]
            upload_category(img, serializer.data)
            
            model_list = ['articles/sample/composition_vii.t7', 'articles/sample/candy.t7', 'articles/sample/feathers.t7', 'articles/sample/la_muse.t7', 'articles/sample/mosaic.t7', 'articles/sample/starry_night.t7', 'articles/sample/the_scream.t7', 'articles/sample/the_wave.t7', 'articles/sample/udnie.t7']
            random.shuffle(model_list)
            
            net = cv2.dnn.readNetFromTorch(model_list[0])
            
            transform(img, net, serializer.data)
            
            return Response({"message":"게시글이 등록되었습니다!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        
class ArticlesFeedDetailView(APIView): #게시글 상세조회, 수정, 삭제 View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, feed_id): # 게시글 상세 조회
        feed = get_object_or_404(Feed, id=feed_id)
        serializer = FeedDetailSerializer(feed)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, feed_id): # 게시글 수정
        feed = get_object_or_404(Feed, id= feed_id)
        if request.user == feed.user:
            serializer = FeedSerializer(feed, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                img = serializer.data["original_image"]
                upload_category(img, serializer.data)
                
                model_list = ['articles/sample/composition_vii.t7', 'articles/sample/candy.t7', 'articles/sample/feathers.t7', 'articles/sample/la_muse.t7', 'articles/sample/mosaic.t7', 'articles/sample/starry_night.t7', 'articles/sample/the_scream.t7', 'articles/sample/the_wave.t7', 'articles/sample/udnie.t7']
                random.shuffle(model_list)
                
                net = cv2.dnn.readNetFromTorch(model_list[0])
                
                transform(img, net, serializer.data)
                
                return Response({"message":"게시글이 수정되었습니다!"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, feed_id): # 게시글 삭제
        feed = get_object_or_404(Feed, id= feed_id)
        if request.user == feed.user:
            feed.delete()
            return Response({"message":"게시글이 삭제되었습니다!"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
class ArticlesFeedLikeView(APIView): # Feed 좋아요 View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request,feed_id ):
        feed = get_object_or_404(Feed, id=feed_id)
        if request.user in feed.like.all():
            feed.like.remove(request.user)
            return Response({"message":"좋아요 취소했습니다!"}, status=status.HTTP_200_OK)
        else:
            feed.like.add(request.user)
            return Response({"message":"좋아요 했습니다!"}, status=status.HTTP_200_OK)
        

class ArticlesSearchView(generics.ListAPIView): # 게시글 검색 View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    queryset = Feed.objects.all()
    serializer_class = ArticleSerializer

    filter_backends = [filters.SearchFilter]
    # 검색 키워드를 지정했을 때, 매칭을 시도할 필드
    search_fields = ["title"]

class TagView(generics.ListAPIView): # 게시글 Tag View
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    queryset = TaggedFeed.objects.all()
    serializer_class = TagSerializer
        
class FeedCommentView(APIView): # 댓글 등록 View (성창남)
    
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, feed_id): # 댓글 등록
        serializer = FeedCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, feed_id=feed_id)
            return Response({"message":"댓글 등록했습니다!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            
class FeedCommentDetailView(APIView):  #댓글(수정,삭제) View (성창남)
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request, feed_id, comment_id): # 댓글 수정
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = FeedCommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"댓글 수정했습니다!"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)
            
    def delete(self, request, feed_id, comment_id): # 댓글 삭제
        comment = get_object_or_404(Comment, id= comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response({"message":"댓글 삭제했습니다!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN)     
        
    