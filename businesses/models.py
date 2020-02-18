from django.contrib.auth.models import User, Permission
from uuid import uuid4
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid4().hex[:6].upper()
        super(UserProfile, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.id}"

    class Meta():
        permissions = [('create_business', 'update_business')]


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
