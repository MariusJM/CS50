from django.contrib import admin
from .models import User, Listing, Comments, Category, Bid

# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comments)