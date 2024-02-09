import hashlib
import urllib.parse

from django.db import models
from django.utils.safestring import mark_safe


class GreekStudyUser(models.Model):
    gs_id = models.IntegerField()
    first = models.CharField(max_length=100)
    last = models.CharField(max_length=100)
