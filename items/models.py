from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class ItemCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_of_item/', blank=True, null=True)        
    def __str__(self):
        return self.name



class RentalItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="RENTAL_ITEM")
    Category_of_items = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name="Category",null=True)
    title = models.CharField(max_length=255)
    daily_price = models.IntegerField()
    weekly_price = models.IntegerField()
    monthly_price = models.IntegerField()
    rental_period = models.IntegerField()
    market_value = models.IntegerField()
    quantity = models.IntegerField()
    location = models.CharField(max_length=255)
    description = models.TextField(max_length=200000000)
    image = models.ImageField(upload_to='rental_item_images/', blank=True, null=True)        


    def __str__(self):
        return self.title
@property
def user_profile_image_url(self):
        if self.user.profile_img:
            return self.user.profile_img.url
        return None

class CheckoutInfo(models.Model):

    Category_of_items_checkout = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name="Category_item_checkout", null=True)
    rental_item_checkout = models.ForeignKey(RentalItem, on_delete=models.CASCADE, related_name="checkout", null=True)
    username = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)
    address = models.TextField()
    country = models.CharField(max_length=100)
    note_to_lender = models.TextField()
    # Any additional fields related to the checkout process could be added here

    def __str__(self):
        return self.username




