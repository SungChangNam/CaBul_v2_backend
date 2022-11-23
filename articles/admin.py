from django.contrib import admin
from articles.models import Feed, Comment


# Register your models here.
admin.site.register(Feed)
admin.site.register(Comment)
class PostAdmin(admin.ModelAdmin):
    # list_display = ('title','content','category')
    list_display = ('title','content','category') # 'title','content','category' 추가

    list_filter = ('title',)
    search_fields = ('title','content','category') # 검색 박스 표시, title, content, category 칼럼에서 검색
    prepopulated_fields = {'slug': ('title',)} # title 필드를 사용해 미리 채워지도록

    # add two methods about tag

    # Post 레코드 리스트를 가져오는 메소드 오버라이딩
    # N:N 관계에서 쿼리 횟수를 줄여 성능 높일때 : prefetch_related
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self,obj):
        return ', '.join(o.name for o in obj.tags.all())