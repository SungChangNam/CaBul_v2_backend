from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("admin/", admin.site.urls),
    path('users/', include("users.urls")),
    path('articles/', include('articles.urls')),
    path('api/user/', include('allauth.urls')),   # 카카오 소셜로그인에서 사용

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)