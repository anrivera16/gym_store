from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext

from apps.utils.timezones import get_timezones_display

from .helpers import validate_profile_picture
from .models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(label=gettext("Email"), required=True)
    language = forms.ChoiceField(label=gettext("Language"))
    timezone = forms.ChoiceField(label=gettext("Timezone"), required=False)

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "language", "timezone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        timezone = self.fields.get("timezone")
        timezone.choices = get_timezones_display()
        if settings.USE_I18N and len(settings.LANGUAGES) > 1:
            language = self.fields.get("language")
            language.choices = settings.LANGUAGES
        else:
            self.fields.pop("language")


class UploadAvatarForm(forms.Form):
    avatar = forms.FileField(validators=[validate_profile_picture])


class CustomSocialSignupForm(SocialSignupForm):
    """Custom social signup form to work around this issue:
    https://github.com/pennersr/django-allauth/issues/3266."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prevent_enumeration = False
