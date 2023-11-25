from unittest.mock import patch

from django import template
from django.test import SimpleTestCase, override_settings

from apps.web.meta import websocket_absolute_url
from apps.web.templatetags.meta_tags import get_image_url


class GetImageUrlFunctionTestCase(SimpleTestCase):
    MOCK_META = {"IMAGE": "http://example.com/default_image.jpg"}

    def _run_test(self, image_url, expected_result):
        with patch("apps.web.meta.get_server_root") as mock_get_server_root:
            mock_get_server_root.return_value = "https://example.com"
            result = get_image_url(self.MOCK_META, image_url)
            self.assertEqual(result, expected_result)

    def test_with_default_fallback(self):
        self._run_test("", "http://example.com/default_image.jpg")

    def test_absolute_urls_not_touched(self):
        self._run_test("https://example.com/absolute.jpg", "https://example.com/absolute.jpg")

    @override_settings(MEDIA_URL="/media/", STATIC_URL="/static/")
    def test_static_resolution(self):
        self._run_test("/static_image.jpg", "https://example.com/static/static_image.jpg")

    @override_settings(MEDIA_URL="/media/")
    def test_with_relative_media_url_prefix(self):
        self._run_test("/media/media_image.jpg", "https://example.com/media/media_image.jpg")

    @override_settings(MEDIA_URL="https://example.s3.amazonaws.com/")
    def test_with_absolute_media_url_prefix(self):
        self._run_test(
            "https://example.s3.amazonaws.com/media/media_image.jpg",
            "https://example.s3.amazonaws.com/media/media_image.jpg",
        )


class AbsoluteUrlTestCase(SimpleTestCase):
    def test_basic_usage(self):
        template = """
{% load meta_tags %}
The URL is {% absolute_url '/test/1/' %}
"""
        self.assertEqual("The URL is https://example.com/test/1/", self._get_rendered_text(template))

    def test_with_url(self):
        template = """
{% load meta_tags %}
{% url 'web:terms' as terms_link %}
The URL is {% absolute_url terms_link %}
"""
        self.assertEqual("The URL is https://example.com/terms/", self._get_rendered_text(template))

    def _get_rendered_text(self, template_text):
        with patch("apps.web.meta.get_server_root") as mock_get_server_root:
            mock_get_server_root.return_value = "https://example.com"
            template_object = template.Template(template_text)
            return template_object.render(template.Context()).strip()


class WebsocketUrlTestCase(SimpleTestCase):
    def test_http(self):
        with patch("apps.web.meta.get_server_root") as mock_get_server_root:
            mock_get_server_root.return_value = "http://example.com"
            self.assertEqual("ws://example.com/websocket/", websocket_absolute_url("/websocket/"))

    def test_https(self):
        with patch("apps.web.meta.get_server_root") as mock_get_server_root:
            mock_get_server_root.return_value = "https://example.com"
            self.assertEqual("wss://example.com/websocket/", websocket_absolute_url("/websocket/"))
