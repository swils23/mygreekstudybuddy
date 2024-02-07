import hashlib
import urllib.parse

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe


class User(AbstractUser):
    gs_userID = models.IntegerField(null=True, blank=True)

    gs_email = models.EmailField(null=True, blank=True)
    gs_password = models.CharField(max_length=100, null=True, blank=True)

    hours = models.IntegerField(default=0)

    @property
    def has_linked_gs(self):
        return self.gs_userID is not None

    def _get_gravatar_url(self, size: int = 40):
        default = "https://example.com/static/images/defaultavatar.jpg"
        hashed_email = hashlib.md5(self.email.lower().encode()).hexdigest()  # nosec
        params = urllib.parse.urlencode({"d": default, "s": str(size)})
        return f"https://www.gravatar.com/avatar/{hashed_email}?{params}"

    @property
    def gravatar(self):
        size = 40
        url = self._get_gravatar_url(size=size)
        return mark_safe(f'<img src="{url}" height="{size}" width="{size}" class="rounded-5">')  # nosec
