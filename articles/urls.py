from django.urls import path
from articles import views


urlpatterns = [

    path('<int:feed_id>/like/', views.ArticlesFeedLikeView.as_view(), name = 'feed_like_view'),    # 좋아요
    path('search/', views.ArticlesSearchView.as_view(), name = 'articles_search_view'),            # 검색
    path('', views.ArticlesFeedView.as_view(), name ='feed_upload_view' ),                         # 게시글 업로드, 조회
    path('<int:feed_id>/', views.ArticlesFeedDetailView.as_view(), name ='feed_detail_view' ),     # 게시글 상세조회, 수정, 삭제
    path('<int:feed_id>/comment/', views.FeedCommentView.as_view(), name = 'feed_comment_view'),   # 댓글 작성
    path('<int:feed_id>/comment/<int:comment_id>/', views.FeedCommentDetailView.as_view(), name = 'feed_comment_detail_view'), # 댓글 수정, 삭제
    path('tag/', views.TagView.as_view(), name='tagged_list'),                                     #테그  #ListView를 상속받아 정의
]

