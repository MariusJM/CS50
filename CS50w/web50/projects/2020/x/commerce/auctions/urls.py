from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("listing_item/<int:item_id>", views.listing_item, name="listing_item"),
    path("off_watchlist/<int:item_id>", views.off_watchlist, name="off_watchlist"),
    path("on_watchlist/<int:item_id>", views.on_watchlist, name="on_watchlist"),
]
