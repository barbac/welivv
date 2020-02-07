from uuid import uuid4
from django.db import models
from django.utils import timezone


class Business(models.Model):
    uuid = models.UUIDField()  # random uuid
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    address2 = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    zip = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    website = models.URLField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid4()
        super(Business, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} {self.name}"
