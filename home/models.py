from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class VerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField(null=False)
    generated_on = models.DateTimeField(default=timezone.now)
    expired = models.BooleanField(default=False)
    expired_on = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.username


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField(null=False)
    generated_on = models.DateTimeField(default=timezone.now)
    expired = models.BooleanField(default=False)
    expired_on = models.DateTimeField(default=None)

    def __str__(self):
        return self.user.username
