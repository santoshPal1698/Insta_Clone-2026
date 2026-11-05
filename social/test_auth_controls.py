from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthControlTemplateTests(TestCase):
    def test_login_renders_password_visibility_script(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'type="password"')
        self.assertContains(response, "js/auth-controls.js")
        self.assertContains(response, "Signing in...")
        self.assertContains(response, "auth-submit-spinner")

    def test_registration_renders_passwords_and_styled_file_input(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'name="confirm_password"')
        self.assertContains(response, 'type="file"')
        self.assertContains(response, "js/auth-controls.js")
        self.assertContains(response, "Creating your account...")
        self.assertContains(response, "auth-submit-spinner")

    def test_shared_action_loader_is_loaded_on_social_and_password_pages(self):
        user = User.objects.create_user(username="action-loader-user")
        self.client.force_login(user)

        for url in (reverse("contact"), reverse("reset_password")):
            with self.subTest(url=url):
                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "js/action-loaders.js")
