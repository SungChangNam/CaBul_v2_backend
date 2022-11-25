from django.urls import path
from articles import views


urlpatterns = [

    path('', views.ArticlesFeedView.as_view(), name ='feed_upload_view' ),# 게시글 전체보기, 등록 url
    path('category/', views.CategoryView.as_view(), name ='category_view' ),# 카테고리 목록 조회 url
    path('category/<str:feed_category>/', views.ArticlesCategoryFeedView.as_view(), name ='feed_category_view' ), # 게시글 카테고리 분류 url
    path('<int:feed_id>/like/', views.ArticlesFeedLikeView.as_view(), name = 'feed_like_view'),    # 게시글 좋아요 url
    path('search/', views.ArticlesSearchView.as_view(), name = 'articles_search_view'),            # 게시글 검색 url
    path('<int:feed_id>/', views.ArticlesFeedDetailView.as_view(), name ='feed_detail_view' ),     # 게시글 상세조회, 수정, 삭제 url
    path('<int:feed_id>/comment/', views.FeedCommentView.as_view(), name = 'feed_comment_view'),   # 댓글 등록 url
    path('<int:feed_id>/comment/<int:comment_id>/', views.FeedCommentDetailView.as_view(), name = 'feed_comment_detail_view'), # 댓글 수정, 삭제 url
    path('tag/', views.TagView.as_view(), name='tagged_list'),   # 게시글 태그 url
]

