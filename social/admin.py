from django.contrib import admin
from social.models import FollowUser, MyPost, MyProfile, PostComment,PostLike ,Cont ,Comment
from django.contrib.admin.options import ModelAdmin

# admin.site.register(Comment)

@admin.register(Cont)
class ContAdmin(admin.ModelAdmin):
     list_display = ['sno', 'name' ,'email' ,'phone', 'desc']
     ordering = ['name']
     search_fields = ('name', 'email')


class FollowUserAdmin(ModelAdmin):
    list_display = ["profile", "followed_by"]
    search_fields = ["profile", "followed_by"]
    list_filter = ["profile", "followed_by"]
admin.site.register(FollowUser, FollowUserAdmin)

class MyPostAdmin(ModelAdmin):
    list_display = ["subject", "cr_date", "uploaded_by"]
    search_fields = ["subject", "msg", "uploaded_by"]
    list_filter = ["cr_date", "uploaded_by"]
admin.site.register(MyPost, MyPostAdmin)


class MyProfileAdmin(ModelAdmin):
    list_display = ["user","name","last_name","phone_no" ,"address","age" ,"status","gender","description","pic"]
    search_fields = ["name", "status", "phone_no"]
    list_filter = ["status", "gender"]
admin.site.register(MyProfile, MyProfileAdmin)


class CommentAdmin(ModelAdmin):
    list_display = ["post", "commented_by","created","updated"]
    search_fields = ["created", "post", "commented_by"]
    list_filter = ["created", "post","commented_by","updated"]
admin.site.register(Comment, CommentAdmin)


class PostLikeAdmin(ModelAdmin):
    list_display = ["post", "liked_by" ,"cr_date"]
    search_fields = ["post", "liked_by","cr_date"]
    list_filter = ["cr_date"]
admin.site.register(PostLike, PostLikeAdmin)

