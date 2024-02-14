from django.contrib import admin
from .models import User, PostContent, Follow
# Register your models here.
admin.site.register(User)
admin.site.register(PostContent)
admin.site.register(Follow)