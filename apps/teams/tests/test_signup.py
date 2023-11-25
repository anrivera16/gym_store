from django.test import TestCase
from django.urls import reverse

from apps.teams.models import Team
from apps.users.models import CustomUser


class TestSignupView(TestCase):
    def test_signup_normal(self):
        self._run_test(team_name="Alice Team", expected_slug="alice-team")

    def test_signup_no_team(self):
        # if you don't specify a team it gets taken from email
        self._run_test(team_name="", expected_slug="alice")

    def test_signup_unicode_team(self):
        # unicode team names will fall back to the email address
        self._run_test(team_name="Сергей Петров", expected_slug="alice")

    def _run_test(self, team_name: str, expected_slug: str):
        response = self.client.post(
            reverse("account_signup"),
            data={
                "email": "alice@example.com",
                "password1": "Super Secret Pa$$word!",
                "team_name": team_name,
                "terms_agreement": True,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, CustomUser.objects.count())
        self.assertEqual(1, Team.objects.count())
        team = Team.objects.get()
        self.assertEqual(team_name or expected_slug, team.name)
        self.assertEqual(expected_slug, team.slug)
