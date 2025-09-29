from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("details/<int:listing_id>", views.details, name="details"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove/<int:watch_id>", views.remove_watch, name="remove_watch"),
    path("listing/<int:listing_id>/toggle_watch", views.toggle_watch, name="toggle_watch"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category, name="category"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>/comment", views.add_comment, name="add_comment"),
    path("listing/<int:listing_id>/bid", views.place_bid, name="place_bid"),
    path("listing/<int:listing_id>/close", views.close_auction, name="close_auction"),
]
