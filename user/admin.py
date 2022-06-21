from django.contrib import admin
from .models import User, UserProfile, Hobby

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Inline : 한 테이블에서 역참조 관계의 테이블을 같이 설정할 수 있다.
# Stackedinline은 세로로, TabularInline은 가로로
class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email')  # object 목록에 띄워줄 필드를 지정한다.
    list_display_links = ('username', )         # object 목록에서 클릭 시 상세 페이지로 들어갈 수 있는 필드를 지정한다.
    list_filter = ('username', )                # filter를 걸 수 있는 필드를 생성한다.
    search_fields = ('username', 'email', )     # 검색에 사용될 필드를 지정한다.

    fieldsets = (                               # 상세페이지에서 필드를 분류하는데 사용된다.
        ("info", {'fields': ('username', 'password', 'email', 'join_date',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', )}),)

    filter_horizontal = []

    def get_readonly_fields(self, request, obj=None):   # 상세페이지에서 읽기 전용 필드를 설정할 때 사용된다.
        if obj:
            return ('username', 'join_date', )
        else:
            return ('join_date', )

    inlines = (
            UserProfileInline,
        )

    def has_add_permission(self, request, obj=None): # 추가 권한
        return False

    def has_delete_permission(self, request, obj=None): # 삭제 권한
        return False

    def has_change_permission(self, request, obj=None): # 수정 권한
        return False


# Register your models here.
admin.site.register(User, UserAdmin)
# admin.site.register(UserManager)
admin.site.register(UserProfile)
admin.site.register(Hobby)