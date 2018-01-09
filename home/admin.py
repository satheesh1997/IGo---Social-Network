from django.contrib import admin
from .models import VerificationToken, PasswordResetToken, Profile, Education, Feeds, Like, Comment
# Register your models here.

admin.site.register(VerificationToken)
admin.site.register(PasswordResetToken)
admin.site.register(Profile)
admin.site.register(Education)
admin.site.register(Feeds)
admin.site.register(Like)
admin.site.register(Comment)
