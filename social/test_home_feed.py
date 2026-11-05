from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from social.models import FollowUser


class HomeFeedDesignTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="feed-design-user")
        FollowUser.objects.create(
            profile=self.user.myprofile,
            followed_by=self.user.myprofile,
        )
        self.client.force_login(self.user)

    def test_feed_shows_intro_search_and_create_action(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your feed")
        self.assertContains(response, 'aria-label="Search posts"')
        self.assertContains(response, "Create post")

    def test_empty_feed_has_responsive_discovery_actions(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Your feed is ready for its first story")
        self.assertContains(response, "Discover people")
        self.assertContains(response, "Create a post")
