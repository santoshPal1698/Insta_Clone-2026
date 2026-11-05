import json
from datetime import timedelta

from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from unfold.admin import ModelAdmin

from social.models import (
    Comment,
    Contact,
    FollowUser,
    MyPost,
    MyProfile,
    PostComment,
    PostLike,
)


def dashboard_callback(request, context):
    today = timezone.localdate()
    days = [today - timedelta(days=offset) for offset in range(6, -1, -1)]
    date_range = (days[0], today)

    post_activity = {
        row["day"]: row["total"]
        for row in MyPost.objects.filter(cr_date__date__range=date_range)
        .annotate(day=TruncDate("cr_date"))
        .values("day")
        .annotate(total=Count("pk"))
    }
    profile_activity = {
        row["day"]: row["total"]
        for row in MyProfile.objects.filter(cr_date__date__range=date_range)
        .annotate(day=TruncDate("cr_date"))
        .values("day")
        .annotate(total=Count("pk"))
    }

    context.update(
        {
            "social_stats": [
                {
                    "title": "Members",
                    "value": MyProfile.objects.count(),
                    "icon": "group",
                },
                {
                    "title": "Posts",
                    "value": MyPost.objects.count(),
                    "icon": "photo_library",
                },
                {
                    "title": "Comments",
                    "value": Comment.objects.count(),
                    "icon": "chat",
                },
                {
                    "title": "Follows",
                    "value": FollowUser.objects.count(),
                    "icon": "person_add",
                },
            ],
            "activity_chart": json.dumps(
                {
                    "labels": [day.strftime("%b %d") for day in days],
                    "datasets": [
                        {
                            "label": "Posts",
                            "data": [post_activity.get(day, 0) for day in days],
                            "borderColor": "#2563eb",
                            "backgroundColor": "rgba(37, 99, 235, 0.12)",
                            "fill": True,
                            "tension": 0.35,
                            "displayYAxis": True,
                        },
                        {
                            "label": "New members",
                            "data": [profile_activity.get(day, 0) for day in days],
                            "borderColor": "#16a34a",
                            "backgroundColor": "rgba(22, 163, 74, 0.12)",
                            "fill": True,
                            "tension": 0.35,
                            "displayYAxis": True,
                        },
                    ],
                }
            ),
            "recent_posts": (
                MyPost.objects.select_related("uploaded_by")
                .order_by("-cr_date")[:5]
            ),
        }
    )
    return context


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ("sno", "name", "email", "phone", "timeStamp")
    search_fields = ("name", "email", "phone", "desc")
    list_filter = ("timeStamp",)
    date_hierarchy = "timeStamp"
    ordering = ("-timeStamp",)
    readonly_fields = ("timeStamp",)
    list_per_page = 25


@admin.register(FollowUser)
class FollowUserAdmin(ModelAdmin):
    list_display = ("profile", "followed_by")
    search_fields = (
        "profile__name",
        "profile__user__username",
        "followed_by__name",
        "followed_by__user__username",
    )
    list_filter = ("profile", "followed_by")
    list_select_related = ("profile__user", "followed_by__user")
    list_per_page = 25


@admin.register(MyPost)
class MyPostAdmin(ModelAdmin):
    list_display = ("subject", "uploaded_by", "cr_date")
    search_fields = (
        "subject",
        "msg",
        "uploaded_by__name",
        "uploaded_by__user__username",
    )
    list_filter = ("cr_date", "uploaded_by")
    date_hierarchy = "cr_date"
    ordering = ("-cr_date",)
    readonly_fields = ("cr_date",)
    list_select_related = ("uploaded_by", "uploaded_by__user")
    list_per_page = 25


@admin.register(MyProfile)
class MyProfileAdmin(ModelAdmin):
    list_display = (
        "user",
        "name",
        "last_name",
        "phone_no",
        "age",
        "status",
        "gender",
        "cr_date",
    )
    search_fields = ("name", "last_name", "phone_no", "user__username", "user__email")
    list_filter = ("status", "gender", "age", "cr_date")
    date_hierarchy = "cr_date"
    ordering = ("-cr_date",)
    readonly_fields = ("cr_date",)
    list_select_related = ("user",)
    list_per_page = 25


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ("post", "commented_by", "active", "created", "updated")
    search_fields = (
        "body",
        "post__subject",
        "commented_by__name",
        "commented_by__user__username",
    )
    list_filter = ("active", "created", "updated")
    date_hierarchy = "created"
    ordering = ("-created",)
    readonly_fields = ("created", "updated")
    list_select_related = ("post", "commented_by", "commented_by__user")
    list_per_page = 25


@admin.register(PostComment)
class PostCommentAdmin(ModelAdmin):
    list_display = ("post", "commented_by", "flag", "cr_date")
    search_fields = (
        "msg",
        "post__subject",
        "commented_by__name",
        "commented_by__user__username",
    )
    list_filter = ("flag", "cr_date")
    date_hierarchy = "cr_date"
    ordering = ("-cr_date",)
    readonly_fields = ("cr_date",)
    list_select_related = ("post", "commented_by", "commented_by__user")
    list_per_page = 25


@admin.register(PostLike)
class PostLikeAdmin(ModelAdmin):
    list_display = ("post", "liked_by", "cr_date")
    search_fields = (
        "post__subject",
        "liked_by__name",
        "liked_by__user__username",
    )
    list_filter = ("cr_date",)
    date_hierarchy = "cr_date"
    ordering = ("-cr_date",)
    readonly_fields = ("cr_date",)
    list_select_related = ("post", "liked_by", "liked_by__user")
    list_per_page = 25
