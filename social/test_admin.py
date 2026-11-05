from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from unfold.admin import ModelAdmin as UnfoldModelAdmin

from social.models import (
    Comment,
    Contact,
    FollowUser,
    MyPost,
    MyProfile,
    PostComment,
    PostLike,
)


class SocialAdminDashboardTests(TestCase):
    def test_social_models_use_unfold_admin(self):
        for model in (
            Contact,
            FollowUser,
            MyPost,
            MyProfile,
            Comment,
            PostComment,
            PostLike,
        ):
            with self.subTest(model=model.__name__):
                self.assertIsInstance(admin.site._registry[model], UnfoldModelAdmin)

    def test_dashboard_shows_social_stats_chart_and_recent_posts(self):
        administrator = User.objects.create(
            username="dashboard-admin",
            is_staff=True,
            is_superuser=True,
        )
        member = User.objects.create_user(username="dashboard-member")
        post = MyPost.objects.create(
            subject="Dashboard sample post",
            uploaded_by=member.myprofile,
        )
        self.client.force_login(administrator)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Posts and new members")
        self.assertContains(response, 'data-type="line"')
        self.assertContains(response, post.subject)
        self.assertEqual(response.context["social_stats"][0]["value"], 1)
        self.assertIn('"label": "Posts"', response.context["activity_chart"])

    def test_social_model_changelists_load(self):
        administrator = User.objects.create(
            username="changelist-admin",
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(administrator)

        for model in (
            Contact,
            FollowUser,
            MyPost,
            MyProfile,
            Comment,
            PostComment,
            PostLike,
        ):
            with self.subTest(model=model.__name__):
                url = reverse(
                    f"admin:{model._meta.app_label}_{model._meta.model_name}_changelist"
                )
                self.assertEqual(self.client.get(url).status_code, 200)
