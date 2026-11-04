from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from social.models import FollowUser, MyPost


class MyPostUpdateViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="post-owner", password="test-password")
        self.other_user = User.objects.create_user(username="other-user", password="test-password")
        self.post = MyPost.objects.create(
            uploaded_by=self.owner.myprofile,
            subject="Original subject",
            msg="Original caption",
        )
        self.edit_url = reverse("mypost_edit", kwargs={"pk": self.post.pk})

    def test_owner_can_edit_post_details(self):
        self.post.pic = "images/existing-photo.jpg"
        self.post.videofile = "videos/existing-video.mp4"
        self.post.save()
        self.client.force_login(self.owner)

        response = self.client.get(self.edit_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="pic"')
        self.assertContains(response, 'name="videofile"')
        self.assertContains(response, "Save changes")

        response = self.client.post(
            self.edit_url,
            {
                "subject": "Updated subject",
                "msg": "Updated caption",
            },
        )

        self.assertRedirects(response, reverse("mypost_list"))
        self.post.refresh_from_db()
        self.assertEqual(self.post.subject, "Updated subject")
        self.assertEqual(self.post.msg, "Updated caption")
        self.assertEqual(self.post.uploaded_by, self.owner.myprofile)
        self.assertEqual(self.post.pic.name, "images/existing-photo.jpg")
        self.assertEqual(self.post.videofile.name, "videos/existing-video.mp4")

    def test_other_user_cannot_edit_post(self):
        self.client.force_login(self.other_user)

        response = self.client.get(self.edit_url)

        self.assertEqual(response.status_code, 404)

    def test_edit_link_is_shown_to_post_owner(self):
        self.client.force_login(self.owner)

        list_response = self.client.get(reverse("mypost_list"))
        detail_response = self.client.get(f"/social/mypost/{self.post.pk}")

        self.assertContains(list_response, self.edit_url)
        self.assertContains(detail_response, self.edit_url)

    def test_login_is_required_to_edit_post(self):
        response = self.client.get(self.edit_url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))


class HomeFeedMediaTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="feed-owner", password="test-password")
        FollowUser.objects.create(
            profile=self.owner.myprofile,
            followed_by=self.owner.myprofile,
        )
        self.photo_video_post = MyPost.objects.create(
            uploaded_by=self.owner.myprofile,
            subject="Photo and video",
            pic="images/feed-photo.jpg",
            videofile="videos/feed-video.mp4",
        )
        self.photo_post = MyPost.objects.create(
            uploaded_by=self.owner.myprofile,
            subject="Photo only",
            pic="images/photo-only.jpg",
        )
        self.client.force_login(self.owner)

    def test_feed_shows_carousel_for_dual_media_and_edit_action_for_owner(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'id="post-media-{self.photo_video_post.pk}"')
        self.assertContains(response, "Photo and video")
        self.assertContains(response, "Show photo")
        self.assertContains(response, "Show video")
        self.assertContains(
            response,
            reverse("mypost_edit", kwargs={"pk": self.photo_video_post.pk}),
        )
        self.assertNotContains(response, f'id="post-media-{self.photo_post.pk}"')
