from django.db import models
from django.contrib.auth import get_user_model
from items.models import RentalItem

User = get_user_model()

# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
#     rental_item = models.ForeignKey('items.RentalItem', on_delete=models.CASCADE, related_name="comments")
#     content = models.TextField()
#     value = models.IntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     def __str__(self):
#         return f"Comment by {self.user.username} on {self.rental_item.title}"


# from django.db import models
# from django.contrib.auth.models import User
# from items.models import RentalItem

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rental_item = models.ForeignKey(RentalItem, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(blank=True, null=True,default=0)  # Add this field for rating
    # created_at = models.DateTimeField(auto_now_add=True,default=timezone.now, editable=False)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.rental_item.title}"



