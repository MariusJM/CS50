from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"{self.id} {self.category_name}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey("auctions.Listing", on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.FloatField(validators=[MinValueValidator(0.01)])

    def __str__(self):
        return f"Bid #{self.id} on {self.listing.title} by {self.bidder.username}"
    

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=64, null=True, blank=False)
    image = models.URLField(null=True, blank=True)
    starting_bid = models.FloatField()
    highest_bid = models.ForeignKey(Bid, on_delete=models.SET_NULL, null=True, blank=True, related_name="bids")
    description = models.TextField(null=True, blank=False, max_length=500)
    isActive = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, null=True, blank=True, related_name="watchlist")

    def __str__(self):
        return f"Item Nr. {self.id} - {self.title}"


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name = "listing_comment")
    comment = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.commenter} comment on {self.listing}"
    class Meta:
        verbose_name = "Comment"