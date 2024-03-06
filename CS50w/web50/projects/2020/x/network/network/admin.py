from django.contrib import admin
<<<<<<< HEAD
from .models import User, Posts
# Register your models here.
admin.site.register(User)
admin.site.register(Posts)
=======
from .models import Tweet, User

# Register your models here.

admin.site.register(Tweet)
admin.site.register(User)
>>>>>>> less-JS
