from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Watchlist, Bid, Comment
from .models import Category


def index(request):
    listings = Listing.objects.filter(is_active=True).order_by('-id')
    return render(request, "auctions/index.html", {
        "listings": listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def details(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    is_watched = False
    comments = Comment.objects.filter(listing=listing).order_by('-id')
    is_winner = False
    
    if request.user.is_authenticated:
        is_watched = Watchlist.objects.filter(user=request.user, listing=listing).exists()
        
        # Vérifier si l'utilisateur est le gagnant
        if not listing.is_active and listing.listing_bid.last():
            if listing.listing_bid.last().user == request.user:
                is_winner = True
                messages.success(request, f"Congratulations! You won this auction with a bid of ${listing.current_price}!")

    return render(request, "auctions/details.html", {
        "listing": listing,
        "is_watched": is_watched,
        "comments": comments,
        "is_winner": is_winner
    })

@login_required
def watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user).order_by('-id')
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

@login_required
def remove_watch(request, watch_id):
    watch = Watchlist.objects.get(pk=watch_id)
    watch.delete()
    messages.success(request, "Item successfully removed from your watchlist!")
    return HttpResponseRedirect(reverse("watchlist"))

@login_required
def toggle_watch(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        watch = Watchlist.objects.filter(user=request.user, listing=listing).first()
        
        if watch:
            watch.delete()
            messages.success(request, "Removed from your watchlist!")
            return HttpResponseRedirect(reverse("details", args=[listing_id]))
        else:
            Watchlist.objects.create(user=request.user, listing=listing)
            messages.success(request, "Added to your watchlist!")
            return HttpResponseRedirect(reverse("details", args=[listing_id]))


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category=category, is_active=True).order_by('-id')
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })

@login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["price"]
        category = request.POST["category"]
        user = request.user
        category = Category.objects.get(pk=category)
        listing = Listing.objects.create(title=title, description=description, image=image, price=price, category=category, user=user)
        listing.save()
        messages.success(request, "Your listing has been successfully published!")
        return HttpResponseRedirect(reverse("index"))
    else:
        categories = Category.objects.all()
        return render(request, "auctions/create_listing.html", {
            "categories": categories
        })

@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        comment = request.POST["comment"]
        Comment.objects.create(
            user=request.user,
            listing=listing,
            comment=comment
        )
        messages.success(request, "Your comment has been posted!")
        return HttpResponseRedirect(reverse("details", args=[listing_id]))

@login_required
def place_bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        bid_amount = float(request.POST["bid"])
        
        if bid_amount <= float(listing.current_price):
            messages.error(request, "Your bid must be higher than the current price!")
        else:
            bid = Bid.objects.create(
                user=request.user,
                listing=listing,
                bid=bid_amount
            )
            listing.current_price = bid_amount
            listing.save()
            if not Watchlist.objects.filter(user=request.user, listing=listing).exists():
                Watchlist.objects.create(user=request.user, listing=listing)
            messages.success(request, "Your bid was placed successfully!")
            
        return HttpResponseRedirect(reverse("details", args=[listing_id]))

@login_required
def close_auction(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        
        # Vérifier que l'utilisateur est bien le créateur
        if request.user != listing.user:
            messages.error(request, "You are not authorized to close this auction!")
            return HttpResponseRedirect(reverse("details", args=[listing_id]))
        
        # Fermer l'enchère
        listing.is_active = False
        listing.save()
        
        # Notifier le gagnant s'il y a des enchères
        winning_bid = listing.listing_bid.last()
        if winning_bid:
            messages.success(request, f"Auction closed! The winner is {winning_bid.user.username} with a bid of ${winning_bid.bid}")
            # On pourrait aussi envoyer un email au gagnant ici
        else:
            messages.info(request, "Auction closed! No bids were placed.")
            
        return HttpResponseRedirect(reverse("details", args=[listing_id]))