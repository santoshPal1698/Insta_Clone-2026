from django.contrib.auth.models import User
from django.test import TestCase

from social.models import FollowUser, MyPost


class PostActionLoaderTemplateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="post-action-loader-user")
        FollowUser.objects.create(
            profile=self.user.myprofile,
            followed_by=self.user.myprofile,
        )
        self.post = MyPost.objects.create(
            subject="Loader test post",
            uploaded_by=self.user.myprofile,
        )
        self.client.force_login(self.user)

    def test_post_detail_actions_have_loader_support(self):
        response = self.client.get(f"/social/mypost/{self.post.pk}")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "js/action-loaders.js")
        self.assertContains(response, 'data-loading-text="Liking post..."')
        self.assertContains(response, 'data-loading-text="Opening editor..."')
        self.assertContains(response, 'data-loading-text="Adding comment..."')

    def test_post_delete_confirmation_has_loader_support(self):
        response = self.client.get(f"/social/mypost/delete/{self.post.pk}")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-loading-text="Deleting post..."')
